from base_adapter import Entity

class NERD:

    def disambiguate(entities: List[Entity]) -> Entity:
        for entity in entities:
            entity.description
            # compare with surrounding words
            # maximum entities
