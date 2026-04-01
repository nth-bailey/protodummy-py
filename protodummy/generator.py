import random
from typing import Type, TypeVar, Any

from google.protobuf.message import Message
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf import message_factory

from .config import GenerationConfig
from .types import generate_scalar

T = TypeVar("T", bound=Message)


class ProtoGenerator:
    def __init__(self, config: GenerationConfig):
        self.config = config
        self.faker = None
        if self.config.use_faker:
            try:
                from faker import Faker

                self.faker = Faker()
            except ImportError:
                import warnings

                warnings.warn(
                    "Faker is not installed. Disabling realistic data generation."
                )
                self.config.use_faker = False

    def _generate_message(self, message_cls: Type[T], current_depth: int) -> T:
        instance = message_cls()

        if current_depth > self.config.max_depth:
            return instance

        descriptor = message_cls.DESCRIPTOR
        assert descriptor is not None

        # Handle oneofs by picking exactly one field per oneof group
        oneof_fields_to_set = set()
        for oneof in descriptor.oneofs:
            if oneof.fields:
                chosen_field = random.choice(oneof.fields)
                oneof_fields_to_set.add(chosen_field.name)

        for field in descriptor.fields:
            if (
                field.containing_oneof is not None
                and field.name not in oneof_fields_to_set
            ):
                continue

            if (
                current_depth >= self.config.max_depth
                and field.type == FieldDescriptor.TYPE_MESSAGE
            ):
                continue

            self._populate_field(instance, field, current_depth)

        return instance

    def _populate_field(
        self, parent_msg: Message, field: FieldDescriptor, current_depth: int
    ):
        if field.is_repeated:
            if field.message_type and field.message_type.GetOptions().map_entry:
                self._populate_map_field(parent_msg, field, current_depth)
            else:
                self._populate_repeated_field(parent_msg, field, current_depth)
        else:
            value = self._get_single_value(field, current_depth)
            if value is not None:
                if field.type == FieldDescriptor.TYPE_MESSAGE:
                    getattr(parent_msg, field.name).CopyFrom(value)
                else:
                    setattr(parent_msg, field.name, value)

    def _populate_repeated_field(
        self, parent_msg: Message, field: FieldDescriptor, current_depth: int
    ):
        count = random.randint(*self.config.list_size_range)
        repeated_container = getattr(parent_msg, field.name)
        for _ in range(count):
            if field.type == FieldDescriptor.TYPE_MESSAGE:
                sub_msg = self._generate_nested_message(
                    field.message_type, current_depth + 1
                )
                repeated_container.add().CopyFrom(sub_msg)
            else:
                val = self._get_single_value(field, current_depth)
                if val is not None:
                    repeated_container.append(val)

    def _populate_map_field(
        self, parent_msg: Message, field: FieldDescriptor, current_depth: int
    ):
        count = random.randint(*self.config.map_size_range)
        map_container = getattr(parent_msg, field.name)
        key_field = field.message_type.fields_by_name["key"]
        value_field = field.message_type.fields_by_name["value"]

        for _ in range(count):
            key = self._get_single_value(key_field, current_depth)
            if key is None:
                continue

            if value_field.type == FieldDescriptor.TYPE_MESSAGE:
                sub_msg = self._generate_nested_message(
                    value_field.message_type, current_depth + 1
                )
                map_container[key].CopyFrom(sub_msg)
            else:
                val = self._get_single_value(value_field, current_depth)
                if val is not None:
                    try:
                        map_container[key] = val
                    except TypeError:
                        pass  # Ignore if key is unhashable or invalid

    def _generate_nested_message(self, message_descriptor, current_depth: int):
        msg_class = message_factory.GetMessageClass(message_descriptor)
        return self._generate_message(msg_class, current_depth)

    def _get_single_value(self, field: FieldDescriptor, current_depth: int) -> Any:
        if field.type == FieldDescriptor.TYPE_MESSAGE:
            return self._generate_nested_message(field.message_type, current_depth + 1)
        elif field.type == FieldDescriptor.TYPE_ENUM:
            return random.choice(field.enum_type.values).number
        else:
            return generate_scalar(
                field.type, field.name, self.config.use_faker, self.faker
            )


def generate(message_cls: Type[T], config: GenerationConfig | None = None) -> T:
    if config is None:
        config = GenerationConfig()
    generator = ProtoGenerator(config)
    return generator._generate_message(message_cls, 0)
