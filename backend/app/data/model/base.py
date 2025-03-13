from sqlmodel import SQLModel, Field
import uuid 
import datetime
from typing import Optional

def get_utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime.datetime | None = Field(default_factory=get_utc_now)
    updated_at: datetime.datetime | None = Field(default_factory=get_utc_now, sa_column={"onupdate": get_utc_now})