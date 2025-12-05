from pydantic import BaseModel
from typing import Optional , List#importar tipo de dados

class usuario_schema(BaseModel): #tranformado em dicionario em python
    email:str
    nome:str
    senha:str
    ativo:Optional[bool]
    admin:Optional[bool]

    class config:
        from_attributes = True #impede que isso se torna um dicionario

class PedidoSchemas(BaseModel):
    usuario:int

    class config:
        from_attributes = True

class loguinschema(BaseModel):
    email:str
    senha:str

    class config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade:int
    sabor:str
    tamanho:str 
    preco_unitario:float

    class config:
        from_attributes = True

#padrão de resposta 
class ResponsePedidoSchema(BaseModel):
    id:int
    status:str
    preco:float
    itens:List[ItemPedidoSchema]

    class config:
        from_attributes = True


            
#são as entradas aonde se usa a estrutura do pydantic para criar as nossas classes de entrada