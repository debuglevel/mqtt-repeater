from pydantic import BaseModel

class PersonIn(BaseModel):
    name: str

class PersonOut(BaseModel):
    name: str
    created_on: str