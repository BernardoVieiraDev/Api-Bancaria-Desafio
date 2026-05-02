from datetime import datetime, timezone

from src.models.model import Conta


CODIGO_DO_BANCO = "720"
AGENCIA = "0001"


def criar_conta(session, usuario_id: int):
    conta = Conta(
        usuario_id=usuario_id,
        saldo=0.0,
        ativo=True,
        numero_conta="",
        data_de_criacao=datetime.now(timezone.utc)
    )

    session.add(conta)
    session.flush()  


    numero_sequencial = str(conta.id).zfill(6)
    numero_conta = f"{CODIGO_DO_BANCO}{AGENCIA}{numero_sequencial}"

    conta.numero_conta = numero_conta # type: ignore

    session.commit()
    session.refresh(conta)

    return conta