from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from main import ALGORITH, SECRET_KEY, oauth2_schema
from src.models.model import Usuario
from database import db
from jose import jwt, JWTError


def pegar_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_session)):
    try: 
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITH) # type: ignore
        id_usuario = dic_info.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
        ''

    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso invalido")

    return usuario