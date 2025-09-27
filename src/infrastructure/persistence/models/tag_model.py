from typing import Dict

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel
from .product_tag_association import ProductTagModel


class TagModel(BaseModel):
    __tablename__ = "tags"

    name: Mapped[Dict] = mapped_column(JSON, default=dict)

    products = relationship("ProductModel", secondary="product_tag", back_populates="tags")

    def __repr__(self):
        return f"<TagModel name={self.name}>"


