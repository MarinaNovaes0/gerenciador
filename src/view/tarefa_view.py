import flet as ft
from services.tarefa_service import cadastrar_tarefa, excluir_tarefa, editar_tarefa
from connection import Session
from model.tarefa_model import Tarefa

class TarefaView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.decoration = ft.BoxDecoration(image=ft.DecorationImage("assets/img/Hero.png"))
        self.tarefas_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.CENTER)  # Centraliza a coluna
        self.error_text = ft.Text(value="", color="red")  # Adiciona o campo de erro
    
    def construir(self):
        self.page.clean()
        self.page.decoration = ft.BoxDecoration(image=ft.DecorationImage("assets/img/Hero.png"))
        self.tarefas_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, alignment=ft.MainAxisAlignment.CENTER)  # Centraliza a coluna
        # Adiciona a coluna de tarefas na página
        header = ft.Row(
            [
                ft.Text("Descrição", size=14, weight="bold", text_align="center", color="green"),
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
                ft.Container(
                    width=120,
                    height=50,  # Define altura menor para tornar o botão retangular
                    alignment=ft.alignment.center,
                    bgcolor="green",  # Define a cor de fundo do container
                    border_radius=ft.border_radius.all(5),  # Adiciona um leve arredondamento
                    content=ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Text("X", font_family="Mine 2", size=20),  # Ícone com fonte "Mine 2"
                                ft.Text("Excluir", font_family="Mine", size=14)  # Texto com fonte "Mine"
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5
                        ),
                        on_click=lambda e: self.on_excluir_tarefa_click(e, self.tarefas_column),
                        bgcolor="transparent",  # Torna o botão transparente para usar o fundo do container
                        color="white",
                        elevation=0  # Remove a elevação para alinhar com o container
                    )
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
            error_text.value = "O CAMPO NÃO PODE SER VAZIO."
            error_text.weight = "bold"
            error_text.update()
            if error_text not in self.page.controls:
                self.page.add(error_text)
        else:
            # Chama a função de cadastro da tarefa
            resultado = cadastrar_tarefa(descricao)
            
            if isinstance(resultado, str) and resultado == "Tarefa já existe.":
                error_text.value = "ERRO: TAREFA JÁ EXISTE."
                error_text.weight = "bold"
                error_text.update()
            elif resultado:
                result_text.value = "TAREFA CADASTRADA COM SUCESSO!"
                result_text.weight = "bold"
                descricao_input.value = ""  # Limpa o campo de texto
                error_text.value = ""  # Limpa a mensagem de erro
            else:
                result_text.value = "ERRO AO CADASTRAR A TAREFA."
                result_text.weight = "bold"
            
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
                                        content=ft.Text(f"{tarefa.descricao}", size=14, text_align="center", color="gray"),  # Aumenta o tamanho do texto
                                        on_click=lambda e, t=tarefa: self.abrir_edicao_tarefa(e, t)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER  # Centraliza o texto da tarefa
                            ),
                            padding=ft.padding.all(5),  # Diminui o padding para reduzir o tamanho do quadrado
                            border=ft.border.all(1, "gray"),  # Muda a cor da borda para cinza
                            border_radius=ft.border_radius.all(5),
                            alignment=ft.alignment.center,
                            width=280  # Diminui a largura da caixa
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
        descricao_input = ft.TextField(
            value=tarefa.descricao,
            expand=False,  # Remove o comportamento de expansão para alinhar melhor
            color="green",
            text_align="start",  # Alinha o texto à esquerda
            autofocus=True,  # Foca automaticamente no campo ao editar
            multiline=True,  # Permite múltiplas linhas
            max_lines=None,  # Sem limite de linhas
            min_lines=1,  # Garante pelo menos uma linha visível
            width=280,  # Define a largura para alinhar com a caixa da lista
            height=50,  # Define uma altura fixa para alinhar com o design
        )
        error_text = ft.Text(value="", color="red", weight="bold")  # Garante que o texto de erro seja exibido

        def salvar_edicao(e):
            if descricao_input.value.strip() == "":
                error_text.value = "O CAMPO NÃO PODE SER VAZIO."
                error_text.update()  # Atualiza o texto de erro na tela
            else:
                # Chama a função de edição da tarefa
                resultado = editar_tarefa(tarefa.id, descricao_input.value)
                
                if isinstance(resultado, str) and resultado == "Tarefa já existe.":
                    error_text.value = "ERRO: TAREFA JÁ EXISTE."
                    error_text.update()  # Atualiza o texto de erro na tela
                elif "editada com sucesso" in resultado:
                    self.atualizar_lista_tarefas(self.tarefas_column)
                else:
                    error_text.value = resultado  # Exibe qualquer outro erro retornado
                    error_text.update()

        def cancelar_edicao(e):
            self.atualizar_lista_tarefas(self.tarefas_column)
        
        tarefa_row = e.control.parent
        tarefa_row.controls.clear()  # Limpa os controles para adicionar os novos
        tarefa_row.controls.append(
            ft.Column(
                [
                    descricao_input,
                    error_text,  # Adiciona o texto de erro abaixo do campo de entrada
                    ft.Row(
                        [
                            ft.Container(
                                width=100,
                                height=40,  # Define altura menor para tornar o botão mais compacto
                                alignment=ft.alignment.center,
                                bgcolor="green",  # Define a cor de fundo do container
                                border_radius=ft.border_radius.all(5),  # Adiciona um leve arredondamento
                                content=ft.ElevatedButton(
                                    content=ft.Text("Salvar", font_family="Mine 2", size=12),  # Ícone de edição
                                    bgcolor="transparent",  # Torna o botão transparente para usar o fundo do container
                                    color="white",
                                    elevation=0,  # Remove a elevação para alinhar com o container
                                    on_click=salvar_edicao  # Chama a função de salvar
                                )
                            ),
                            ft.Container(
                                width=100,
                                height=40,  # Define altura menor para tornar o botão mais compacto
                                alignment=ft.alignment.center,
                                bgcolor="red",  # Define a cor de fundo do container
                                border_radius=ft.border_radius.all(5),  # Adiciona um leve arredondamento
                                content=ft.ElevatedButton(
                                    content=ft.Text("Cancelar", font_family="Mine", size=12),  # Ícone de cancelar
                                    bgcolor="transparent",  # Torna o botão transparente para usar o fundo do container
                                    color="white",
                                    elevation=0,  # Remove a elevação para alinhar com o container
                                    on_click=cancelar_edicao  # Chama a função de cancelar
                                )
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
            def confirmar_exclusao(e):
                # Exclui as tarefas selecionadas
                for tarefa_id in tarefas_marcadas:
                    excluir_tarefa(tarefa_id)
                self.atualizar_lista_tarefas(tarefas_column)
                dialog.open = False
                self.page.update()

            def cancelar_exclusao(e):
                dialog.open = False
                self.page.update()

            # Criação do pop-up de confirmação
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("CONFIRMAR EXCLUSÃO", color="red", weight="bold"),
                content=ft.Text("VOCÊ TEM CERTEZA QUE DESEJA EXCLUIR AS TAREFAS SELECIONADAS?", weight="bold"),
                actions=[
                    ft.TextButton("SIM", on_click=confirmar_exclusao),
                    ft.TextButton("NÃO", on_click=cancelar_exclusao)
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            # Abre o diálogo
            self.page.open(dialog)
        else:
            # Criação do pop-up de erro
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("ERRO", color="red", weight="bold"),
                content=ft.Text("NENHUMA TAREFA SELECIONADA. POR FAVOR, SELECIONE PELO MENOS UMA TAREFA PARA EXCLUIR.", weight="bold"),
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
