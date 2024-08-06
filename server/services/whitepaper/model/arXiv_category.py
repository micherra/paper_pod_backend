from pydantic import BaseModel


class ArXivCategory(BaseModel):
    id: str
    name: str
    category: str
    description: str
