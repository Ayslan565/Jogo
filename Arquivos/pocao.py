import pygame
import os

class PocaoVida:
    """
    Representa um item consumível de Poção de Vida.
    Quando usado, restaura completamente a vida do jogador.
    """
    def __init__(self):
        """
        Inicializa os atributos da poção, como nome, descrição e ícone.
        """
        self.nome = "Poção de Vida"
        self.descricao = "Um frasco de líquido carmesim que restaura toda a sua vida."
        self.tipo = "Consumível"
        
        # Carrega o ícone da poção que será exibido na interface do usuário (UI).
        # Certifique-se de que a imagem correspondente exista no caminho especificado.
        caminho_icone = os.path.join("Sprites", "Itens", "Pocoes", "pocao_vida.png")
        self.icone = self._carregar_icone(caminho_icone)

    def _carregar_icone(self, caminho_relativo: str, tamanho: tuple = (48, 48)):
        """
        Carrega a imagem do ícone a partir de um caminho relativo à raiz do projeto.
        Retorna uma superfície do Pygame ou um placeholder em caso de erro.
        """
        try:
            # Constrói o caminho absoluto a partir da localização deste script
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            caminho_completo = os.path.join(base_dir, caminho_relativo.replace("/", os.sep))

            if not os.path.exists(caminho_completo):
                raise FileNotFoundError(f"Arquivo de ícone não encontrado: {caminho_completo}")

            icone = pygame.image.load(caminho_completo).convert_alpha()
            return pygame.transform.scale(icone, tamanho)
        except (pygame.error, FileNotFoundError) as e:
            print(f"ALERTA (PocaoVida): Não foi possível carregar o ícone '{caminho_relativo}'. Usando placeholder. Erro: {e}")
            # Cria um ícone placeholder rosa para indicar que a imagem está faltando
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            placeholder.fill((255, 0, 100, 200)) # Rosa semitransparente
            return placeholder

    def usar(self, jogador) -> bool:
        """
        Aplica o efeito da poção no jogador.
        Verifica se a vida do jogador não está cheia antes de usar.

        Args:
            jogador: A instância do objeto Player que está usando o item.

        Returns:
            True se o item foi consumido com sucesso, False caso contrário.
        """
        # Verifica se o jogador e seu sistema de vida são válidos
        if not jogador or not hasattr(jogador, 'vida') or not hasattr(jogador.vida, 'vida_atual'):
            return False

        # A poção só pode ser usada se a vida não estiver no máximo
        if jogador.vida.vida_atual < jogador.vida.vida_maxima:
            # Acessa o método de cura da classe Vida e cura o máximo possível
            jogador.vida.receber_cura(jogador.vida.vida_maxima)
            print(f"INFO: Jogador usou '{self.nome}' e recuperou a vida toda.")
            return True # Retorna True para indicar que o consumível foi gasto
        else:
            print(f"INFO: Vida do jogador já está cheia. '{self.nome}' não foi usada.")
            return False # Retorna False, o item não é consumido
