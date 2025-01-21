from dataclasses import dataclass, field


@dataclass
class Entity[ID]:
    id: ID = field(hash=True)

    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.id == other.id
        return False
