from pydantic import BaseModel

class Rule(BaseModel):
    name: str
    current_price: int
    target_price: int
    message : str
    action: str

class RuleUpdate(BaseModel):
    name: str | None = None
    current_price: int | None = None
    target_price: int | None = None
    message : str | None = None
    action: str | None = None

class UserCreate(BaseModel):
    username : str
    password : str