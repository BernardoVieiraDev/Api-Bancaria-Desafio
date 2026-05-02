from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.model import Conta, Transacao, Usuario
from src.dependencies.dependencies import pegar_session, verificar_token
from src.schemas.schemas import TransacaoCreate
from src.services.account_services import criar_conta
from src.services.transaction_service import validar_transacao, criar_transacao, validar_contas

transaction_router = APIRouter(prefix="/transaction", tags=["transaction"])



@transaction_router.post("/transferencia")
async def transferir(transaction_schema: TransacaoCreate, session: Session = Depends(pegar_session), usuario: Usuario = Depends(verificar_token)):
    conta_origem = session.query(Conta).filter(Conta.usuario_id == usuario.id).first()
    conta_destino = session.query(Conta).filter(Conta.numero_conta==transaction_schema.conta_de_destino_numero).first()

    validar_contas(conta_destino, conta_origem)
    validar_transacao(conta_origem.saldo, transaction_schema.valor)

    conta_origem.saldo -= transaction_schema.valor      # type: ignore
    conta_destino.saldo += transaction_schema.valor     # type: ignore

    # codigo para criar transação, objeto do tipo da classe Transactiom
    nova_transacao = criar_transacao(conta_origem.id, conta_destino.id, transaction_schema.valor)
    session.add(nova_transacao)
    session.commit()

    return {"mensagem": f"Transação efetuada com sucesso. Saldo atual {conta_origem.saldo}"}
