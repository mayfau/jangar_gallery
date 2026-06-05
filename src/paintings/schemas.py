from pydantic import BaseModel

class PaintingCreate(BaseModel):
    title: str
    description: str
    price: int
    image_url: str | None = ""

class PaintingOut(BaseModel):
    id: int
    title: str
    description: str | None = ""
    price: int
    image_url: str | None = ""

    class Config:
        from_attributes = True