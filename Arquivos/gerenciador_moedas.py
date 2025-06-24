# gerenciador_moedas.py
import pygame
import os

class GerenciadorMoedas:
    """
    Classe para gerenciar as moedas do jogador e exibir a contagem na tela.
    """
    def __init__(self, jogador_ref, fonte_path=None, tamanho_fonte=28, cor_texto=(255, 215, 0)):
        """
        Inicializa o GerenciadorMoedas.

        Args:
            jogador_ref: Referência direta para a instância do jogador.
            fonte_path (str, optional): Caminho para um arquivo de fonte .ttf. Defaults to None (usa fonte padrão).
            tamanho_fonte (int, optional): Tamanho da fonte para exibir as moedas. Defaults to 28.
            cor_texto (tuple, optional): Cor do texto das moedas (R, G, B). Defaults to (255, 215, 0) (dourado).
        """
        
        self.jogador_ref = jogador_ref
        self.cor_texto = cor_texto
        self.fonte = None

        try:
            if not pygame.font.get_init(): # Garante que o módulo de fontes do Pygame está inicializado
                pygame.font.init()

            if fonte_path and os.path.exists(fonte_path):
                self.fonte = pygame.font.Font(fonte_path, tamanho_fonte)
            else:
                self.fonte = pygame.font.Font(None, tamanho_fonte) # Usa a fonte padrão do Pygame
        except Exception as e:
            print(f"AVISO(GerenciadorMoedas): Erro ao carregar fonte '{fonte_path}': {e}. Usando fonte padrão.")
            self.fonte = pygame.font.Font(None, tamanho_fonte) # Fallback final

    def adicionar_moedas(self, quantidade: int):
        print(f"DEBUG: Jogador recebeu {quantidade} moedas. Total: {self.jogador_ref.dinheiro}")
        
        """
        Adiciona uma quantidade de moedas ao jogador.

        Args:
            quantidade (int): A quantidade de moedas a ser adicionada.
        """
        if hasattr(self.jogador_ref, 'dinheiro' ):
            if quantidade > 0:
                self.jogador_ref.dinheiro += quantidade
       #         print(f"DEBUG: Jogador recebeu {quantidade} moedas. Total: {self.jogador_ref.dinheiro}")

        else:
            print("ERRO(GerenciadorMoedas): Objeto jogador não possui o atributo 'dinheiro'.")

    def gastar_moedas(self, quantidade: int) -> bool:
        """
        Tenta gastar uma quantidade de moedas do jogador.

        Args:
            quantidade (int): A quantidade de moedas a ser gasta.

        Returns:
            bool: True se as moedas foram gastas com sucesso, False caso contrário.
        """
        if hasattr(self.jogador_ref, 'dinheiro'):
            if self.jogador_ref.dinheiro >= quantidade:
                self.jogador_ref.dinheiro -= quantidade
                # print(f"DEBUG: Jogador gastou {quantidade} moedas. Restante: {self.jogador_ref.dinheiro}")
                return True
            else:
                # print("DEBUG: Moedas insuficientes para gastar.")
                return False
        else:
            print("ERRO(GerenciadorMoedas): Objeto jogador não possui o atributo 'dinheiro'.")
            return False

    def get_saldo_moedas(self) -> int:
        """
        Retorna o saldo atual de moedas do jogador.

        Returns:
            int: A quantidade de moedas do jogador, ou 0 se o atributo não existir.
        """
        return getattr(self.jogador_ref, 'dinheiro', 0)

    def desenhar_hud_moedas(self, tela: pygame.Surface, pos_x: int, pos_y: int):
        """
        Desenha a contagem de moedas do jogador na tela.

        Args:
            tela (pygame.Surface): A superfície onde desenhar.
            pos_x (int): A coordenada X para a posição do texto.
            pos_y (int): A coordenada Y para a posição do texto.
        """
        if self.fonte and hasattr(self.jogador_ref, 'dinheiro'):
            texto_moedas = f"Moedas: {self.get_saldo_moedas()}" # Usa o método get_saldo_moedas
            try:
                superficie_texto = self.fonte.render(texto_moedas, True, self.cor_texto)
                tela.blit(superficie_texto, (pos_x, pos_y))
            except Exception as e:
                print(f"ERRO(GerenciadorMoedas): Falha ao renderizar texto de moedas: {e}")
        elif not self.fonte:
            # Esta mensagem só aparecerá uma vez se a fonte falhar ao carregar no __init__
            # print("AVISO(GerenciadorMoedas): Fonte não carregada, não é possível desenhar HUD de moedas.")
            pass
