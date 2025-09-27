from typing import List, Dict

from sqlalchemy import JSON, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import BaseModel
from .category_model import CategoryModel
from .product_image_model import ProductImageModel
from .tag_model import TagModel


product_tag = Table(
    "product_tag",
    BaseModel.metadata,
    Column("product_id", ForeignKey("products.uuid"), primary_key=True),
    Column("tag_id", ForeignKey("tags.uuid"), primary_key=True),
)


class ProductModel(BaseModel):
    __tablename__ = "products"

    name: Mapped[Dict] = mapped_column(JSON, default=dict)
    description: Mapped[Dict] = mapped_column(JSON, default=dict)
    price: Mapped[float] = mapped_column()
    stock: Mapped[int] = mapped_column()

    category_id: Mapped[str] = mapped_column(ForeignKey("categories.uuid", ondelete="CASCADE"))
    category: Mapped[CategoryModel] = relationship("CategoryModel", back_populates="products")

    tags: Mapped[List[TagModel]] = relationship("TagModel", secondary=product_tag, back_populates="products")

    images: Mapped[List[ProductImageModel]] = relationship("ProductImageModel", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProductModel name={self.name} price={self.price} stock={self.stock}>"
