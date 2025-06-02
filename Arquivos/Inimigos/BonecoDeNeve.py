# BonecoDeNeve.py
import pygame
import os
import math
import time # Usado para cooldowns de ataque

# --- Importação da Classe Base Inimigo ---
# Assumimos que existe um arquivo 'Inimigos.py' na MESMA PASTA que este
# (Jogo/Arquivos/Inimigos/Inimigos.py) e que ele define a classe 'Inimigo' base.
# ESSA CLASSE 'Inimigo' BASE DEVE TER O MÉTODO _carregar_sprite CORRIGIDO
# para encontrar a raiz do jogo a partir de sua própria localização.
try:
    from .Inimigos import Inimigo as InimigoBase 
    # Se Inimigos.py se chama Inimigo.py, seria: from .Inimigo import Inimigo as InimigoBase
    print(f"DEBUG(BonecoDeNeve): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    print(f"DEBUG(BonecoDeNeve): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    # Este é um placeholder MUITO SIMPLES. A classe base real deve ser mais completa.
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((128, 128, 128, 100)) # Placeholder cinza
            pygame.draw.rect(self.image, (255,0,0), self.image.get_rect(), 1) # Borda vermelha
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0; 
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            print(f"DEBUG(InimigoBase Placeholder): Instanciado. Sprite path (não usado por este placeholder): {sprite_path}")
        
        # Métodos básicos para evitar AttributeError se a classe base real não for carregada
        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt=None): pass # Placeholder não se move
        def atualizar_animacao(self): pass # Placeholder não anima
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): pass
        def desenhar(self, janela, camera_x, camera_y): 
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

# --- Importação do Projétil ---
# Tenta importar ProjetilNeve. Se falhar, um placeholder será definido mais abaixo.
ProjetilNeve = None # Inicializa como None
try:
    # Assumindo que Projetil_BolaNeve.py está na mesma pasta (Jogo/Arquivos/Inimigos/)
    from .Projetil_BolaNeve import ProjetilNeve as ProjetilNeveReal
    ProjetilNeve = ProjetilNeveReal
    print("DEBUG(BonecoDeNeve): Classe ProjetilNeveReal importada com sucesso de .Projetil_BolaNeve.")
except ImportError:
    print("DEBUG(BonecoDeNeve): FALHA ao importar ProjetilNeveReal de .Projetil_BolaNeve. Placeholder será usado.")
except Exception as e:
    print(f"DEBUG(BonecoDeNeve): ERRO GERAL ao importar ProjetilNeveReal: {e}. Placeholder será usado.")


class BonecoDeNeve(InimigoBase):
    sprites_animacao = None # Cache para os sprites de animação (carregados uma vez)
    tamanho_sprite_definido = (70, 90) # Ajuste conforme o tamanho desejado do sprite

    @staticmethod
    def carregar_recursos():
        if BonecoDeNeve.sprites_animacao is not None: # Já carregado?
            return

        BonecoDeNeve.sprites_animacao = []
        # Caminhos dos sprites de animação RELATIVOS À PASTA RAIZ DO JOGO (ex: Jogo/)
        caminhos_relativos_sprites = [
            "Sprites/Inimigos/Boneco de Neve/Boneco De Neve 1.png",
            "Sprites/Inimigos/Boneco de Neve/Boneco de Neve 2.png",
            "Sprites/Inimigos/Boneco de Neve/Boneco de Neve 3.png",
        ]

        # Determina a pasta raiz do jogo a partir da localização deste arquivo (BonecoDeNeve.py)
        # __file__ aqui se refere a BonecoDeNeve.py
        diretorio_script_boneco = os.path.dirname(os.path.abspath(__file__))
        
        # Se BonecoDeNeve.py está em Jogo/Arquivos/Inimigos/
        # Para chegar na pasta raiz "Jogo/", subimos dois níveis.
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_boneco, "..", ".."))
        print(f"DEBUG(BonecoDeNeve.carregar_recursos): Pasta raiz do jogo calculada como: {pasta_raiz_jogo}")

        for path_relativo in caminhos_relativos_sprites:
            # Constrói o caminho absoluto para cada sprite de animação
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            print(f"DEBUG(BonecoDeNeve.carregar_recursos): Tentando carregar sprite de animação: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, BonecoDeNeve.tamanho_sprite_definido)
                    BonecoDeNeve.sprites_animacao.append(sprite)
                    print(f"DEBUG(BonecoDeNeve.carregar_recursos): Sprite de animação '{caminho_completo}' carregado.")
                else:
                    print(f"DEBUG(BonecoDeNeve.carregar_recursos): ARQUIVO DE ANIMAÇÃO NÃO EXISTE: {caminho_completo}. Usando placeholder visual (azul).")
                    placeholder = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder.fill((50, 50, 200, 180)) # Azul escuro para placeholder de animação
                    BonecoDeNeve.sprites_animacao.append(placeholder)
            except pygame.error as e:
                print(f"DEBUG(BonecoDeNeve.carregar_recursos): ERRO PYGAME ao carregar sprite de animação '{caminho_completo}': {e}. Usando placeholder visual (azul).")
                placeholder = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder.fill((50, 50, 200, 180))
                BonecoDeNeve.sprites_animacao.append(placeholder)
        
        if not BonecoDeNeve.sprites_animacao: # Fallback se nenhum sprite de animação foi carregado
            print("DEBUG(BonecoDeNeve.carregar_recursos): FALHA TOTAL em carregar sprites de animação. Usando placeholder final (azul mais escuro).")
            placeholder = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
            placeholder.fill((0, 0, 150, 200))
            BonecoDeNeve.sprites_animacao.append(placeholder)

    def __init__(self, x, y, velocidade=1.2): # Velocidade padrão para o BonecoDeNeve
        BonecoDeNeve.carregar_recursos() # Garante que os sprites de animação estão carregados

        vida_boneco = 70
        dano_contato_boneco = 7
        xp_boneco = 30
        # moedas_dropadas = 10
        
        # Este é o sprite_path principal que será passado para o construtor da InimigoBase.
        # A InimigoBase (com seu _carregar_sprite corrigido) é responsável por carregar este.
        # O caminho DEVE SER RELATIVO À PASTA RAIZ DO JOGO.
        sprite_path_principal_relativo_ao_jogo = "Sprites/Inimigos/Boneco de Neve/Boneco De Neve 1.png"

        super().__init__(
            x, y, 
            BonecoDeNeve.tamanho_sprite_definido[0], BonecoDeNeve.tamanho_sprite_definido[1], 
            vida_boneco, velocidade, dano_contato_boneco, xp_boneco,
            sprite_path_principal_relativo_ao_jogo 
        )

        # Define os sprites para animação desta instância
        # self.image já foi definido pelo super().__init__() se o sprite principal foi carregado
        self.sprites = BonecoDeNeve.sprites_animacao
        if not self.sprites or not isinstance(self.sprites[0], pygame.Surface): # Fallback crítico
            print("DEBUG(BonecoDeNeve __init__): Sprites de animação não carregados ou inválidos. Usando self.image como único sprite.")
            if hasattr(self, 'image') and isinstance(self.image, pygame.Surface):
                 self.sprites = [self.image]
            else: # Último recurso, cria um placeholder para self.image e self.sprites
                placeholder_img = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((100,0,0,100)) # Vermelho escuro para erro grave
                self.image = placeholder_img
                self.sprites = [self.image]


        self.sprite_index = 0
        # self.tempo_ultimo_update_animacao já é inicializado na InimigoBase
        self.intervalo_animacao = 250 # Intervalo específico para animação do BonecoDeNeve

        # Atributos específicos de ataque do BonecoDeNeve
        self.attack_damage = 12
        self.attack_range = 350      # Distância em pixels para iniciar o ataque
        self.attack_cooldown = 2.5   # Segundos entre tentativas de ataque
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000) # Permite atacar logo
        
        self.velocidade_projetil = 6 # Velocidade da bola de neve
        
        self.attack_prepare_duration = 500 # Milissegundos para "preparar" o tiro (ex: animação de arremesso)
        self.is_preparing_attack = False   # Flag se está na fase de preparação do ataque
        self.attack_prepare_start_time = 0 # Tempo em que a preparação do ataque começou

    # O método atualizar_animacao é herdado da InimigoBase.
    # O método mover_em_direcao é herdado da InimigoBase.
    # O método receber_dano é herdado e pode ser estendido se necessário.
    # O método desenhar é herdado.

    def update(self, player, projeteis_inimigos_ref, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            return

        agora = pygame.time.get_ticks()
        distancia_ao_jogador = float('inf')

        # Verifica se o jogador e seus atributos necessários existem
        jogador_valido = (hasattr(player, 'rect') and 
                          hasattr(player, 'vida') and 
                          hasattr(player.vida, 'esta_vivo') and 
                          player.vida.esta_vivo())

        if jogador_valido:
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, 
                                             self.rect.centery - player.rect.centery)

        # Lógica de Ataque com Projétil
        if self.is_preparing_attack:
            # Está preparando para atirar
            if agora - self.attack_prepare_start_time >= self.attack_prepare_duration:
                # Tempo de preparação terminou, atira!
                if jogador_valido and ProjetilNeve is not None: # Verifica se a classe ProjetilNeve está disponível
                    # Cria e adiciona o projétil
                    novo_projetil = ProjetilNeve(
                        self.rect.centerx, self.rect.centery,
                        player.rect.centerx, player.rect.centery,
                        self.attack_damage, self.velocidade_projetil
                    )
                    if hasattr(projeteis_inimigos_ref, 'add'): # Se for um pygame.sprite.Group
                        projeteis_inimigos_ref.add(novo_projetil)
                    # print(f"DEBUG(BonecoDeNeve): Atirou bola de neve!")
                
                self.is_preparing_attack = False # Sai do estado de preparação
                self.last_attack_time = agora    # Reseta o cooldown do ataque
        
        elif jogador_valido and distancia_ao_jogador <= self.attack_range and \
             (agora - self.last_attack_time >= self.attack_cooldown * 1000):
            # Condições para iniciar um novo ataque foram atendidas
            self.is_preparing_attack = True
            self.attack_prepare_start_time = agora
            # print(f"DEBUG(BonecoDeNeve): Preparando ataque. Dist: {distancia_ao_jogador:.0f}")
            # Aqui você poderia mudar para uma animação de "preparação de ataque" se tivesse uma

        # Movimento e Animação (herdado da InimigoBase)
        if not self.is_preparing_attack and jogador_valido: # Só se move se não estiver preparando para atirar
            self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
        
        self.atualizar_animacao() # Atualiza a animação (pode ser de andar ou de preparar ataque)
        
        # Dano de Contato (lógica da InimigoBase, mas precisa ser chamada ou replicada)
        # Se InimigoBase.update() não for chamado, ou se esta lógica não estiver lá:
        if jogador_valido and self.rect.colliderect(player.rect) and \
           (agora - self.last_contact_time >= self.contact_cooldown):
            if hasattr(player, 'receber_dano'):
                player.receber_dano(self.contact_damage)
                self.last_contact_time = agora


# --- Placeholder para ProjetilNeve ---
# Definido globalmente neste módulo se a importação de .Projetil_BolaNeve falhar.
if ProjetilNeve is None:
    print("DEBUG(BonecoDeNeve.py - Global): Usando placeholder GLOBAL para ProjetilNeve devido à falha no import.")
    class ProjetilNeve(pygame.sprite.Sprite): 
        def __init__(self, x_origem, y_origem, x_alvo, y_alvo, dano, velocidade=5, tamanho=10, cor=(200, 200, 255)):
            super().__init__()
            self.image = pygame.Surface((tamanho*2,tamanho*2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, cor, (tamanho, tamanho), tamanho)
            self.rect = self.image.get_rect(center=(x_origem,y_origem))
            self.dano = dano
            
            dx = x_alvo - x_origem
            dy = y_alvo - y_origem
            dist = math.hypot(dx,dy)
            
            if dist > 0:
                self.vel_x = (dx/dist) * velocidade
                self.vel_y = (dy/dist) * velocidade
            else: # Alvo está no mesmo lugar da origem, atira para cima por padrão
                self.vel_x = 0
                self.vel_y = -velocidade
            
            self.alive = True # Flag para controlar se o projétil está ativo
            # self.tempo_criacao = time.time() # Para possível tempo de vida
            # self.vida_util = 3 # Exemplo: projétil dura 3 segundos

        def update(self, player, tela_largura, tela_altura, dt_ms=None):
            if not self.alive: 
                return
            
            fator_tempo = 1.0
            if dt_ms is not None and dt_ms > 0:
                fator_tempo = (dt_ms / (1000.0 / 60.0)) # Ajusta para framerate

            self.rect.x += self.vel_x * fator_tempo
            self.rect.y += self.vel_y * fator_tempo
            
            # Colisão com jogador
            if hasattr(player, 'rect') and hasattr(player, 'vida') and \
               hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
               self.rect.colliderect(player.rect):
                if hasattr(player, 'receber_dano'):
                    player.receber_dano(self.dano)
                self.kill() # Remove de todos os grupos
                self.alive = False # Marca como não vivo
                return # Para de atualizar após colisão

            # Remoção se sair da tela (com uma margem)
            margem_tela = 100 
            if not (-margem_tela < self.rect.centerx < tela_largura + margem_tela and \
                    -margem_tela < self.rect.centery < tela_altura + margem_tela):
                self.kill()
                self.alive = False
            
            # Exemplo de tempo de vida
            # if time.time() - self.tempo_criacao > self.vida_util:
            # self.kill()
            # self.alive = False

        def desenhar(self, surface, camera_x, camera_y):
            if self.alive:
                surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

