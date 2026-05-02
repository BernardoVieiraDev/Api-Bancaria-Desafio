from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.model import Conta, Usuario
from src.dependencies.dependencies import pegar_session, verificar_token
from src.services.account_services import criar_conta

account_router = APIRouter(prefix="/account", tags=["account"])



@account_router.post("/criar-conta-corrente")
async def criar_conta_corrente(session: Session = Depends(pegar_session), usuario: Usuario = Depends(verificar_token)):
    nova_conta = criar_conta(session, usuario.id) # type: ignore
    return {"mensagem": f"Conta criado com sucesso. Número da conta {nova_conta.numero_conta}"}


@account_router.get("/consultar-saldo")
async def consultar_saldo(session: Session = Depends(pegar_session), usuario: Usuario = Depends(verificar_token)):
    conta = session.query(Conta).filter(Conta.usuario_id == usuario.id).first()
    if not conta:
        raise HTTPException(status_code=400, detail="Conta não existe")
    return {"mensagem": f"Saldo atual {conta.saldo}"}

