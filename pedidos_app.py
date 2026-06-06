import flet as ft
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"


def main(page: ft.Page):
    page.title = "Painel de Pedidos"

    # ✅ lista com rolagem garantida
    lista_pedidos = ft.ListView(expand=True, spacing=10)

    # 🎨 cores por status
    def cor_status(status):
        if status == "pendente":
            return "yellow"
        elif status == "preparando":
            return "lightblue"
        elif status == "pronto":
            return "lightgreen"
        else:
            return "white"

    # ✅ deletar pedido
    def deletar(pedido_id):
        requests.delete(f"{API_URL}/pedidos/{pedido_id}")
        carregar_pedidos()

    # 🔄 atualizar pedidos
    def carregar_pedidos(e=None):
        lista_pedidos.controls.clear()

        try:
            pedidos = requests.get(f"{API_URL}/pedidos").json()
        except:
            pedidos = []

        for pedido in pedidos:

            itens_lista = [
                ft.Text(f"{i['nome']} x{i['quantidade']}")
                for i in pedido["itens"]
            ]

            # ✅ data segura
            try:
                data = datetime.fromisoformat(pedido["data"]).strftime("%d/%m %H:%M")
            except:
                data = "sem data"

            def mudar_status(id, status):
                requests.put(
                    f"{API_URL}/pedidos/{id}",
                    json={"status": status}
                )
                carregar_pedidos()

            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"Pedido #{pedido['id']}", weight="bold"),
                        ft.Text(f"🕒 {data}", size=12),
                        ft.Text(f"Status: {pedido['status']}"),
                        ft.Text(f"Total: R$ {pedido['total']}"),

                        ft.Column(itens_lista),

                        ft.Row([
                            ft.ElevatedButton(
                                "Preparando",
                                on_click=lambda e, id=pedido["id"]: mudar_status(id, "preparando")
                            ),
                            ft.ElevatedButton(
                                "Pronto",
                                on_click=lambda e, id=pedido["id"]: mudar_status(id, "pronto")
                            ),
                            ft.ElevatedButton(
                                "Entregue",
                                on_click=lambda e, id=pedido["id"]: mudar_status(id, "entregue")
                            ),
                            ft.ElevatedButton(
                                "Excluir",
                                bgcolor="red",
                                color="white",
                                on_click=lambda e, id=pedido["id"]: deletar(id)
                            ),
                        ])
                    ]),
                    padding=10,
                    bgcolor=cor_status(pedido["status"]),
                    border_radius=10
                )
            )

            lista_pedidos.controls.append(card)

        page.update()

    # ✅ layout correto
    page.add(
        ft.Column([
            ft.Text("📋 Painel de Pedidos", size=30),
            ft.ElevatedButton("Atualizar", on_click=carregar_pedidos),
            lista_pedidos
        ], expand=True)
    )

    carregar_pedidos()


ft.app(target=main)