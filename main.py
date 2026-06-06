from fastapi import FastAPI
from datetime import datetime
import json
import os
from pydantic import BaseModel
import time

app = FastAPI()

ARQUIVO = "dados.json"


# ✅ MODELOS (IMPORTANTE)
class Categoria(BaseModel):
    nome: str


class Item(BaseModel):
    nome: str
    preco: float
    categoriaId: str


# ✅ Carregar dados
def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return {"categorias": [], "itens": [], "pedidos": []}

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


# ✅ Salvar dados
def salvar_dados():
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump({
            "categorias": categorias,
            "itens": itens,
            "pedidos": pedidos
        }, f, indent=4, ensure_ascii=False)

    print("✅ Dados salvos!")


# ✅ carregar ao iniciar
dados = carregar_dados()
categorias = dados.get("categorias", [])
itens = dados.get("itens", [])
pedidos = dados.get("pedidos", [])


@app.get("/")
def home():
    return {"msg": "API Restaurante funcionando"}


# =========================
# ✅ CATEGORIAS
# =========================

@app.post("/categorias")
def criar_categoria(body: Categoria):
    categoria = {
        "id": str(time.time()),
        "nome": body.nome,
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
def criar_item(body: Item):
    item = {
        "id": str(time.time()),
        "nome": body.nome,
        "preco": body.preco,
        "categoriaId": body.categoriaId
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
        item_encontrado = next(
            (i for i in itens if i["id"] == item["itemId"]), None
        )

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
        "data": datetime.now().isoformat()
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


@app.delete("/pedidos/{id}")
def deletar_pedido(id: str):
    global pedidos

    pedidos = [p for p in pedidos if p["id"] != id]
    salvar_dados()

    return {"msg": "Pedido removido"}


# =========================
# ✅ PDF
# =========================
from reportlab.pdfgen import canvas


@app.get("/pedidos/pdf/{data}")
def gerar_pdf(data: str):
    nome_arquivo = f"pedidos_{data}.pdf"
    c = canvas.Canvas(nome_arquivo)

    y = 800

    for p in pedidos:
        if data in p["data"]:

            if y < 50:
                c.showPage()
                y = 800

            c.drawString(50, y, f"Pedido {p['id']} - Total R$ {p['total']}")
            y -= 20

            for item in p["itens"]:
                c.drawString(
                    70, y,
                    f"{item['nome']} x{item['quantidade']}"
                )
                y -= 20

            y -= 10

    c.save()

    return {"msg": f"PDF gerado: {nome_arquivo}"}
import time
