from typing import List, Dict

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import CategoryModel
from .base_model import BaseModel
from .tag_model import TagModel


class ProductModel(BaseModel):
    __tablename__ = "products"

    name: Mapped[Dict] = mapped_column(JSON, default=dict)
    description: Mapped[Dict] = mapped_column(JSON, default=dict)
    price: Mapped[float] = mapped_column()
    stock: Mapped[int] = mapped_column()

    category_id: Mapped[str] = mapped_column(ForeignKey("categories.uuid", ondelete="CASCADE"))
    category: Mapped[CategoryModel] = relationship("CategoryModel", back_populates="products")

    tags: Mapped[List[TagModel]] = relationship("TagModel", secondary="product_tag", back_populates="products")

    def __repr__(self):
        return f"<ProductModel name={self.name} price={self.price} stock={self.stock}>"
