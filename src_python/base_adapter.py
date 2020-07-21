from abc import ABC
from dataclasses import dataclass
from typing import List

@dataclass
class Entity:
    name: str
    probabity: float
    description: str
    uri: str


class EntityDatabase(ABC):

    def __init__(entity):
        self.entity = entity

    @abstractmethod
    def __possible_entities__(self) -> List[Entity]:
        raise NotImplemented

         
