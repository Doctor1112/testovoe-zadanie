import asyncio
import contextlib
import importlib
import json
import sys
import typing
from enum import Enum
from functools import partial

from pydantic import BaseModel as PydanticBaseModel, ValidationError
from tortoise import Model

from project.enums.custom_encode_type import CustomEncodeType


class CustomJsonItemModel(PydanticBaseModel):
    encode_type: CustomEncodeType
    class_module: str
    class_name: str
    value: typing.Any


class CustomDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
        self.loop = asyncio.get_event_loop()

    def object_hook(self, obj: dict) -> Model | PydanticBaseModel | Enum | dict:
        with contextlib.suppress(ValidationError):
            item = CustomJsonItemModel.parse_obj(obj)
            importlib.import_module(item.class_module)
            cls = getattr(sys.modules[item.class_module], item.class_name)
            match item.encode_type:
                case CustomEncodeType.TORTOISE:
                    return self.loop.run_until_complete(cls.get_or_none(id=item.value))  # bad practice. nest-asyncio
                case CustomEncodeType.PYDANTIC:
                    return cls.parse_obj(item.value)
                case CustomEncodeType.ENUM:
                    return cls(item.value)
        return obj


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        kwargs = dict()
        if isinstance(obj, Model):
            kwargs = dict(
                encode_type=CustomEncodeType.TORTOISE,
                value=obj.id,  # noqa
            )
        if isinstance(obj, PydanticBaseModel):
            kwargs = dict(
                encode_type=CustomEncodeType.PYDANTIC,
                value=json.loads(obj.json()),
            )
        if isinstance(obj, Enum):
            kwargs = dict(
                encode_type=CustomEncodeType.ENUM,
                value=obj.value,
            )
        if kwargs:
            return json.loads(CustomJsonItemModel(
                class_module=obj.__module__,
                class_name=obj.__class__.__name__,
                **kwargs,
            ).json())
        return super().default(obj)


custom_encoder = CustomEncoder()
custom_decoder = CustomDecoder()
custom_json_loads = partial(json.loads, cls=CustomDecoder)
custom_json_dumps = partial(json.dumps, cls=CustomEncoder)


class CustomBaseModel(PydanticBaseModel):
    """Inherit from this class if you want to have de/serializable child tortoise orm models"""

    class Config:
        arbitrary_types_allowed = True
        json_loads = custom_json_loads
        json_dumps = custom_json_dumps

        json_encoders = {
            Model: lambda model: custom_encoder.default(model),
        }
