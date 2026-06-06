import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"


def main(page: ft.Page):
    page.title = "Fazer Pedido"
    page.expand = True

    carrinho = {}
    lista = ft.ListView(expand=True, spacing=10)

    # ✅ FUNÇÕES FORA DO LOOP (CORRETO)
    def aumentar(item_id):
        carrinho[item_id] = carrinho.get(item_id, 0) + 1
        atualizar_view()

    def diminuir(item_id):
        if carrinho.get(item_id, 0) > 0:
            carrinho[item_id] -= 1
        atualizar_view()

    def atualizar_view(e=None):
        lista.controls.clear()

        try:
            categorias = requests.get(f"{API_URL}/categorias").json()
            itens = requests.get(f"{API_URL}/itens").json()
        except:
            categorias = []
            itens = []

        categorias_completa = categorias.copy()
        categorias_completa.append({"id": None, "nome": "Outros"})

        for cat in categorias_completa:

            lista.controls.append(
                ft.Text(f"🍽️ {cat['nome']}", size=20, weight="bold")
            )

            for item in itens:
                if item.get("categoriaId") == cat["id"]:

                    qtd = carrinho.get(item["id"], 0)

                    lista.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.Row([
                                    ft.Column([
                                        ft.Text(item["nome"], size=16),
                                        ft.Text(f"R$ {item['preco']}", color="green"),
                                    ]),

                                    ft.Row([
                                        ft.IconButton(
                                            ft.Icons.REMOVE,
                                            on_click=lambda e, id=item["id"]: diminuir(id)
                                        ),
                                        ft.Text(str(qtd)),
                                        ft.IconButton(
                                            ft.Icons.ADD,
                                            on_click=lambda e, id=item["id"]: aumentar(id)
                                        ),
                                    ])
                                ], alignment="spaceBetween"),
                                padding=10
                            )
                        )
                    )

        page.update()

    def enviar_pedido(e):
        itens_pedido = []

        for item_id, qtd in carrinho.items():
            if qtd > 0:
                itens_pedido.append({
                    "itemId": item_id,
                    "quantidade": qtd
                })

        if not itens_pedido:
            print("Nenhum item no pedido")
            return

        requests.post(f"{API_URL}/pedidos", json={"itens": itens_pedido})

        carrinho.clear()
        atualizar_view()

    page.add(
        ft.Column([
            ft.Text("🍽️ Fazer Pedido", size=30),

            ft.ElevatedButton(
                "🔄 Atualizar menu",
                on_click=atualizar_view
            ),

            lista,

            ft.ElevatedButton(
                "Finalizar Pedido",
                on_click=enviar_pedido
            )
        ], expand=True)
    )

    atualizar_view()


ft.app(target=main)


def main(page: ft.Page):
    page.title = "Fazer Pedido"
    page.expand = True

