from dataclasses import dataclass

from uuid import UUID

from application.dto import CategoryDTO


@dataclass
class CategoryEntity:
    uuid: UUID | None
    name: str
    description: str | None = None

    def to_dto(self) -> CategoryDTO:
        return CategoryDTO(
            uuid=self.uuid,
            name=self.name,
            description=self.description
        )

