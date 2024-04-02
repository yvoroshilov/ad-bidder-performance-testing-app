import datetime
import functools
import logging
import random
import typing
from collections.abc import Collection
from typing import TypeVar, Type, Any

import pydantic
import yaml

Model = TypeVar("Model", bound="BaseModel")
logging.basicConfig(level="DEBUG", format="[%(asctime)s] %(levelname)s %(message)s")

primitives = {
    bool,
    str,
    int,
    float,
    typing.Any,
    datetime.datetime
}
iterables = {
    set,
    list,
    tuple,
    typing.List,
    typing.Set,
    typing.Tuple
}


def gen_for_composite(model_type: Type[Model], *, str_size: int = 1, arr_size: int = 1,
                      excluded_fields: Collection[str] = (), custom_values: dict[str, Any] = {}) -> Model:
    """
    1. Check if current field is in the config
    2. if in the config, check if multiple values
    3. if multiple values, choose random
    4. if one choose one
    5. if not in the config, call any of _gen
    """

    class_members = typing.get_type_hints(model_type)
    class_members = filter(
        lambda attr: _class_fields_only_filter(attr[0], model_type), class_members.items())
    class_members = map(
        lambda attr: (attr[0], _map_optional_to_normal(attr[1])), class_members)
    class_members = dict(class_members)

    if len(class_members) == 0:
        raise Exception(f"Unknown type={model_type}!")

    config = _read_config()
    name_value = {}
    for attr_name in class_members:
        logging.debug(f"attr_name={attr_name}")
        value = custom_values.get(attr_name)
        if attr_name not in custom_values and attr_name not in excluded_fields:
            attr_type = class_members[attr_name]
            value = _get_value_from_config(model_type, attr_type, attr_name, config)
            if value is None:
                value = _gen_value(attr_type, arr_size=arr_size, str_size=str_size)
        name_value[attr_name] = value

    if issubclass(model_type, pydantic.BaseModel):
        model = model_type.model_validate(name_value)
    else:
        model = model_type()
        for name in name_value:
            setattr(model, name, name_value[name])
    return model


def _get_value_from_config(model_type: Type, attr_type: Type, attr_name: str, config: dict) -> Any:
    model_type_name = model_type.__name__
    config_path = ".".join((model_type_name, attr_name))
    config_value = _access_config_dot(config_path, config)

    result = None
    if config_value is not None:
        if _is_iterable_type(attr_type):
            if _is_iterable_type(type(config_value)):
                result = config_value
            else:
                raise Exception(f"Expected {attr_type}, got {type(config_value)} for path {config_path}")
        else:
            if _is_iterable_type(type(config_value)):
                result = random.choice(config_value)
            elif type(config_value) == attr_type:
                result = config_value
            else:
                raise Exception(f"Expected {attr_type}, got {type(config_value)} for path {config_path}")

    return result


def _gen_value(attr_type: Any, recursion_level: int = 0, arr_size: int = 1, str_size: int = 1) -> Any:
    recursion_pad = "  " * recursion_level
    logging.debug(recursion_pad + f"attr_type={attr_type}")
    primitive_gens = {
        bool: _gen_bool,
        str: _gen_str,
        int: _gen_int,
        float: _gen_float,
        typing.Any: _gen_any,
        datetime.datetime: lambda **_: datetime.datetime.now()
    }

    if _is_primitive_type(attr_type):
        value = primitive_gens[attr_type](str_size=str_size)
        result = value
    elif _is_iterable_type(attr_type):
        arr = []
        iterable_elem_type = typing.get_args(attr_type)[0]
        for _ in range(arr_size):
            logging.debug(recursion_pad + f"Descending into recursion 😨, level={recursion_level + 1}")
            arr.append(_gen_value(iterable_elem_type, recursion_level + 1))
        result = arr
    elif issubclass(attr_type, pydantic.BaseModel):
        logging.debug(recursion_pad + f"Composing {attr_type} 😨😨")
        result = gen_for_composite(attr_type)
        logging.debug(recursion_pad + f"Composed {attr_type} 😌😌!")
    else:
        raise Exception(f"Unknown type={attr_type}!")

    if recursion_level > 0:
        logging.debug(recursion_pad + f"Ending recursion 😌, level={recursion_level}")

    return result


def _gen_str(**kwargs) -> str:
    str_size = kwargs["str_size"]
    str_len = random.randint(1, str_size)
    result = functools.reduce(lambda prev, cur: prev + cur, {chr(random.randint(32, 126)) for _ in range(str_len)})
    return result


def _gen_int(**kwargs) -> int:
    return random.randint(0, 100)


def _gen_float(**kwargs) -> float:
    return random.random() * random.choice((1, 10, 100))


def _gen_bool(**kwargs) -> bool:
    return random.choice((True, False))


def _gen_any(**kwargs) -> Any:
    class Empty(pydantic.BaseModel):
        pass

    return Empty()


def _is_primitive_type(typ: Type) -> bool:
    return typ in primitives


def _is_iterable_type(typ: Type) -> bool:
    return typ in iterables or typing.get_origin(typ) in iterables


def _class_fields_only_filter(attr_name: str, typ: Type[Any]) -> bool:
    return not attr_name.startswith("_") and (not hasattr(typ, attr_name) or not callable(getattr(typ, attr_name)))


def _map_optional_to_normal(typ: Type) -> Type:
    args = typing.get_args(typ)
    if len(args) < 2:
        return typ

    typ1, typ2 = args
    if typ2 != type(None):
        raise Exception(f"Provided type ({typ}) is not generic")
    return typ1


def _read_config() -> dict:
    with open("config.yml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def _access_config_dot(key: str, config: dict) -> Any:
    return functools.reduce(lambda cfg, part:
                            cfg[part] if cfg is not None and part in cfg else None, key.split("."), config)


if __name__ == "__main__":
    class Test2(pydantic.BaseModel):
        a: int | None
        b: "Test"
        c: list[str]


    class Test(pydantic.BaseModel):
        a: int | None
        b: str | None
        z: float | None
        c: list[str] | None
        x: typing.Optional[str]

        def foo(self, d: int) -> str:
            return "e"


    logging.debug(gen_for_composite(AdRequest).model_dump_json(indent=2))
