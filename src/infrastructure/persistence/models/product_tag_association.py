from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import BaseModel


class ProductTagModel(BaseModel):
    __tablename__ = "product_tag"

    product_id: Mapped[str] = mapped_column(
        ForeignKey("products.uuid", ondelete="CASCADE"), primary_key=True
    )
    tag_id: Mapped[str] = mapped_column(
        ForeignKey("tags.uuid", ondelete="CASCADE"), primary_key=True
    )

    def __repr__(self):
        return f"<ProductTagModel product_id={self.product_id} tag_id={self.tag_id}>"
