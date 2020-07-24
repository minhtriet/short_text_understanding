from base_adapter import Entity
from typing import List

class NERD:

    def disambiguate(entities: List[Entity]) -> Entity:
        for entity in entities:
            entity.description
            # compare with surrounding words
            # maximum entities
