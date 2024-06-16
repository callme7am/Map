from pydantic import BaseModel


class CreateQueryArchiveOpts(BaseModel):
    text: str
    elapsed_time: float
