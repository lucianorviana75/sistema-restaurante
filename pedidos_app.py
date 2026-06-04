import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"


def main(page: ft.Page):
    page.title = "Painel de Pedidos"
    page.scroll = "auto"

    lista_pedidos = ft.Column()

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

    # 🔄 atualizar pedidos
    def carregar_pedidos(e=None):
        lista_pedidos.controls.clear()

        response = requests.get(f"{API_URL}/pedidos")
        pedidos = response.json()

        for pedido in pedidos:
            itens_lista = []

            for item in pedido["itens"]:
                itens_lista.append(
                    ft.Text(f"{item['nome']} x{item['quantidade']}")
                )

            # botões de status
            def mudar_status(pedido_id, status):
                requests.put(
                    f"{API_URL}/pedidos/{pedido_id}",
                    json={"status": status}
                )
                carregar_pedidos()

            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"Pedido #{pedido['id']}", weight="bold"),
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
                        ])
                    ]),
                    padding=15,
                    bgcolor=cor_status(pedido["status"]),
                    border_radius=10
                )
            )

            lista_pedidos.controls.append(card)

        page.update()

    # botão atualizar
    atualizar_btn = ft.ElevatedButton("Atualizar", on_click=carregar_pedidos)

    page.add(
        ft.Text("📋 Painel de Pedidos", size=30, weight="bold"),
        atualizar_btn,
        lista_pedidos
    )

    carregar_pedidos()


ft.app(target=main)