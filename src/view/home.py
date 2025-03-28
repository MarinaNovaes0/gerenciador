import flet as ft
from view.tarefa_view import TarefaView

class Home:
    def __init__(self, page: ft.Page):
        self.page = page
    
    def construir(self):
        self.page.clean()
        # Campo de entrada para a descrição da tarefa
        result_text = ft.Text(color="green", weight="bold")
        error_text = ft.Text(value="", color="red", weight="bold")

        def limpar_mensagens(e):
            result_text.value = ""
            error_text.value = ""
            result_text.update()
            error_text.update()

        descricao_input = ft.TextField(
            label="Descrição da Tarefa",
            autofocus=True,
            width=300,
            on_focus=limpar_mensagens,  # Limpa as mensagens ao clicar no campo
            color="green"
        )

        # Instância de TarefaView
        tarefa_view = TarefaView(self.page)
        
        # Botão para adicionar a tarefa
        add_button = ft.Container(
            width=120,
            height=50,  # Define altura menor para tornar o botão retangular
            alignment=ft.alignment.center,
            bgcolor="green",  # Define a cor de fundo do container
            border_radius=ft.border_radius.all(5),  # Adiciona um leve arredondamento
            content=ft.ElevatedButton(
                content=ft.Text("Cadastrar Tarefa", color="white"),
                on_click=lambda e: tarefa_view.on_add_tarefa_click(e, descricao_input, result_text, error_text),
                bgcolor="transparent",  # Torna o botão transparente para usar o fundo do container
                color="white",
                elevation=0  # Remove a elevação para alinhar com o container
            )
        )

        # Adiciona todos os componentes na página
        return ft.Container(
            content=ft.Column(
                [descricao_input, add_button, result_text, error_text],
                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os elementos
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            expand=True,
            alignment=ft.alignment.center
        )

