from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID

from .base_model import BaseModel


class ProductImageModel(BaseModel):
    __tablename__ = "product_images"

    product_id: Mapped[UUID] = mapped_column(ForeignKey("products.uuid", ondelete="CASCADE"))
    image_id: Mapped[UUID] = mapped_column(ForeignKey("upload_files.uuid", ondelete="CASCADE"))

    def __repr__(self):
        return f"<ProductImageModel product_id={self.product_id} image_id={self.image_id}>"
