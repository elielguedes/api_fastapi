from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao , verificar_token
from schemas import PedidoSchemas , ItemPedidoSchema , ResponsePedidoSchema
from models import Pedido , Usuario , ItemPedido
from typing import List #lista de schema de pedidos

order_router = APIRouter(prefix="/pedidos" , tags=['pedidos'] ,  dependencies = [Depends(verificar_token)])

@order_router.get("/home")
async def pedidos():
    return {"mensagem":"Você acessou a rota de pedidos"}

@order_router.post("/pedidos")
async def criar_pedido(pedido_schema:PedidoSchemas , session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario = pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem":f"pedido criado com seucceso .ID do pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/id_pedido")
async def cancelar_pedido(id_pedido: int , session: Session= Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    # usuario admin = True
    # usuario.id = pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code = 400 , detail="pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code = 401 , detail="Voce nao tem autorização para essa modificação")
    pedido.status = "CANCELADO"
    session.commit()
    return {
            "mensagem": f"Pedido número {id_pedido} cancelado com sucesso",
            "pedido":pedido
        }

@order_router.get("/listar")
async def listar_pedidos(session: Session= Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code = 401 , detail="Voce nao tem autorização para essa modificação")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos":pedidos
        }

@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido , item_pedido: ItemPedidoSchema , session:Session = Depends(pegar_sessao) , usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code = 400 ,detail="pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code = 401 , detail = "voce não tem autorização paea fazer essa operação") 
    item_pedido = ItemPedido(item_pedido.quantidade , item_pedido.sabor , item_pedido.tamanho , item_pedido.preco_unitario, id_pedido)
    pedido.calcular_preco()
    session.add(item_pedido)
    session.commit()
    return {
        "mensagem":"Item criado com sucesso",
        "item_id":item_pedido.id,
        "preco_pedido":pedido.preco
    }

@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido , item_pedido: ItemPedidoSchema , session:Session = Depends(pegar_sessao) , usuario: Usuario = Depends(verificar_token)):
    item_pedido_obj = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    if not item_pedido_obj:
        raise HTTPException(status_code = 400 ,detail="item do pedido não existente")
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido_obj.pedido_id).first()
    if not pedido:
        raise HTTPException(status_code = 400 ,detail="pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code = 401 , detail = "voce não tem autorização paea fazer essa operação") 
    session.delete(item_pedido_obj)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem":"Item removido com sucesso",
        "quatidade_itens_pedido":len(pedido.itens),
        "pedido":pedido.id
    }

@order_router.post("/pedido/finalizar/id_pedido")
async def finalizar_pedido(id_pedido: int , session: Session= Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    # usuario admin = True
    # usuario.id = pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code = 400 , detail="pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code = 401 , detail="Voce nao tem autorização para essa modificação")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
            "mensagem": f"Pedido número {id_pedido} finalizado com sucesso",
            "pedido":pedido
        }

 
#vizualizar pedido
@order_router.get("/pedido/{id_pedido}")
async def vizualizar_pedido(id_pedido: int , session:Session = Depends(pegar_sessao), usuario:Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code = 400 , detail="pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code = 401 , detail="Voce nao tem autorização para essa modificação")
    return {
        "quantidade_itens_pedido":len(pedido.itens),
        "pedido":pedido
    }

#vizualizar pedidos de usuario
@order_router.get("/listar/pedidos-usuario", response_model = List[ResponsePedidoSchema])
async def listar_pedidos(session: Session= Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
        pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
        return pedidos