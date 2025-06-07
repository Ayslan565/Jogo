# Jogo/Arquivos/creditos.py
import pygame
import sys
import os

def exibir_creditos(tela, clock):
    """
    Exibe uma tela de créditos rolantes em uma superfície Pygame já existente.

    Args:
        tela (pygame.Surface): A superfície principal do jogo onde os créditos serão desenhados.
        clock (pygame.time.Clock): O relógio principal do jogo para controlar o FPS.
    """
    # --- Constantes e Configurações ---
    VELOCIDADE_ROLAGEM = 1
    COR_FUNDO = (0, 0, 0)
    COR_TEXTO = (255, 255, 255)
    TAMANHO_FONTE_NOME = 40
    TAMANHO_FONTE_FUNCAO = 25
    ESPACO_ENTRE_CREDITOS = 100
    TAMANHO_IMAGEM = (350, 350)
    
    # --- Caminhos para os assets (relativos à raiz do projeto "Jogo") ---
    # Assume que este script está em Jogo/Arquivos/
    caminho_base_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FONTE_RETRO_PATH = os.path.join(caminho_base_projeto, "Fontes", "Retro Gaming.ttf")
    MUSICA_CREDITOS_PATH = os.path.join(caminho_base_projeto, "Musica", "Creditos", "Creditos.mp3")
    
    dados_creditos = [
        {"nome": "Ayslan Araújo", "funcao": "Diretor, Produtor", "imagem": os.path.join(caminho_base_projeto, "Creditos", "Ayslan.jpg")},
        {"nome": "Andre Costa", "funcao": "Agradecimento Especial", "imagem": os.path.join(caminho_base_projeto, "Creditos", "Andre.jpg")},
        {"nome": "Caio Macedo", "funcao": "Agradecimento Especial", "imagem": os.path.join(caminho_base_projeto, "Creditos", "Caio.jpg")},
        {"nome": "Calebe de Oliveira", "funcao": "Agradecimento Especial", "imagem": os.path.join(caminho_base_projeto, "Creditos", "Calebe.jpg")},
        {"nome": "Felipe Hipolio", "funcao": "Agradecimento Especial", "imagem": os.path.join(caminho_base_projeto, "Creditos", "Felipe.jpg")},
        {"nome": "Raiane Oliveira", "funcao": "Agradecimento Especial", "imagem": os.path.join(caminho_base_projeto, "Creditos", "Raiane.jpg")},
        {"nome": "Caio Rangel", "funcao": "Agradecimento Especial", "imagem": os.path.join(caminho_base_projeto, "Creditos", "Rangel.jpg")},
    ]

    # Para a música do menu e toca a música dos créditos
    pygame.mixer.music.stop()
    if os.path.exists(MUSICA_CREDITOS_PATH):
        pygame.mixer.music.load(MUSICA_CREDITOS_PATH)
        pygame.mixer.music.play(-1)
    else:
        print(f"Erro: Música de créditos não encontrada em {MUSICA_CREDITOS_PATH}")

    # --- Configuração da Tela e Fonte ---
    largura_tela, altura_tela = tela.get_size()
    
    try:
        if not os.path.exists(FONTE_RETRO_PATH):
            raise FileNotFoundError(f"Arquivo de fonte não encontrado: {FONTE_RETRO_PATH}")

        fonte_nome = pygame.font.Font(FONTE_RETRO_PATH, TAMANHO_FONTE_NOME)
        fonte_funcao = pygame.font.Font(FONTE_RETRO_PATH, TAMANHO_FONTE_FUNCAO)
        fonte_iniciais = pygame.font.Font(FONTE_RETRO_PATH, 40)
    except (pygame.error, FileNotFoundError) as e:
        print(f"AVISO: Fonte personalizada não encontrada ou falhou ao carregar ({e}). Usando fonte padrão 'Arial'.")
        fonte_nome = pygame.font.SysFont("arial", TAMANHO_FONTE_NOME)
        fonte_funcao = pygame.font.SysFont("arial", TAMANHO_FONTE_FUNCAO)
        fonte_iniciais = pygame.font.SysFont("arial", 40, bold=True)

    # --- Carregamento e Preparação dos Créditos ---
    creditos_renderizados = []
    altura_total_creditos = 0
    for credito in dados_creditos:
        texto_nome = fonte_nome.render(credito["nome"], True, COR_TEXTO)
        texto_funcao = fonte_funcao.render(credito["funcao"], True, COR_TEXTO)

        try:
            imagem_original = pygame.image.load(credito["imagem"]).convert_alpha()
            imagem_escalada = pygame.transform.scale(imagem_original, TAMANHO_IMAGEM)
            
            imagem_circular = pygame.Surface(TAMANHO_IMAGEM, pygame.SRCALPHA)
            pygame.draw.circle(imagem_circular, (255, 255, 255), (TAMANHO_IMAGEM[0] // 2, TAMANHO_IMAGEM[1] // 2), TAMANHO_IMAGEM[0] // 2)
            imagem_circular.blit(imagem_escalada, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            imagem = imagem_circular
        except (pygame.error, FileNotFoundError):
            imagem = pygame.Surface(TAMANHO_IMAGEM, pygame.SRCALPHA)
            imagem.fill((0,0,0,0)) 
            cor_placeholder = (50, 50, 50)
            raio = TAMANHO_IMAGEM[0] // 2
            pygame.draw.circle(imagem, cor_placeholder, (raio, raio), raio)
            iniciais = "".join(p[0] for p in credito["nome"].split()[:2]).upper()
            texto_iniciais = fonte_iniciais.render(iniciais, True, COR_TEXTO)
            rect_texto = texto_iniciais.get_rect(center=(raio, raio))
            imagem.blit(texto_iniciais, rect_texto)

        creditos_renderizados.append({"nome": texto_nome, "funcao": texto_funcao, "imagem": imagem})
        altura_total_creditos += TAMANHO_IMAGEM[1] + texto_nome.get_height() + texto_funcao.get_height() + ESPACO_ENTRE_CREDITOS

    texto_final_surf = fonte_nome.render("Obrigado pela atenção!", True, COR_TEXTO)
    estado = "rolando"
    alpha_esmaecer = 0
    tempo_pausa_inicio = 0
    DURACAO_PAUSA = 2000

    posicao_y_inicial = altura_tela
    rodando_creditos = True
    while rodando_creditos:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                rodando_creditos = False

        largura_atual, altura_atual = tela.get_size()
        tela.fill(COR_FUNDO)

        posicao_y_atual = posicao_y_inicial
        
        for credito in creditos_renderizados:
            pos_x_imagem = (largura_atual - TAMANHO_IMAGEM[0]) // 2
            pos_x_nome = (largura_atual - credito["nome"].get_width()) // 2
            pos_x_funcao = (largura_atual - credito["funcao"].get_width()) // 2
            
            tela.blit(credito["imagem"], (pos_x_imagem, posicao_y_atual))
            posicao_y_atual += TAMANHO_IMAGEM[1] + 10
            tela.blit(credito["nome"], (pos_x_nome, posicao_y_atual))
            posicao_y_atual += credito["nome"].get_height() + 5
            tela.blit(credito["funcao"], (pos_x_funcao, posicao_y_atual))
            posicao_y_atual += credito["funcao"].get_height() + ESPACO_ENTRE_CREDITOS
        
        pos_y_final = posicao_y_atual + 50
        pos_x_final = (largura_atual - texto_final_surf.get_width()) // 2
        tela.blit(texto_final_surf, (pos_x_final, pos_y_final))

        if estado == "rolando":
            posicao_y_inicial -= VELOCIDADE_ROLAGEM
            if pos_y_final <= altura_atual // 2:
                ajuste = (altura_atual // 2) - pos_y_final
                posicao_y_inicial += ajuste
                estado = "pausado"
                tempo_pausa_inicio = pygame.time.get_ticks()

        elif estado == "pausado":
            if pygame.time.get_ticks() - tempo_pausa_inicio > DURACAO_PAUSA:
                estado = "esmaecendo"

        elif estado == "esmaecendo":
            alpha_esmaecer += 3
            if alpha_esmaecer >= 255:
                rodando_creditos = False
            
            fade_surface = pygame.Surface((largura_atual, altura_atual))
            fade_surface.fill(COR_FUNDO)
            fade_surface.set_alpha(alpha_esmaecer)
            tela.blit(fade_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop() # Para a música dos créditos
