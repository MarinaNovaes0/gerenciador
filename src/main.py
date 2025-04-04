import flet as ft
from view.home import Home
from view.tarefa_view import TarefaView

def main(page: ft.Page):
    page.title = "Cadastro de Tarefa"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Ajusta o alinhamento horizontal
    page.bgcolor = None  # Remove a cor de fundo
    page.clean()
    page.padding = 0  # Remove qualquer padding da página
    page.spacing = 0  # Remove espaçamento entre os elementos
    background_image = ft.Image(
        src="https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/f2/Dirt_background_BE1.png/revision/latest?cb=20210820093527",  # URL da imagem
        fit=ft.ImageFit.COVER,
        expand=True  # Faz a imagem preencher toda a tela
    )
    # Certifique-se de que o link seja válido
    page.add(ft.Stack([background_image]))  # Adiciona a imagem de fundo

    # Configuração global da fonte
    page.fonts = {
        "Mine": "/fonts/minecraftia/Minecraftia-Regular.ttf",
        "Mine 2": "/fonts/minedings/minedings.ttf"
    }
    page.theme = ft.Theme(font_family="Mine")  # Define a fonte global como "Mine"
    
    page.theme_mode = ft.ThemeMode.DARK
    page.window_resizable = True  # Permite redimensionar a janela
    page.window_width = 360  # Largura padrão para dispositivos móveis
    page.window_height = 640  # Altura padrão para dispositivos móveis
    
    def mudar_rotas(e):
        if e.control.selected_index == 0:
            print('indo para cadastro')
            page.go('/cadastro')
        elif e.control.selected_index == 1:
            print('indo para boletim')
            page.go('/boletim')
            
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Text("N", font_family="Mine 2", size=30), label="Cadastro"),
            ft.NavigationBarDestination(icon=ft.Text("B", font_family="Mine 2", size=30), label="Listagem"),
        ],
        on_change=mudar_rotas      
    )  
      
    def rotas(route):
        page.controls.clear()
        if route == '/cadastro':
            tela = Home(page)
        elif route == '/boletim':
            tela = TarefaView(page)
        else:
            tela = Home(page)  # Define a tela padrão como Home

        page.add(tela.construir())
        page.update()
    
    page.on_route_change = lambda e: rotas(e.route)
    page.go('/cadastro')
    page.update()

if __name__ == "__main__":
    ft.app(target=main)  # Executa o aplicativo no navegador
