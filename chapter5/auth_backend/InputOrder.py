from pydantic import BaseModel


class InputOrder(BaseModel):
    userId: str