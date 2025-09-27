from typing import Dict

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel


class CategoryModel(BaseModel):
    __tablename__ = "categories"

    name: Mapped[Dict] = mapped_column(JSON, default=dict)
    description: Mapped[Dict] = mapped_column(JSON, default=dict)

    products = relationship("ProductModel", back_populates="category")

    def __repr__(self):
        return f"<CategoryModel name={self.name}>"