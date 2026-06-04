import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"


def main(page: ft.Page):
    page.title = "Admin Restaurante"

    nome = ft.TextField(label="Nome do item")
    preco = ft.TextField(label="Preço")
    categoria = ft.TextField(label="Categoria")

    lista = ft.Column()

    # ✅ carregar itens
    def carregar(e=None):
        lista.controls.clear()

        try:
            itens = requests.get(f"{API_URL}/itens").json()
        except:
            itens = []

        for item in itens:

            # ✅ pega o id corretamente (IMPORTANTE)
            item_id = item["id"]

            def excluir(e, id=item_id):
                try:
                    requests.delete(f"{API_URL}/itens/{id}")
                except:
                    print("Erro ao deletar")
                carregar()

            linha = ft.Row([
                ft.Text(f"{item['nome']} - R$ {item['preco']}"),
                ft.ElevatedButton("Excluir", on_click=excluir)
            ])

            lista.controls.append(linha)

        page.update()

    # ✅ salvar item
    def salvar(e):
        if not nome.value or not preco.value:
            print("Preencha os campos")
            return

        try:
            requests.post(f"{API_URL}/itens", json={
                "nome": nome.value,
                "preco": float(preco.value),
                "categoriaId": categoria.value
            })
        except:
            print("Erro ao salvar")

        nome.value = ""
        preco.value = ""
        categoria.value = ""

        carregar()

    # ✅ layout
    page.add(
        ft.Text("🛠️ Administração", size=30),

        nome,
        preco,
        categoria,

        ft.ElevatedButton("Adicionar Item", on_click=salvar),

        ft.Divider(),

        ft.Text("Cardápio", size=20),

        ft.ElevatedButton("🔄 Atualizar", on_click=carregar),

        lista
    )

    carregar()


ft.app(target=main)