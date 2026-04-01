import random
import string
import uuid
from google.protobuf.descriptor import FieldDescriptor

TYPE_DOUBLE = FieldDescriptor.TYPE_DOUBLE
TYPE_FLOAT = FieldDescriptor.TYPE_FLOAT
TYPE_INT64 = FieldDescriptor.TYPE_INT64
TYPE_UINT64 = FieldDescriptor.TYPE_UINT64
TYPE_INT32 = FieldDescriptor.TYPE_INT32
TYPE_FIXED64 = FieldDescriptor.TYPE_FIXED64
TYPE_FIXED32 = FieldDescriptor.TYPE_FIXED32
TYPE_BOOL = FieldDescriptor.TYPE_BOOL
TYPE_STRING = FieldDescriptor.TYPE_STRING
TYPE_BYTES = FieldDescriptor.TYPE_BYTES
TYPE_UINT32 = FieldDescriptor.TYPE_UINT32
TYPE_SFIXED32 = FieldDescriptor.TYPE_SFIXED32
TYPE_SFIXED64 = FieldDescriptor.TYPE_SFIXED64
TYPE_SINT32 = FieldDescriptor.TYPE_SINT32
TYPE_SINT64 = FieldDescriptor.TYPE_SINT64


def generate_scalar(
    field_type: int, field_name: str = "", use_faker: bool = False, faker_instance=None
):
    field_lower = field_name.lower()

    if use_faker and faker_instance and field_type == TYPE_STRING:
        if "email" in field_lower:
            return faker_instance.email()
        elif "url" in field_lower:
            return faker_instance.url()
        elif "phone" in field_lower:
            return faker_instance.phone_number()
        elif "address" in field_lower:
            return faker_instance.address()
        elif "city" in field_lower:
            return faker_instance.city()
        elif "country" in field_lower:
            return faker_instance.country()
        elif "name" in field_lower:
            return faker_instance.name()
        elif "uuid" in field_lower or "guid" in field_lower or "id" in field_lower:
            return faker_instance.uuid4()

    if "uuid" in field_lower or "guid" in field_lower or "id" in field_lower:
        if field_type == TYPE_STRING:
            return str(uuid.uuid4())
        elif field_type == TYPE_BYTES:
            return uuid.uuid4().bytes

    if field_type in (TYPE_DOUBLE, TYPE_FLOAT):
        return random.uniform(-1000.0, 1000.0)
    elif field_type in (TYPE_INT64, TYPE_SINT64, TYPE_SFIXED64):
        return random.randint(-1000000, 1000000)
    elif field_type in (TYPE_INT32, TYPE_SINT32, TYPE_SFIXED32):
        return random.randint(-10000, 10000)
    elif field_type in (TYPE_UINT64, TYPE_FIXED64):
        return random.randint(0, 1000000)
    elif field_type in (TYPE_UINT32, TYPE_FIXED32):
        return random.randint(0, 10000)
    elif field_type == TYPE_BOOL:
        return random.choice([True, False])
    elif field_type == TYPE_STRING:
        if use_faker and faker_instance:
            return faker_instance.word()
        return "".join(random.choices(string.ascii_letters, k=8))
    elif field_type == TYPE_BYTES:
        return bytes(random.choices(range(256), k=16))

    return None
