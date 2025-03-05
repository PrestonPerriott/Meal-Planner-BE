from sqlmodel import SQLModel, Field
import uuid
import datetime

def get_utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

class GroceryItemBase(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str | None = Field(default=None)
    brand: str | None = Field(default=None)
    image: str | None = Field(default=None, max_length=512)
    link: str | None = Field(default=None, max_length=512)
    price: float | None = Field(default=None)
    uom: str | None = Field(default=None, max_length=50)
    chain: str | None = Field(default=None, max_length=100)
    store: str | None = Field(default=None, max_length=100)
    created_at: datetime.datetime | None = Field(default_factory=get_utc_now)
    updated_at: datetime.datetime | None = Field(default_factory=get_utc_now, sa_column={"onupdate": get_utc_now})
    
class GroceryItem(GroceryItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
class CreateGroceryItem(GroceryItemBase):
    pass

class GroceryItems(SQLModel):
    data: list[GroceryItem]
    count: int