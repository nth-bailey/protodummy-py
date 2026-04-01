from dataclasses import dataclass
from typing import Tuple


@dataclass
class GenerationConfig:
    """Configuration for protobuf random data generation."""

    max_depth: int = 5
    list_size_range: Tuple[int, int] = (1, 5)
    map_size_range: Tuple[int, int] = (1, 5)
    use_faker: bool = False
