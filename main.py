from fastapi import FastAPI
import time
from datetime import datetime
import json
import os

app = FastAPI()

ARQUIVO = "dados.json"


# ✅ Carregar dados
def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return {"categorias": [], "itens": [], "pedidos": []}

    with open(ARQUIVO, "r") as f:
        return json.load(f)


# ✅ Salvar dados
def salvar_dados():
    with open(ARQUIVO, "w") as f:
        json.dump({
            "categorias": categorias,
            "itens": itens,
            "pedidos": pedidos
        }, f, indent=4)


# ✅ carregar ao iniciar
dados = carregar_dados()

categorias = dados["categorias"]
itens = dados["itens"]
pedidos = dados["pedidos"]


@app.get("/")
def home():
    return {"msg": "API Restaurante funcionando"}


# =========================
# ✅ CATEGORIAS
# =========================
@app.post("/categorias")
def criar_categoria(body: dict):
    categoria = {
        "id": str(time.time()),
        "nome": body.get("nome"),
        "ativo": True
    }

    categorias.append(categoria)
    salvar_dados()
    return categoria


@app.get("/categorias")
def listar_categorias():
    return categorias


# =========================
# ✅ ITENS
# =========================
@app.post("/itens")
def criar_item(body: dict):
    item = {
        "id": str(time.time()),
        "nome": body.get("nome"),
        "preco": body.get("preco"),
        "categoriaId": body.get("categoriaId")
    }

    itens.append(item)
    salvar_dados()
    return item


@app.get("/itens")
def listar_itens():
    return itens


@app.delete("/itens/{id}")
def deletar_item(id: str):
    global itens
    itens = [item for item in itens if item["id"] != id]

    salvar_dados()
    return {"msg": "Item removido"}


# =========================
# ✅ PEDIDOS
# =========================

@app.post("/pedidos")
def criar_pedido(body: dict):

    lista_itens = body.get("itens", [])

    itens_pedido = []
    total = 0

    for item in lista_itens:
        item_encontrado = next((i for i in itens if i["id"] == item["itemId"]), None)

        if item_encontrado:
            subtotal = item_encontrado["preco"] * item["quantidade"]

            itens_pedido.append({
                "itemId": item_encontrado["id"],
                "nome": item_encontrado["nome"],
                "quantidade": item["quantidade"],
                "preco": item_encontrado["preco"],
                "subtotal": subtotal
            })

            total += subtotal

    pedido = {
        "id": str(time.time()),
        "itens": itens_pedido,
        "total": total,
        "status": "pendente",
        "data": str(datetime.now())
    }

    pedidos.append(pedido)
    salvar_dados()

    return pedido


@app.get("/pedidos")
def listar_pedidos():
    return pedidos


@app.put("/pedidos/{id}")
def atualizar_pedido(id: str, body: dict):
    for p in pedidos:
        if p["id"] == id:
            p["status"] = body.get("status", p["status"])
            salvar_dados()
            return p

    return {"erro": "pedido não encontrado"}