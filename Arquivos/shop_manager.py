import pygame
import random
import time
import os
import math

# Importa a função para rodar a cena da loja
# Adicionado try-except para robustez
try:
    from loja import run_shop_scene
except ImportError:
    run_shop_scene = None
    print("Aviso: Arquivo 'loja.py' ou função 'run_shop_scene' não encontrado. A loja não funcionará.") # Mensagem mais específica

# Importa a probabilidade e o intervalo mínimo de spawn da loja
# Adicionado try-except para robustez
try:
    from Spawn_Loja import PROBABILIDADE_SPAWN_LOJA, INTERVALO_MINIMO_SPAWN_LOJA
except ImportError:
    PROBABILIDADE_SPAWN_LOJA = 0.0 # Define probabilidade zero se o arquivo não for encontrado
    INTERVALO_MINIMO_SPAWN_LOJA = 0 # Define intervalo zero se o arquivo não for encontrado
    print("Aviso: Arquivo 'Spawn_Loja.py' não encontrado. O spawn da loja está desativado.") # Mensagem mais específica


# Caminho para o sprite da loja no mapa
SHOP_SPRITE_PATH = "Sprites/Loja/Loja.png" # Corrigido barra invertida
# Tamanho do placeholder da loja se a imagem não carregar
SHOP_PLACEHOLDER_SIZE = (150, 150)


class ShopManager:
    """
    Gerencia o spawn, atualização e desenho da loja especial no mapa do jogo,
    incluindo pop-up e seta indicativa.
    """
    # Adicionado argumentos largura_tela e altura_tela ao construtor
    def __init__(self, largura_tela, altura_tela):
        """
        Inicializa o gerenciador da loja.

        Args:
            largura_tela (int): Largura da tela do jogo.
            altura_tela (int): Altura da tela do jogo.
        """
        self.largura_tela = largura_tela # Armazena a largura da tela
        self.altura_tela = altura_tela # Armazena a altura da tela

        self.current_shop_rect = None # Retângulo de colisão da loja no mundo do jogo
        self.shop_sprite_image = None # Imagem do sprite da loja
        self.last_shop_spawn_time = time.time() # Tempo do último spawn bem-sucedido da loja

        # Variáveis para o pop-up e seta da loja
        self.shop_spawn_popup_message = ""
        self.shop_popup_display_time = 0 # Tempo restante para exibir o pop-up (em milissegundos)
        self.shop_arrow_visible = False
        self.shop_arrow_display_time = 0 # Tempo restante para exibir a seta (em milissegundos)
        self.shop_arrow_target_pos = (0, 0) # Posição do alvo da seta (centro da loja)

        # Carrega a imagem do sprite da loja uma vez na inicialização
        self._load_shop_sprite()

        # Variável para rastrear o estado de interação (para evitar abrir a loja várias vezes com um único clique)
        self._can_interact = True


    def _load_shop_sprite(self):
        """Tenta carregar a imagem do sprite da loja ou cria um placeholder."""
        try:
            # Verifica se o arquivo existe antes de tentar carregar
            if os.path.exists(SHOP_SPRITE_PATH):
                self.shop_sprite_image = pygame.image.load(SHOP_SPRITE_PATH).convert_alpha()
                # Opcional: Redimensionar a imagem da loja se necessário
                # self.shop_sprite_image = pygame.transform.scale(self.shop_sprite_image, (200, 200)) # Exemplo de redimensionamento
            else:
                # Cria um placeholder se a imagem não for encontrada
                print(f"Aviso: Sprite da loja não encontrado em '{SHOP_SPRITE_PATH}'. Usando placeholder.") # Mensagem informativa
                self.shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
                pygame.draw.rect(self.shop_sprite_image, (100, 50, 0), (0, 0, SHOP_PLACEHOLDER_SIZE[0], SHOP_PLACEHOLDER_SIZE[1])) # Placeholder marrom

        except pygame.error as e:
            print(f"Erro ao carregar imagem da loja: {e}. Usando placeholder.") # Mantido, é um erro de carregamento
            # Cria um placeholder em caso de erro de carregamento
            self.shop_sprite_image = pygame.Surface(SHOP_PLACEHOLDER_SIZE, pygame.SRCALPHA)
            pygame.draw.rect(self.shop_sprite_image, (100, 50, 0), (0, 0, SHOP_PLACEHOLDER_SIZE[0], SHOP_PLACEHOLDER_SIZE[1])) # Placeholder marrom


    def check_and_spawn_shop(self, jogador, bloco_coord, base_x, base_y):
        """
        Verifica as condições e spawna a loja em um novo bloco de mapa, se aplicável.

        Args:
            jogador (Player): O objeto jogador.
            bloco_coord (tuple): Coordenadas (x, y) do bloco atual.
            base_x (int): Posição X base do bloco.
            base_y (int): Posição Y base do bloco.
        """
        # Verifica si a loja ainda não existe no mundo
        # Verifica si a probabilidade de spawn é maior que 0 e a função run_shop_scene existe
        # E verifica si o intervalo mínimo desde o último spawn passou
        current_time = time.time()
        if self.current_shop_rect is None and PROBABILIDADE_SPAWN_LOJA > 0 and run_shop_scene is not None and \
           (current_time - self.last_shop_spawn_time) >= INTERVALO_MINIMO_SPAWN_LOJA:

            # Rola a "sorte" para spawnar a loja neste bloco
            if random.random() < PROBABILIDADE_SPAWN_LOJA:

                # Calcula uma posição aleatória para a loja dentro deste bloco
                bloco_tamanho = 1080 # Tamanho do bloco (hardcoded aqui, pode ser passado como parâmetro se variar)
                # Garante que a loja spawne dentro dos limites do bloco com alguma margem
                shop_x = base_x + random.randint(50, bloco_tamanho - (self.shop_sprite_image.get_width() if self.shop_sprite_image else SHOP_PLACEHOLDER_SIZE[0]) - 50)
                shop_y = base_y + random.randint(50, bloco_tamanho - (self.shop_sprite_image.get_height() if self.shop_sprite_image else SHOP_PLACEHOLDER_SIZE[1]) - 50)
                shop_world_pos = (shop_x, shop_y)

                # Cria o retângulo de colisão para a loja na posição calculada
                if self.shop_sprite_image is not None:
                    self.current_shop_rect = self.shop_sprite_image.get_rect(topleft=shop_world_pos)
                    self.last_shop_spawn_time = current_time # Atualiza o tempo do último spawn bem-sucedido

                    # --- Ativa o pop-up e a seta ---
                    self.shop_spawn_popup_message = "Uma loja apareceu!"
                    self.shop_popup_display_time = 3000 # Exibir pop-up por 3 segundos (em milissegundos)
                    self.shop_arrow_visible = True
                    self.shop_arrow_display_time = 10000 # Exibir seta por 10 segundos (em milissegundos)
                    # A seta aponta para o centro do retângulo da loja
                    self.shop_arrow_target_pos = self.current_shop_rect.center


    def update_visuals_timers(self, dt_ms):
        """
        Atualiza os timers para o pop-up e a seta da loja.

        Args:
            dt_ms (int): Tempo decorrido desde o último frame em milissegundos.
        """
        if self.shop_popup_display_time > 0:
            self.shop_popup_display_time -= dt_ms
            if self.shop_popup_display_time <= 0:
                self.shop_spawn_popup_message = "" # Limpa a mensagem


        if self.shop_arrow_display_time > 0:
            self.shop_arrow_display_time -= dt_ms
            if self.shop_arrow_display_time <= 0:
                self.shop_arrow_visible = False # Esconde a seta


    # Modificado para lidar com eventos e retornar o estado do jogo
    def handle_event(self, evento, jogador):
        """
        Processa eventos relacionados à interação com a loja.

        Args:
            evento (pygame.event.Event): O evento a ser processado.
            jogador (Player): O objeto jogador.

        Returns:
            str or None: Retorna "shop" se a cena da loja for ativada,
                         "playing" se a cena da loja for fechada para continuar o jogo,
                         "quit" se o jogo for encerrado a partir da loja,
                         ou None caso contrário.
        """
        # Verifica se a loja existe no mapa
        if self.current_shop_rect is not None and jogador is not None and hasattr(jogador, 'rect'):
             # Verifica se o jogador está colidindo com a loja
             if jogador.rect.colliderect(self.current_shop_rect):
                  # Verifica se a tecla de interação foi pressionada
                  if evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
                       # Verifica se pode interagir (evita múltiplos cliques)
                       if self._can_interact:
                            self._can_interact = False # Desativa a interação temporariamente
                            # Verifica se a função da cena da loja existe
                            if run_shop_scene is not None:
                                # Pausa a música do jogo antes de entrar na loja
                                pygame.mixer.music.pause()
                                # Roda a cena da loja, passando a janela, jogador, largura e altura
                                # A janela será passada para run_shop_scene a partir do loop principal do jogo
                                # Retorna o resultado da cena da loja (True para continuar, False para sair)
                                # A janela será passada no loop principal ao chamar shop_manager.handle_event
                                # Aqui, apenas indicamos que a cena da loja deve ser ativada
                                return "shop" # Indica para mudar o estado do jogo para "shop"
                            else:
                                print("Função run_shop_scene não disponível. Não foi possível entrar na loja.") # Mensagem de erro
                                return None # Nenhuma ação de interação

                  # Reseta a flag de interação quando a tecla é solta
                  if evento.type == pygame.KEYUP and evento.key == pygame.K_e:
                       self._can_interact = True

        return None # Nenhum evento de interação com a loja processado


    # Adicionado método para desenhar a cena da loja (se o ShopManager for responsável por isso)
    # Se a lógica da loja estiver toda em run_shop_scene, este método pode não ser necessário
    def draw_shop_scene(self, janela):
        """
        Desenha a interface da cena da loja.
        (Este método pode ser chamado se o ShopManager gerenciar o desenho da UI da loja)

        Args:
            janela (pygame.Surface): A superfície onde desenhar.
        """
        # Lógica de desenho da UI da loja aqui
        # Exemplo: preencher o fundo, desenhar botões, inventário do jogador, itens da loja, etc.
        janela.fill((50, 50, 50)) # Fundo cinza para a loja
        # Desenhar elementos da UI da loja...


    def draw(self, janela, camera_x, camera_y, jogador=None):
        """
        Desenha o sprite da loja, pop-up e seta na janela.

        Args:
            janela (pygame.Surface): A superfície onde desenhar.
            camera_x (int): O offset x da câmera.
            camera_y (int): O offset y da câmera.
            jogador (Player, optional): O objeto jogador, necessário para desenhar a seta. Defaults to None.
        """
        # --- Desenha o sprite da loja no mundo do jogo (se existir) ---
        # Verifica se a imagem da loja e o retângulo existem
        if self.shop_sprite_image is not None and self.current_shop_rect is not None:
            # Calcula a posição da imagem na tela com o offset da câmera
            shop_screen_pos = (self.current_shop_rect.x - camera_x, self.current_shop_rect.y - camera_y)
            janela.blit(self.shop_sprite_image, shop_screen_pos)


        # --- Desenha o pop-up da loja (se ativo) ---
        if self.shop_popup_display_time > 0 and self.shop_spawn_popup_message:
            # Usa uma fonte simples para o pop-up
            try:
                popup_font = pygame.font.Font(None, 40)
                popup_text_surface = popup_font.render(self.shop_spawn_popup_message, True, (255, 255, 255))
                # Posiciona o pop-up no centro superior da tela
                popup_rect = popup_text_surface.get_rect(center=(janela.get_width() // 2, 80))
                # Desenha um fundo semi-transparente para o pop-up (opcional)
                popup_bg = pygame.Surface((popup_rect.width + 20, popup_rect.height + 10), pygame.SRCALPHA)
                popup_bg.fill((0, 0, 0, 180)) # Fundo preto semi-transparente
                janela.blit(popup_bg, (popup_rect.x - 10, popup_rect.y - 5))
                janela.blit(popup_text_surface, popup_rect)
            except pygame.error as e:
                print(f"Erro ao desenhar pop-up da loja: {e}") # Mantido, pois é um erro de desenho, não debug


        # --- Desenha a seta apontando para a loja (se ativa) ---
        if self.shop_arrow_visible and self.current_shop_rect is not None and jogador is not None and hasattr(jogador, 'rect'):
            # Calcula a posição do centro da tela
            screen_center_x = janela.get_width() // 2
            screen_center_y = janela.get_height() // 2
            screen_center = (screen_center_x, screen_center_y)

            # Calcula a posição da loja na tela (com offset da câmera)
            shop_screen_center_x = self.current_shop_rect.centerx - camera_x
            shop_screen_center_y = self.current_shop_rect.centery - camera_y
            shop_screen_center = (shop_screen_center_x, shop_screen_center_y)

            # Calcula o vetor da tela para a loja na tela
            direction_vector = (shop_screen_center_x - screen_center_x, shop_screen_center_y - screen_center_y)

            # Calcula a distância até a loja na tela
            distance_to_shop_on_screen = math.hypot(direction_vector[0], direction_vector[1])

            # Define a posição inicial da seta (um pouco afastada do centro da tela)
            arrow_start_distance = 100 # Distância do centro da tela onde a seta começa
            arrow_length = 30 # Comprimento da seta

            # Desenha a seta apenas se a loja estiver fora da área visível central
            if distance_to_shop_on_screen > arrow_start_distance:
                # Normaliza o vetor de direção
                if distance_to_shop_on_screen > 0:
                    direction_norm = (direction_vector[0] / distance_to_shop_on_screen,
                                      direction_vector[1] / distance_to_shop_on_screen)
                else:
                    direction_norm = (0, 0) # Evita divisão por zero

                # Calcula a posição inicial da seta na tela
                arrow_start_x = screen_center_x + direction_norm[0] * arrow_start_distance
                arrow_start_y = screen_center_y + direction_norm[1] * arrow_start_distance
                arrow_start_pos = (arrow_start_x, arrow_start_y)

                # Calcula a posição final da seta (ponta)
                arrow_end_x = arrow_start_x + direction_norm[0] * arrow_length
                arrow_end_y = arrow_start_y + direction_norm[1] * arrow_length
                arrow_end_pos = (arrow_end_x, arrow_end_y)

                # Desenha a linha principal da seta
                pygame.draw.line(janela, (255, 255, 0), arrow_start_pos, arrow_end_pos, 3) # Seta amarela

                # Desenha as pontas da seta (triângulo)
                # Calcula o ângulo da seta
                angle = math.atan2(direction_norm[1], direction_norm[0])
                # Calcula os pontos da base do triângulo da ponta
                head_size = 10 # Tamanho da ponta da seta
                point1 = (arrow_end_x - head_size * math.cos(angle - math.pi / 6),
                          arrow_end_y - head_size * math.sin(angle - math.pi / 6))
                point2 = (arrow_end_x - head_size * math.cos(angle + math.pi / 6),
                          arrow_end_y - head_size * math.sin(angle + math.pi / 6))
                # Desenha o triângulo da ponta
                pygame.draw.polygon(janela, (255, 255, 0), [arrow_end_pos, point1, point2]) # Seta amarela
