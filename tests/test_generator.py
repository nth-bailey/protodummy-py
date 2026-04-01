from typing import Any
from protodummy import generate, GenerationConfig
from . import test_proto_pb2

User: Any = getattr(test_proto_pb2, "User")
RecursiveNode: Any = getattr(test_proto_pb2, "RecursiveNode")


def test_generate_user():
    config = GenerationConfig(use_faker=False)
    user = generate(User, config)

    assert isinstance(user, User)
    assert isinstance(user.id, str)
    assert len(user.id) > 0
    assert isinstance(user.age, int)

    # Check repeated and map
    assert len(user.roles) >= 1
    assert len(user.scores) >= 1

    # Check nested message
    assert user.HasField("address")
    assert isinstance(user.address.city, str)

    # Check oneof
    assert user.WhichOneof("avatar") in ["avatar_url", "avatar_bytes"]


def test_generate_user_faker():
    config = GenerationConfig(use_faker=True)
    user = generate(User, config)

    assert isinstance(user, User)
    # Check that faker probably generated an email address
    assert "@" in user.email


def test_recursive_node():
    config = GenerationConfig(max_depth=2, use_faker=False)
    node = generate(RecursiveNode, config)

    assert isinstance(node, RecursiveNode)
    # Check it generated nested nodes but eventually stopped.
    depth = 0
    curr = node
    while curr.HasField("left"):
        depth += 1
        curr = curr.left
    assert depth <= 2
