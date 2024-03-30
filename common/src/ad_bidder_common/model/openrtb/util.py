from typing import Any, List, TypeVar, Union

from pydantic import field_validator

Model = TypeVar("Model", bound=Union["BaseModel", "MongoDbMixin"])


class MongoDbMixin:
    _id: str | None = None

    @field_validator("id", mode="before", check_fields=False)
    @classmethod
    def validate_id(cls, obj: Any) -> str | None:
        return str(obj) if obj is not None else None

    @classmethod
    def validate_mongo(cls, obj: Any, **kwargs) -> Model:
        model = cls.model_validate(obj, **kwargs)
        model.id = str(obj["_id"]) if obj["_id"] is not None else model.id
        return model

    @classmethod
    def validate_mongo_many(cls, objs: List[Any], **kwargs) -> List[Model]:
        models = []
        for obj in objs:
            model = cls.validate_mongo(obj, **kwargs)
            models.append(model)
        return models

    def dump_mongo(self, **kwargs):
        return self.model_dump(exclude={"id"}, **kwargs)
