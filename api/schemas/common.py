from pydantic import BaseModel, Field



class SuccessfullResponse(BaseModel):
    details: str = Field("Выполнено", title="Статус операции")


class TokenOut(BaseModel):
    access_token: str = Field(..., description="Access token")
    token_type: str = Field(..., description="Token type")