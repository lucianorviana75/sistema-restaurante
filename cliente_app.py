import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"


def main(page: ft.Page):
    page.title = "Fazer Pedido"

    carrinho = {}
    lista = ft.Column()

    # ✅ Atualizar lista de itens
    def atualizar_view(e=None):
        lista.controls.clear()

        try:
            itens = requests.get(f"{API_URL}/itens").json()
            print("ITENS:", itens)
        except:
            itens = []

        for item in itens:
            if not item["nome"] or not item["preco"]:
                continue
            qtd = carrinho.get(item["id"], 0)

            def aumentar(e, item_id=item["id"]):
                carrinho[item_id] = carrinho.get(item_id, 0) + 1
                atualizar_view()

            def diminuir(e, item_id=item["id"]):
                if carrinho.get(item_id, 0) > 0:
                    carrinho[item_id] -= 1
                atualizar_view()

            lista.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(item["nome"], size=18),
                                ft.Text(f"R$ {item['preco']}"),
                            ]),
                            ft.Row([
                                ft.IconButton(ft.Icons.REMOVE, on_click=diminuir),
                                ft.Text(str(qtd)),
                                ft.IconButton(ft.Icons.ADD, on_click=aumentar),
                            ])
                        ]),
                        padding=10
                    )
                )
            )

        page.update()

    # ✅ Enviar pedido
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

        requests.post(f"{API_URL}/pedidos", json={
            "itens": itens_pedido
        })

        carrinho.clear()
        atualizar_view()

    # ✅ Layout
    page.add(
        ft.Text("🍽️ Fazer Pedido", size=30),

        ft.ElevatedButton(
            "🔄 Atualizar menu",
            on_click=atualizar_view   # 👈 ESSENCIAL
        ),

        lista,

        ft.ElevatedButton(
            "Finalizar Pedido",
            on_click=enviar_pedido
        )
    )

    # ✅ carregar ao abrir
    atualizar_view()


ft.app(target=main)