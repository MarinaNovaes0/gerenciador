import flet as ft
from services.tarefa_service import cadastrar_tarefa, excluir_tarefa, editar_tarefa
from connection import Session
from model.tarefa_model import Tarefa

class TarefaView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.image_src = "src/assets/img/fundo.png"
        self.page.image_fit = ft.ImageFit.COVER
        
        # Configuração da lista de tarefas com rolagem
        self.tarefas_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=False,
            width=400  # Largura fixa para centralização
        )
        
        self.error_text = ft.Text(value="", color="red")
        self.editing_task_id = None
    
    def construir(self):
        self.page.clean()
        self.page.padding = 0
        self.page.spacing = 0
        
        # Elementos da UI
        background_image = ft.Image(
            src="https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/f2/Dirt_background_BE1.png/revision/latest?cb=20210820093527",
            fit=ft.ImageFit.COVER,
            expand=True
        )
        
        header = ft.Row(
            [ft.Text("Descrição", size=14, weight="bold", text_align="center", color="white")],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        # Substitui o Container por um Column para suportar o atributo controls
        main_content = ft.Column(
            controls=[
                header,
                ft.Container(
                    content=self.tarefas_list,
                    height=self.page.height * 0.7,  # 70% da altura da página
                    alignment=ft.alignment.center,
                    margin=ft.margin.symmetric(horizontal=20),  # Margem nas laterais
                    border_radius=10,
                    padding=10
                ),
                self._create_footer()
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza horizontalmente
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        # Adiciona o main_content à página antes de atualizar a lista
        self.page.controls.clear()
        self.page.add(main_content)  # Certifique-se de adicionar o controle à página
        self.page.update()  # Atualiza a página para refletir as mudanças

        # Atualiza a lista de tarefas após adicionar o main_content
        self.atualizar_lista_tarefas()

        return ft.Stack([background_image, main_content])
    
    def _create_footer(self):
        """Cria o rodapé centralizado com o botão de excluir"""
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        width=120,
                        height=50,
                        alignment=ft.alignment.center,
                        bgcolor="#6E6E6E",
                        border=ft.border.all(1, "#5C5C5C"),
                        border_radius=ft.border_radius.all(5),
                        shadow=ft.BoxShadow(blur_radius=5, color="black", spread_radius=1),
                        content=ft.ElevatedButton(
                            content=ft.Row(
                                [
                                    ft.Text("X", font_family="Mine 2", size=20, color="white"),
                                    ft.Text("Excluir", font_family="Mine", size=14, color="white")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=5
                            ),
                            on_click=self.on_excluir_tarefa_click,  # Corrige o evento do botão
                            bgcolor="transparent",
                            color="white",
                            elevation=0
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=ft.padding.only(top=20)  # Espaço acima do botão
        )

    def atualizar_lista_tarefas(self):
        """Atualiza a lista de tarefas centralizadas"""
        self.editing_task_id = None
        session = Session()
        
        try:
            self.tarefas_list.controls.clear()
            todas_tarefas = session.query(Tarefa).all()

            for tarefa in todas_tarefas:
                def on_checkbox_change(e, tarefa_container):
                    tarefa_container.bgcolor = "#5A5A5A" if e.control.value else "#6E6E6E"
                    tarefa_container.update()

                # Container da tarefa centralizado
                tarefa_container = ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Text(f"{tarefa.descricao}", size=14, text_align="center", color="white"),
                                on_click=lambda e, t=tarefa: self.abrir_edicao_tarefa(e, t),
                                alignment=ft.alignment.center
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=ft.padding.all(5),
                    bgcolor="#6E6E6E",
                    border=ft.border.all(1, "#5C5C5C"),
                    border_radius=ft.border_radius.all(5),
                    shadow=ft.BoxShadow(blur_radius=5, color="black", spread_radius=1),
                    alignment=ft.alignment.center,
                    width=280
                )

                # Linha da tarefa centralizada
                tarefa_row = ft.Row(
                    [
                        tarefa_container,
                        ft.Checkbox(
                            value=False,
                            data=tarefa.id,
                            fill_color="#5A5A5A",
                            on_change=lambda e, tc=tarefa_container: on_checkbox_change(e, tc)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
                
                # Container para centralizar a linha da tarefa
                centered_row = ft.Container(
                    content=tarefa_row,
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=20)
                )
                
                self.tarefas_list.controls.append(centered_row)

            self.tarefas_list.update()

        finally:
            session.close()

    def abrir_edicao_tarefa(self, e, tarefa):
        if self.editing_task_id is not None and self.editing_task_id != tarefa.id:
            return  # Impede abrir outro campo de edição se já houver um aberto

        self.editing_task_id = tarefa.id  # Define a tarefa atual como em edição
        descricao_input = ft.TextField(
            value=tarefa.descricao,
            expand=False,  # Remove o comportamento de expansão para alinhar melhor
            text_align="start",  # Alinha o texto à esquerda
            autofocus=True,  # Foca automaticamente no campo ao editar
            multiline=True,  # Permite múltiplas linhas
            max_lines=None,  # Sem limite de linhas
            min_lines=1,  # Garante pelo menos uma linha visível
            width=270,  # Define a largura para alinhar com a caixa da lista
            height=70,  # Define uma altura fixa para alinhar com o design
            color="white",  # Texto branco
            bgcolor="black",  # Fundo preto
            border_color="white",  # Remove a borda visível
            focused_border_color="white"  # Remove a borda ao focar no campo
            
        )
        error_text = ft.Text(value="", color="white", weight="bold")  # Alterado para branco

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
                    self.editing_task_id = None  # Libera a edição após salvar
                    self.atualizar_lista_tarefas()  # Atualiza a lista de tarefas
                else:
                    error_text.value = resultado  # Exibe qualquer outro erro retornado
                    error_text.update()

        def cancelar_edicao(e):
            self.editing_task_id = None  # Libera a edição ao cancelar
            self.atualizar_lista_tarefas()  # Atualiza a lista de tarefas
        
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
                                alignment=ft.alignment.center,  # Centraliza o conteúdo do botão
                                bgcolor="green",  # Define a cor de fundo do container
                                border_radius=ft.border_radius.all(5),  # Adiciona um leve arredondamento
                                content=ft.ElevatedButton(
                                    content=ft.Text("Salvar", font_family="Mine", size=12),  # Ícone de edição
                                    bgcolor="transparent",  # Torna o botão transparente para usar o fundo do container
                                    color="white",
                                    elevation=0,  # Remove a elevação para alinhar com o container
                                    on_click=salvar_edicao  # Chama a função de salvar
                                )
                            ),
                            ft.Container(width=50),  # Adiciona um espaçamento fixo entre os botões
                            ft.Container(
                                width=100,
                                height=40,  # Define altura menor para tornar o botão mais compacto
                                alignment=ft.alignment.center,  # Centraliza o conteúdo do botão
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
                        ],
                        alignment=ft.MainAxisAlignment.START  # Alinha os botões no início, com o espaçamento fixo
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER  # Centraliza o conteúdo verticalmente
            )
        )
        tarefa_row.update()

    def on_excluir_tarefa_click(self, e):
        # Coleta todas as tarefas marcadas
        tarefas_marcadas = []
        for item in self.tarefas_list.controls:
            if isinstance(item, ft.Container) and isinstance(item.content, ft.Row):
                row = item.content
                if len(row.controls) >= 2 and isinstance(row.controls[1], ft.Checkbox):
                    checkbox = row.controls[1]
                    if checkbox.value and checkbox.data:
                        tarefas_marcadas.append(checkbox.data)

        if tarefas_marcadas:
            def confirmar_exclusao(e):
                erros = []
                for tarefa_id in tarefas_marcadas:
                    resultado = excluir_tarefa(tarefa_id)
                    if not isinstance(resultado, str) or "sucesso" not in resultado.lower():
                        erros.append(tarefa_id)

                self.fechar_dialog(dialog)

                if erros:
                    self.mostrar_dialogo_erro(f"Erro ao excluir as tarefas: {', '.join(map(str, erros))}")
                else:
                    self.atualizar_lista_tarefas()

            def cancelar_exclusao(e):
                self.fechar_dialog(dialog)

            # Criação do pop-up de confirmação
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("CONFIRMAR EXCLUSÃO", color="red", weight="bold"),
                content=ft.Text(f"Você tem certeza que deseja excluir {len(tarefas_marcadas)} tarefa(s) selecionada(s)?", weight="bold"),
                actions=[
                    ft.TextButton("SIM", on_click=confirmar_exclusao),
                    ft.TextButton("NÃO", on_click=cancelar_exclusao)
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            # Abre o diálogo
            self.page.dialog = dialog
            dialog.open = True
            self.page.update()
        else:
            # Criação do pop-up de erro
            self.mostrar_dialogo_erro("Nenhuma tarefa selecionada. Por favor, selecione pelo menos uma tarefa para excluir.")

    def mostrar_dialogo_erro(self, mensagem):
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("ERRO", color="red", weight="bold"),
            content=ft.Text(mensagem, weight="bold"),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.fechar_dialog(dialog))
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def fechar_dialog(self, dialog):
        dialog.open = False
        self.page.update()
