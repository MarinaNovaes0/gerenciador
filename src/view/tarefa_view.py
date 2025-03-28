import flet as ft
from services.tarefa_service import cadastrar_tarefa, excluir_tarefa, editar_tarefa
from connection import Session
from model.tarefa_model import Tarefa

class TarefaView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.tarefas_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.CENTER)  # Centraliza a coluna
        self.error_text = ft.Text(value="", color="red")  # Adiciona o campo de erro
    
    def construir(self):
        self.page.clean()
        self.tarefas_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.CENTER)  # Centraliza a coluna
        # Adiciona a coluna de tarefas na página
        header = ft.Row(
            [
                ft.Text("Descrição", size=14, weight="bold", text_align="center"),
           ],
           alignment=ft.MainAxisAlignment.CENTER  # Centraliza o cabeçalho
        )
        container = ft.Container(
            content=ft.Column([header, self.tarefas_column], alignment=ft.MainAxisAlignment.CENTER),  # Centraliza o conteúdo
            expand=True,
            alignment=ft.alignment.center
        )
        # Adiciona o container à página antes de atualizar a lista de tarefas
        self.page.add(container)
        # Inicializa a lista de tarefas
        self.atualizar_lista_tarefas(self.tarefas_column)
        
        # Adiciona o botão de excluir no fim da janela
        footer = ft.Row(
            [
                ft.ElevatedButton(
                    "Excluir",
                    on_click=lambda e: self.on_excluir_tarefa_click(e, self.tarefas_column),
                    bgcolor="black",
                    color="white",
                    elevation=2,
                    width=100,
                    height=40
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o botão
            spacing=10
        )
        self.page.add(footer)
        
        return container
    
    def on_add_tarefa_click(self, e, descricao_input, result_text, error_text):
        descricao = descricao_input.value

        if descricao.strip() == "":
            error_text.value = "O campo não pode ser vazio."
            error_text.update()
            if error_text not in self.page.controls:
                self.page.add(error_text)
        else:
            # Chama a função de cadastro da tarefa
            resultado = cadastrar_tarefa(descricao)
            
            if isinstance(resultado, str) and resultado == "Tarefa já existe.":
                error_text.value = "Erro: Tarefa já existe."
                error_text.update()
            elif resultado:
                result_text.value = "Tarefa cadastrada com sucesso!"
                descricao_input.value = ""  # Limpa o campo de texto
                error_text.value = ""  # Limpa a mensagem de erro
            else:
                result_text.value = "Erro ao cadastrar a tarefa."
            
            # Atualiza o texto na tela
            result_text.update()
            descricao_input.update()  # Atualiza o campo de texto
            error_text.update()  # Atualiza a mensagem de erro
    
    def atualizar_lista_tarefas(self, tarefas_column):
        # Função para atualizar a lista de tarefas
        session = Session()
        
        try:
            # Limpa a coluna de tarefas
            tarefas_column.controls.clear()

            # Busca todas as tarefas no banco de dados
            todas_tarefas = session.query(Tarefa).all()

            # Adiciona cada tarefa à coluna de tarefas
            for tarefa in todas_tarefas:
                tarefa_row = ft.Row(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(f"{tarefa.descricao}", size=12, text_align="center"),
                                        on_click=lambda e, t=tarefa: self.abrir_edicao_tarefa(e, t)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER  # Centraliza o texto da tarefa
                            ),
                            padding=ft.padding.all(10),
                            border=ft.border.all(1, "white"),  # Muda a cor da borda para branco
                            border_radius=ft.border_radius.all(5),
                            alignment=ft.alignment.center,
                            width=300  # Define a largura da caixa
                        ),
                        ft.Checkbox(value=False, data=tarefa.id)  # Adiciona a checkbox fora da caixinha com o ID da tarefa
                    ],
                    alignment=ft.MainAxisAlignment.CENTER  # Centraliza a linha da tarefa
                )
                tarefas_column.controls.append(tarefa_row)

            # Atualiza a tela com as novas tarefas
            tarefas_column.update()

        finally:
            # Fechar a sessão após o processo
            session.close()

    def abrir_edicao_tarefa(self, e, tarefa):
        descricao_input = ft.TextField(value=tarefa.descricao, expand=True)
        error_text = ft.Text(value="", color="red")

        def salvar_edicao(e):
            if descricao_input.value.strip() == "":
                error_text.value = "O campo não pode ser vazio."
                error_text.update()
            else:
                # Chama a função de edição da tarefa
                resultado = editar_tarefa(tarefa.id, descricao_input.value)
                
                if isinstance(resultado, str) and resultado == "Tarefa já existe.":
                    error_text.value = "Erro: Tarefa já existe."
                    error_text.update()
                else:
                    self.atualizar_lista_tarefas(self.tarefas_column)
        
        def cancelar_edicao(e):
            self.atualizar_lista_tarefas(self.tarefas_column)
        
        tarefa_row = e.control.parent
        tarefa_row.controls.clear()  # Limpa os controles para adicionar os novos
        tarefa_row.controls.append(
            ft.Column(
                [
                    descricao_input,
                    error_text,
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                                icon_color=ft.Colors.GREEN,
                                tooltip="Concluir Edição",
                                on_click=salvar_edicao
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CANCEL_OUTLINED,
                                icon_color=ft.Colors.RED,
                                tooltip="Cancelar Edição",
                                on_click=cancelar_edicao
                            )
                        ]
                    )
                ]
            )
        )
        tarefa_row.update()

    def on_excluir_tarefa_click(self, e, tarefas_column):
        # Coleta todas as tarefas marcadas
        tarefas_marcadas = [control.controls[1].data for control in tarefas_column.controls if isinstance(control.controls[1], ft.Checkbox) and control.controls[1].value]
        
        if tarefas_marcadas:
            # Exclui as tarefas selecionadas
            for tarefa_id in tarefas_marcadas:
                excluir_tarefa(tarefa_id)
            self.atualizar_lista_tarefas(tarefas_column)
        else:
            # Criação do pop-up de erro
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Erro", color="red"),
                content=ft.Text("Nenhuma tarefa selecionada. Por favor, selecione pelo menos uma tarefa para excluir."),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: self.fechar_dialog(dialog))  # Chama o método de fechamento
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            # Abre o diálogo
            self.page.open(dialog)

    def fechar_dialog(self, dialog):
        # Fecha o diálogo definindo o 'open' como False
        dialog.open = False
        self.page.update()  # Atualiza a página para garantir que os controles voltem a funcionar
