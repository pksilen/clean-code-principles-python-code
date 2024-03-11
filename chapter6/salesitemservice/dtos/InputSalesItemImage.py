from pydantic import AfterValidator, BaseModel, HttpUrl, PositiveInt
from typing_extensions import Annotated

HttpUrlString = Annotated[HttpUrl, AfterValidator(lambda url: str(url))]


class InputSalesItemImage(BaseModel):
    rank: PositiveInt
    url: HttpUrlString
