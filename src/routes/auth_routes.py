from fastapi import APIRouter, Depends, HTTPException
from src.dependencies.dependencies import pegar_session, verificar_token
from src.models.model import Usuario
from main import bcrypt_context, ALGORITH, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from src.schemas.schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now() + duracao_token
    dict_info = {"sub": str(id_usuario), "exp_date": data_expiracao.timestamp()}
    jwt_codificado = jwt.encode(dict_info, SECRET_KEY, ALGORITH) # type: ignore

    return jwt_codificado

def autenticar_usuario(cpf, senha, session):
    usuario = session.query(Usuario).filter(Usuario.cpf==cpf).first()  # type: ignore
    if not usuario:
        return False
    
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False

    return usuario

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
def home():

    return {
        "Mensagem": "Você acessou a rota padrão de autenticação",
        "Autenticado": "Não"
            }

@auth_router.post("/criar-conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_session)):

    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()  # type: ignore
    if usuario:
        raise HTTPException(status_code=400, detail="Já existe um usuario com esse email")
    usuario = session.query(Usuario).filter(Usuario.cpf==usuario_schema.cpf).first()  # type: ignore
    if usuario:
        raise HTTPException(status_code=400, detail="Já existe um usuario com esse CPF")


    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)

        novo_usuario = Usuario(
            usuario_schema.nome, 
            usuario_schema.email, 
            usuario_schema.cpf,
            senha_criptografada, 
            usuario_schema.ativo if usuario_schema.ativo is not None else True, 
            )
        
    try:
        session.add(novo_usuario)
        session.commit()
        session.refresh(novo_usuario)

        usuarios = session.query(Usuario).all()

        return {
            "mensagem": "usuario cadastrado",
            "usuario_id": novo_usuario.id,
            "total_usuarios": len(usuarios)
        }

    except Exception as e:
        session.rollback()
        print("ERRO:", e)
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.post("/login")
async def login(login_schemma: LoginSchema, session: Session = Depends(pegar_session)):
    usuario = autenticar_usuario(login_schemma.cpf, login_schemma.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail=f"Usuario ou credenciais invalidas")
    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
        }
    
    
@auth_router.get("/refresh")
async def user_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
        }


@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_session)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail=f"Usuario ou credenciais invalidas")
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
        }
    