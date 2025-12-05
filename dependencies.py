from fastapi import Depends , HTTPException
from models import db , Usuario
from sqlalchemy.orm import sessionmaker , Session
from jose import jwt , JWTError
from main import SECRET_KEY , ALGORITHM , oauth2_schema

def pegar_sessao():
    try:
        Sessison = sessionmaker(bind=db)
        session = Sessison()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema) , session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token , SECRET_KEY , ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code = 401 , detail="Acesso negado verifique a validade do roken") # 401 rota existe mais não esta sendo autenticado 
    # verifique token e extrair o id 
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code = 401 , detail = "acesso invalido")
    return usuario