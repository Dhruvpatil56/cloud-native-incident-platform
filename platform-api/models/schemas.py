from pydantic import BaseModel


class ServiceMetadata(BaseModel):
    name: str
    owner: str
    tier: str
