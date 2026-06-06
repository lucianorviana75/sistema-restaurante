import flet as ft
import requests

API_URL = "http://127.0.0.1:8000"


def main(page: ft.Page):
    page.title = "Admin Restaurante"

    nome = ft.TextField(label="Nome do item")
    preco = ft.TextField(label="Preço")

    # ✅ dropdown de categorias (melhor que TextField)
    dropdown_categoria = ft.Dropdown(label="Categoria")

    lista = ft.Column()

    # ✅ carregar categorias no dropdown
    def carregar_categorias():
        dropdown_categoria.options.clear()

        try:
            categorias = requests.get(f"{API_URL}/categorias").json()
        except:
            categorias = []

        for cat in categorias:
            dropdown_categoria.options.append(
                ft.dropdown.Option(cat["id"], cat["nome"])
            )

        page.update()

    # ✅ carregar itens
    def carregar(e=None):
        lista.controls.clear()

        try:
            itens = requests.get(f"{API_URL}/itens").json()
        except:
            itens = []

        for item in itens:

            item_id = item["id"]

            def excluir(e, id=item_id):
                requests.delete(f"{API_URL}/itens/{id}")
                carregar()

            linha = ft.Row([
                ft.Text(f"{item['nome']} - R$ {item['preco']}"),
                ft.ElevatedButton("Excluir", on_click=excluir)
            ])

            lista.controls.append(linha)

        page.update()

    # ✅ salvar item
    def salvar(e):
        if not nome.value or not preco.value or not dropdown_categoria.value:
            print("Preencha os campos")
            return

        requests.post(f"{API_URL}/itens", json={
            "nome": nome.value,
            "preco": float(preco.value),
            "categoriaId": dropdown_categoria.value
        })

        nome.value = ""
        preco.value = ""
        dropdown_categoria.value = None

        carregar()

    # ✅ layout
    page.add(
        ft.Text("🛠️ Administração", size=30),

        nome,
        preco,
        dropdown_categoria,  # ✅ aqui entra categoria

        ft.ElevatedButton("Adicionar Item", on_click=salvar),

        ft.Divider(),

        ft.Text("Cardápio", size=20),

        ft.ElevatedButton("🔄 Atualizar", on_click=carregar),

        lista
    )

    carregar_categorias()
    carregar()


ft.app(target=main)