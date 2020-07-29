from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

@dataclass
class Entity:
    name: str
    probability: float
    description: str
    uri: str
    start_pos: int = 0
    end_pos: int = 0


class EntityDatabase(ABC):

    @abstractmethod
    def __init__(self, entity):
        return NotImplemented

    @abstractmethod
    def _get_probabilities(self) -> Dict:
        return NotImplemented

