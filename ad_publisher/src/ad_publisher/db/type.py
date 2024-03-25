from typing import Annotated, Any

from bson import ObjectId
from pydantic import BeforeValidator, PlainSerializer


def object_id_validator(obj_id: Any) -> ObjectId | None:
    if obj_id is None:
        return None
    elif isinstance(obj_id, str):
        return ObjectId(obj_id)
    else:
        raise Exception(f"Can't convert object {obj_id} of type {type(obj_id)} to ObjectId")


def object_id_serializer(obj_id: ObjectId) -> str:
    return str(obj_id) if obj_id is not None else None


PyObjectId = Annotated[ObjectId, BeforeValidator(object_id_validator), PlainSerializer(object_id_serializer)]
