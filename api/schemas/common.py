from pydantic import BaseModel, Field



class SuccessfullResponse(BaseModel):
    details: str = Field("Выполнено", title="Статус операции")

class TokenIn(BaseModel):
    access_token: str = Field(..., description='Авторизационный токен')

class TokenOut(BaseModel):
    access_token: str = Field(..., description="Авторизационный токен")
    token_type: str = Field(..., description="Тип токена")