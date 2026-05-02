from datetime import datetime, timezone

from fastapi import HTTPException

from src.models.model import Conta, Transacao


def validar_transacao(saldo_em_conta, quantia_para_transferir):

    if 0 >= quantia_para_transferir:
        raise HTTPException(status_code=400, detail="Quantia igual ou menor que zero.")

    if saldo_em_conta < quantia_para_transferir:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    
def validar_contas(conta_de_destino: Conta, conta_de_origem: Conta):

    if not conta_de_origem:
        raise HTTPException(status_code=400, detail="Conta de origem não existe")
    
    if not conta_de_destino:
        raise HTTPException(status_code=400, detail="Conta de destino não existe")
    
    if conta_de_destino.id == conta_de_origem.id:  # type: ignore
        raise HTTPException(status_code=400, detail="Não é possivel transferir para a propria conta.")


    

def criar_transacao(conta_origem_id, conta_destino_id, valor):
    nova_transacao = Transacao(datetime.now(timezone.utc), conta_origem_id, conta_destino_id, valor)
    return nova_transacao
