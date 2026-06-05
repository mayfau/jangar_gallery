from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class PaintingModel(Base):
    __tablename__ = "paintings"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    price: Mapped[int]
    quote: Mapped[str | None]
    image_url: Mapped[str | None] = mapped_column(String, default="")