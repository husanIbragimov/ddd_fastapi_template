from .base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"<CategoryModel name={self.name}>"