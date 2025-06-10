# Nome do arquivo: tela_selecao_arma.py
import pygame
import sys
import os
import import_Loja
# --- Configurações da Tela ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- Cores ---
COR_FUNDO = (30, 30, 30)
COR_TEXTO = (230, 230, 230)
COR_TEXTO_ARMA = (200, 200, 200)
COR_DESTAQUE = (255, 255, 0)
COR_BOTAO = (0, 120, 0)
COR_BOTAO_HOVER = (0, 180, 0)
COR_BOTAO_TEXTO = (255, 255, 255)
COR_PLACEHOLDER_IMG = (100, 100, 100)
COR_BORDA_PLACEHOLDER = (255, 0, 0)

# --- Configurações das Armas e Layout ---
# !! IMPORTANTE: Certifique-se que as imagens referenciadas em WEAPONS_DATA
# !! estejam na mesma pasta que este script, ou ajuste os caminhos.
WEAPONS_DATA = [
    {
        "name": "Adaga do Fogo Contudente",
        "id": "adaga_fogo",
        "image_path": "Sprites/Armas/Adagas/AdagaFogo/Icone_E1.png", # Ex: seu 'Adaga E-1.png' renomeado e colocado aqui
        "surface": None,
        "display_rect": None
    },
    {
        "name": "Machado Bárbaro Cravejado",
        "id": "machado_barbaro",
        "image_path": "Sprites/Armas/Machados/Icone_MB1.png", # Ex: seu 'Icone_MB1.png' renomeado e colocado aqui
        "surface": None,
        "display_rect": None
    }
]

IMAGE_DISPLAY_WIDTH = 150  # Largura da imagem da arma na tela de seleção
IMAGE_DISPLAY_HEIGHT = 150 # Altura da imagem da arma
ITEM_PADDING = 80
TEXT_OFFSET_Y = 20

# --- Botão Confirmar ---
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_TEXT = "Confirmar"

def draw_text(surface, text, font, color, center_pos):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center_pos)
    surface.blit(text_surface, text_rect)

def executar_tela_selecao_arma():
    """
    Executa a tela de seleção de armas.
    Retorna o ID da arma escolhida ('adaga_fogo' ou 'machado_barbaro') ou None se fechado.
    Esta função assume que pygame.init() já foi chamado pelo seu jogo principal,
    mas por segurança, ela garante a inicialização dos módulos necessários se não estiverem.
    Ela NÃO chama pygame.quit().
    """
    if not pygame.get_init(): # Se o Pygame principal não foi inicializado
        pygame.init()
        # Se o módulo de fontes não foi inicializado (pygame.init() faz isso, mas para garantir)
    if not pygame.font.get_init():
        pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Escolha sua Arma Inicial")
    clock = pygame.time.Clock()

    try:
        title_font = pygame.font.Font(None, 50)
        weapon_name_font = pygame.font.Font(None, 30)
        button_font = pygame.font.Font(None, 36)
    except pygame.error:
        title_font = pygame.font.SysFont("arial", 50)
        weapon_name_font = pygame.font.SysFont("arial", 30)
        button_font = pygame.font.SysFont("arial", 36)

    script_dir = os.path.dirname(os.path.abspath(__file__)) # Diretório do script atual

    for weapon_info in WEAPONS_DATA:
        try:
            image_full_path = weapon_info["image_path"]
            if not os.path.isabs(image_full_path): # Se não for absoluto, considera relativo ao script
                 image_full_path = os.path.join(script_dir, image_full_path)

            original_image = pygame.image.load(image_full_path).convert_alpha()
            weapon_info["surface"] = pygame.transform.smoothscale(original_image, (IMAGE_DISPLAY_WIDTH, IMAGE_DISPLAY_HEIGHT))
        except pygame.error as e:
            print(f"Erro ao carregar imagem '{weapon_info['image_path']}': {e}")
            print(f"Caminho tentado: {image_full_path}")
            weapon_info["surface"] = pygame.Surface((IMAGE_DISPLAY_WIDTH, IMAGE_DISPLAY_HEIGHT), pygame.SRCALPHA)
            weapon_info["surface"].fill(COR_PLACEHOLDER_IMG)
            pygame.draw.rect(weapon_info["surface"], COR_BORDA_PLACEHOLDER, (0,0, IMAGE_DISPLAY_WIDTH, IMAGE_DISPLAY_HEIGHT), 3)
            draw_text(weapon_info["surface"], "X", title_font, COR_BORDA_PLACEHOLDER, (IMAGE_DISPLAY_WIDTH//2, IMAGE_DISPLAY_HEIGHT//2))

    num_weapons = len(WEAPONS_DATA)
    total_content_width = (num_weapons * IMAGE_DISPLAY_WIDTH) + ((num_weapons - 1) * ITEM_PADDING)
    start_x = (SCREEN_WIDTH - total_content_width) // 2
    image_y = SCREEN_HEIGHT // 2 - IMAGE_DISPLAY_HEIGHT // 2 - 30

    for i, weapon_info in enumerate(WEAPONS_DATA):
        item_x = start_x + i * (IMAGE_DISPLAY_WIDTH + ITEM_PADDING)
        weapon_info["display_rect"] = pygame.Rect(item_x, image_y, IMAGE_DISPLAY_WIDTH, IMAGE_DISPLAY_HEIGHT)

    button_rect = pygame.Rect(
        (SCREEN_WIDTH - BUTTON_WIDTH) // 2,
        SCREEN_HEIGHT - BUTTON_HEIGHT - 40,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )

    selected_weapon_index = 0
    chosen_weapon_id = None
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        current_button_color = COR_BOTAO

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                chosen_weapon_id = None 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    selected_weapon_index = (selected_weapon_index - 1) % num_weapons
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    selected_weapon_index = (selected_weapon_index + 1) % num_weapons
                elif event.key == pygame.K_RETURN:
                    chosen_weapon_id = WEAPONS_DATA[selected_weapon_index]["id"]
                    running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if button_rect.collidepoint(mouse_pos):
                        chosen_weapon_id = WEAPONS_DATA[selected_weapon_index]["id"]
                        running = False
                    else:
                        for i, weapon_info in enumerate(WEAPONS_DATA):
                            if weapon_info["display_rect"].collidepoint(mouse_pos):
                                selected_weapon_index = i
                                break
        
        if button_rect.collidepoint(mouse_pos):
            current_button_color = COR_BOTAO_HOVER

        screen.fill(COR_FUNDO)
        draw_text(screen, "Escolha sua Arma Inicial", title_font, COR_TEXTO, (SCREEN_WIDTH // 2, 80))

        for i, weapon_info in enumerate(WEAPONS_DATA):
            screen.blit(weapon_info["surface"], weapon_info["display_rect"].topleft)
            name_center_x = weapon_info["display_rect"].centerx
            name_center_y = weapon_info["display_rect"].bottom + TEXT_OFFSET_Y + weapon_name_font.get_height() // 2
            draw_text(screen, weapon_info["name"], weapon_name_font, COR_TEXTO_ARMA, (name_center_x, name_center_y))
            if i == selected_weapon_index:
                pygame.draw.rect(screen, COR_DESTAQUE, weapon_info["display_rect"], 3)

        pygame.draw.rect(screen, current_button_color, button_rect, border_radius=8)
        pygame.draw.rect(screen, COR_TEXTO, button_rect, 2, border_radius=8)
        draw_text(screen, BUTTON_TEXT, button_font, COR_BOTAO_TEXTO, button_rect.center)
        
        pygame.display.flip()
        clock.tick(FPS)

    if chosen_weapon_id:
        chosen_weapon_full_name = next((w["name"] for w in WEAPONS_DATA if w["id"] == chosen_weapon_id), "N/A")
        print(f"Tela de Seleção: Arma escolhida: {chosen_weapon_full_name} (ID: {chosen_weapon_id})")
        return chosen_weapon_id
    else:
        print("Tela de Seleção: Nenhuma arma escolhida (tela fechada).")
        return None

# Este bloco permite testar a tela de seleção de forma isolada
if __name__ == '__main__':
    # Para o teste standalone, inicializamos e finalizamos o Pygame aqui.
    pygame.init() # Necessário para o teste standalone
    
    arma_selecionada_id = executar_tela_selecao_arma()
    
    if arma_selecionada_id:
        print(f"Retorno do teste standalone: ID da arma '{arma_selecionada_id}'")
    else:
        print("Retorno do teste standalone: Nenhuma arma foi escolhida.")
        
    pygame.quit() # Finaliza o Pygame após o teste standalone
    sys.exit()
