from sqlalchemy import create_engine , Column , String , Integer , Boolean , Float , ForeignKey
from sqlalchemy.orm import declarative_base , relationship
from sqlalchemy_utils.types import ChoiceType

#conexão com banco 
db = create_engine("sqlite:///banco.db") #minha sessão 

#base de banco
Base = declarative_base()

#classes do banco
class Usuario(Base):
    __tablename__ = "Usuarios"

    id = Column("id" ,Integer,primary_key=True , autoincrement=True)
    nome = Column("nome" , String)
    email = Column("email", String , nullable=False)
    senha = Column("senha" , String)
    ativo = Column("ativo" , Boolean)
    admin = Column("admin" , Boolean , default=False)

    def __init__(self , nome , email , senha , ativo=True , admin=False): #os parametros que quero passar para meu usuario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

#pedidos
class Pedido(Base):
    __tablename__ = "pedidos"

    #STATUS_PEDIDO = (
    #   ("PENDENTE" , "PENDETE"),
     #   ("CANCELADO" , "CANCELADO"),
      #  ("FINALIZADO" , "FINALIZADO")
    #)

    id = Column("id" ,Integer,primary_key=True , autoincrement=True)
    status = Column("status" , String) #pedente #cancelado #concluido 
    usuario = Column("usuario", ForeignKey("Usuarios.id")) #chave estrangeira a foreignKey
    preco =Column("preco" , Float)
    itens = relationship("ItemPedido", cascade="all , delete")#to criando uma relação de 2 tabelas mais nao dependecia uma caminho contrario da chave estrangeira 

    # itens = 
    def __init__(self , usuario ,status="PEDENTE" , preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

    def calcular_preco(self):
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)


class ItemPedido(Base):
    __tablename__ = "itens_pedidos"

    id = Column("id" ,Integer,primary_key=True , autoincrement=True)
    quantidade = Column("quatidade" , Integer)
    sabor = Column("sabor" , String)
    tamanho = Column("tamanho" , String)
    preco_unitario = Column("preco_unitario" , Float) 
    pedido = Column("pedido" , ForeignKey("pedidos.id"))

    def __init__(self , quantidade , sabor , tamanho , preco_unitario , pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido


#criar a migração no banco de dados: alembic revision --autogenerate -m "alterar repr Pedidos"
#executa a migração : alembic upgrade head
