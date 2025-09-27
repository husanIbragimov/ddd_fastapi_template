from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import BaseModel


class UploadModel(BaseModel):
    __tablename__ = "upload_files"

    url: Mapped[str] = mapped_column(String(255))

    def __repr__(self):
        return f"<UploadModel file_name={self.file_name} url={self.url}>"
