from pydantic import BaseModel, Field



class SuccessfullResponse(BaseModel):
    details: str = Field("Выполнено", title="Статус операции")

class TokenIn(BaseModel):
    access_token: str = Field(..., description='Авторизационный токен')

class TokenOut(BaseModel):
    access_token: str = Field(..., description="Авторизационный токен")
    token_type: str = Field(..., description="Тип токена")

class Pagination(BaseModel):
    number_of_items: int = Field(..., gt=0, le=50, description="Количество сущностей на страницу")
    page: int = Field(..., gt=0, description="Номер страницы")