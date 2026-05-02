from pydantic import BaseModel
from typing import Optional


"""
O que meu backend busca?: Não entra
e o que meu usuario manda no front: Entra

"""


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    cpf: str
    senha: str
    ativo: Optional[bool]

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    cpf: str
    senha: str

    class Config:
        from_attributes = True


class TransacaoCreate(BaseModel): 
    conta_de_destino_numero: str
    valor: float 
    
    class Config:
        from_attributes = True