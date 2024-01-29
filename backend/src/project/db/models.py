import typing

from tortoise import Model, fields, Tortoise
from tortoise.expressions import F, Function, Aggregate
from tortoise.functions import Sum, Coalesce, Concat, Trim, Count
from tortoise.models import MODEL
from tortoise.queryset import QuerySet

from aiogram import types
from aiogram.fsm.storage.base import StorageKey
from aiogram.utils import markdown as md
from aiogram.utils.web_app import WebAppUser

from project.utils.custom_encoders import custom_json_loads, custom_json_dumps


class BaseModel(Model):
    id = fields.BigIntField(pk=True)

    @classmethod
    async def update_or_create_custom(
            cls: MODEL,
            unique: dict[str, typing.Any],
            other: dict[str, typing.Any]
    ) -> tuple[MODEL, bool]:
        instance: MODEL = await cls.get_or_none(**unique)
        if instance is not None:
            await instance.update_from_dict(other)
            await instance.save(update_fields=other)
            created = False
        else:
            instance = await cls.create(**unique, **other)
            created = True
        return instance, created

    async def get_prev_and_next(self: MODEL, items: QuerySet[MODEL] | list[MODEL]) -> tuple[MODEL | None, MODEL | None]:
        if isinstance(items, QuerySet):
            items = await items
        index = items.index(self)
        prev_item = items[prev_index] if (prev_index := index - 1) >= 0 else None
        next_item = items[next_index] if (next_index := index + 1) < len(items) else None
        return prev_item, next_item

    @classmethod
    async def sum(cls, field_name: str, **filter_kwargs) -> float:
        return await cls.aggregate(Sum(field_name), **filter_kwargs) or 0.0

    @classmethod
    async def distinct_count(cls: MODEL, field_name: str = 'id', **filter_kwargs) -> int:
        return await cls.aggregate(Count(field_name, distinct=True), **filter_kwargs) or 0

    @classmethod
    async def aggregate(cls: MODEL, function: Aggregate, **filter_kwargs):
        annotate_key = f'{function.field}_{function.__class__.__name__}'
        query = await cls \
            .filter(**filter_kwargs) \
            .annotate(**{annotate_key: function}) \
            .first() \
            .values(annotate_key)
        return query[annotate_key] if query else None

    class Meta:
        abstract = True

    class PydanticMeta:
        exclude_raw_fields = True
        max_recursion = 15


class FSMData(BaseModel):
    bot_id = fields.BigIntField()
    chat_id = fields.BigIntField()
    user: fields.ForeignKeyRelation['User'] = fields.ForeignKeyField(
        model_name='models.User',
        related_name='fsm_data',
    )
    destiny = fields.TextField()
    data = fields.JSONField(
        default={},
        encoder=custom_json_dumps,
        decoder=custom_json_loads,
    )
    state = fields.TextField(null=True)

    @classmethod
    async def get_by_storage_key(cls, key: StorageKey) -> 'FSMData':
        user = await User.get_current()  # TODO: optimize
        assert user.id == key.user_id
        model, created = await cls.get_or_create(
            bot_id=key.bot_id,
            chat_id=key.chat_id,
            user=user,
            destiny=key.destiny,
        )
        return model

    class Meta:
        unique_together = (
            'bot_id',
            'chat_id',
            'user',
            'destiny',
        )


class CreatedAtMixin:
    created_at = fields.DatetimeField(auto_now_add=True)


class UpdatedAtMixin:
    updated_at = fields.DatetimeField(auto_now=True)


class User(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    tg_first_name = fields.TextField()
    tg_last_name = fields.TextField(null=True)
    tg_username = fields.TextField(null=True)
    language = fields.CharField(default='ru', max_length=4)
    phone_number = fields.CharField(max_length=32, unique=True, null=True)
    is_banned = fields.BooleanField(default=False)

    age = fields.IntField(null=True)
    first_name = fields.TextField(null=True)

    card_token = fields.TextField(null=True)
    card_first_six = fields.IntField(null=True)
    card_last_four = fields.IntField(null=True)
    card_type = fields.TextField(null=True)
    card_exp_date = fields.TextField(null=True, description='MM/YY')

    context = fields.JSONField(
        default={},
        decoder=custom_json_loads,
        encoder=custom_json_dumps,
    )

    messages: fields.ReverseRelation['Message']
    communities: fields.ReverseRelation['Community']
    subscriptions: fields.ReverseRelation['Subscription']

    tg_full_name_annotations: dict[str, Function] = dict(
        tg_first_and_last_name=Trim(Concat(Coalesce(F('tg_first_name'), ''), ' ', Coalesce(F('tg_last_name'), ''))),
        tg_last_and_first_name=Trim(Concat(Coalesce(F('tg_last_name'), ''), ' ', Coalesce(F('tg_first_name'), ''))),
    )

    def tg_full_name(self) -> str:
        return f"{self.tg_first_name or ''} {self.tg_last_name or ''}".strip()

    @property
    def full_name(self) -> str:
        return self.tg_full_name()

    @property
    def tg_link(self) -> str:
        return md.hlink(self.full_name, f'tg://user?id={self.id}')

    @classmethod
    async def get_current(cls) -> 'User':
        tg_user = types.User.get_current()
        user = await User.get_or_none(id=tg_user.id)
        if user is None:
            user = await User.new(tg_user)
        else:
            update_fields = dict(
                tg_first_name=tg_user.first_name,
                tg_last_name=tg_user.last_name or None,
                tg_username=tg_user.username or None,
            )
            await user.update_from_dict(update_fields)
            await user.save(update_fields=update_fields)
        return user

    @classmethod
    async def new(cls, tg_user: types.User | WebAppUser) -> 'User':
        user = await cls.create(
            id=tg_user.id,
            tg_first_name=tg_user.first_name,
            tg_last_name=tg_user.last_name or None,
            tg_username=tg_user.username or None,
        )
        return user

    class PydanticMeta(BaseModel.PydanticMeta):
        exclude = (
            'context',
            'fsm_data', 'messages',
            'card_token',
        )


Tortoise.init_models(['project.db.models'], 'models')
