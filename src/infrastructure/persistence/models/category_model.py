from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    # products: Mapped[List] = relationship("ProductModel", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CategoryModel name={self.name}>"