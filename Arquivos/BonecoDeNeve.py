# BonecoDeNeve.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos

# Importa a classe base Inimigo do ficheiro Inimigos.py
# Certifique-se de que o ficheiro Inimigos.py está na mesma pasta ou num caminho acessível
try:
    from Inimigos import Inimigo
    # Tenta importar o projétil aqui também, se o BonecoDeNeve for atirar
    from Projetil_BolaNeve import ProjetilNeve 
    print("DEBUG(BonecoDeNeve): Classe Inimigo e ProjetilNeve importadas com sucesso.")
except ImportError:
    print("DEBUG(BonecoDeNeve): ERRO: Falha ao importar Inimigo ou ProjetilNeve. Usando placeholders.")
    # Define uma classe Inimigo placeholder mais completa para evitar NameError e AttributeError
    class Inimigo(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path):
            super().__init__()
            self.x = x
            self.y = y
            self.largura = largura
            self.altura = altura
            self.hp = vida_maxima 
            self.max_hp = vida_maxima 
            self.velocidade = velocidade 
            self.contact_damage = dano_contato
            self.xp_value = xp_value
            self.sprite_path_base = sprite_path 

            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), (0, 0, largura, altura)) 
            self.rect = self.image.get_rect(topleft=(x, y))

            self.last_hit_time = 0
            self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128) 

            self.is_attacking = False
            self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
            self.hit_by_player_this_attack = False
            self.contact_cooldown = 1000 
            self.last_contact_time = pygame.time.get_ticks()
            self.facing_right = True 
            
            self.sprites = [self.image] 
            self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.intervalo_animacao = 200


        def _carregar_sprite(self, path, tamanho): 
            base_dir = os.path.dirname(os.path.abspath(__file__))
             # Assumindo que BonecoDeNeve.py está numa subpasta e 'Sprites' na raiz
            game_root_dir = os.path.dirname(base_dir)
            # Se BonecoDeNeve.py e 'Sprites' estiverem na mesma pasta (raiz do projeto):
            # game_root_dir = base_dir
            full_path = os.path.join(game_root_dir, path.replace("\\", "/")) # Usa / para consistência
            
            print(f"--- DEBUG PLACEHOLDER TENTANDO CARREGAR (BonecoDeNeve): {full_path}")
            if not os.path.exists(full_path):
                print(f"DEBUG(InimigoPlaceholder - BonecoDeNeve): Sprite não encontrado: {full_path}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255, 0, 255), (0, 0, tamanho[0], tamanho[1]))
                return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error as e:
                print(f"DEBUG(InimigoPlaceholder - BonecoDeNeve): Erro ao carregar sprite '{full_path}': {e}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (255, 0, 255), (0, 0, tamanho[0], tamanho[1]))
                return img

        def receber_dano(self, dano, fonte_dano_rect=None): # Adicionado fonte_dano_rect para consistência
            self.hp -= dano
            self.last_hit_time = pygame.time.get_ticks()
            if self.hp <= 0:
                self.hp = 0

        def esta_vivo(self):
            return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): # Adicionado dt_ms
            if self.esta_vivo() and self.velocidade > 0:
                dx = alvo_x - self.rect.centerx
                dy = alvo_y - self.rect.centery
                dist = math.hypot(dx, dy)
                fator_tempo = 1.0
                if dt_ms is not None and dt_ms > 0:
                    fator_tempo = (dt_ms / (1000.0 / 60.0)) # Assume velocidade em px/frame @60FPS
                
                if dist > 0:
                    dx_norm = dx / dist
                    dy_norm = dy / dist
                    self.rect.x += dx_norm * self.velocidade * fator_tempo
                    self.rect.y += dy_norm * self.velocidade * fator_tempo
                    if dx > 0:
                        self.facing_right = True
                    elif dx < 0:
                        self.facing_right = False
        
        def atualizar_animacao(self): 
            agora = pygame.time.get_ticks()
            if self.sprites and len(self.sprites) > 1 and self.esta_vivo():
                if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                    self.tempo_ultimo_update_animacao = agora
                    self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            
            if self.sprites and len(self.sprites) > 0: 
                idx = int(self.sprite_index % len(self.sprites))
                if idx < len(self.sprites) and isinstance(self.sprites[idx], pygame.Surface): 
                    base_image = self.sprites[idx]
                    self.image = pygame.transform.flip(base_image, not self.facing_right, False)
                elif isinstance(self.sprites[0], pygame.Surface):
                    self.image = pygame.transform.flip(self.sprites[0], not self.facing_right, False)
            # Se não, self.image mantém o placeholder do __init__ ou o último sprite válido


        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): # Adicionado dt_ms
            if self.esta_vivo():
                if hasattr(player, 'rect'):
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
                self.atualizar_animacao() 
                
                current_ticks = pygame.time.get_ticks()
                if hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                   self.rect.colliderect(player.rect) and \
                   (current_ticks - self.last_contact_time >= self.contact_cooldown):
                    if hasattr(player, 'receber_dano'):
                        player.receber_dano(self.contact_damage)
                        self.last_contact_time = current_ticks

        def desenhar(self, janela, camera_x, camera_y):
            if not hasattr(self, 'image') or self.image is None or not isinstance(self.image, pygame.Surface):
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (255,0,255,128), (0,0,self.largura,self.altura))
                if not hasattr(self, 'rect'): self.rect = self.image.get_rect(topleft=(self.x,self.y))

            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            janela.blit(self.image, (screen_x, screen_y))

            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time < self.hit_flash_duration and hasattr(self, 'image') and self.image:
                flash_overlay = self.image.copy()
                flash_overlay.fill(self.hit_flash_color[:3] + (0,), special_flags=pygame.BLEND_RGB_ADD)
                flash_overlay.set_alpha(self.hit_flash_color[3])
                janela.blit(flash_overlay, (screen_x, screen_y))

            if self.hp < self.max_hp and self.hp > 0: # Mostra barra de vida apenas se não estiver com HP máximo e estiver vivo
                bar_w = self.largura; bar_h = 5
                health_p = self.hp / self.max_hp
                curr_bar_w = int(bar_w * health_p)
                bar_x = screen_x; bar_y = screen_y - bar_h - 5 
                pygame.draw.rect(janela, (255,0,0), (bar_x, bar_y, bar_w, bar_h),0,2)
                pygame.draw.rect(janela, (0,255,0), (bar_x, bar_y, curr_bar_w, bar_h),0,2)
                pygame.draw.rect(janela, (255,255,255), (bar_x, bar_y, bar_w, bar_h),1,2)

    # Placeholder para ProjetilNeve ajustado para a nova assinatura
    # Este placeholder só é usado se a importação de Projetil_BolaNeve.py falhar
    if 'ProjetilNeve' not in globals(): # Verifica se ProjetilNeve não foi importado com sucesso
        print("DEBUG(BonecoDeNeve): Usando placeholder INTERNO para ProjetilNeve.")
        class ProjetilNeve(pygame.sprite.Sprite): 
            def __init__(self, x_origem, y_origem, x_alvo, y_alvo, dano, velocidade=5, tamanho=10, cor=(200, 200, 255)):
                super().__init__()
                self.image = pygame.Surface((tamanho*2,tamanho*2), pygame.SRCALPHA)
                pygame.draw.circle(self.image, cor, (tamanho, tamanho), tamanho)
                self.rect = self.image.get_rect(center=(x_origem,y_origem))
                self.dano = dano
                self.velocidade_magnitude = velocidade
                dx = x_alvo - x_origem
                dy = y_alvo - y_origem
                dist = math.hypot(dx,dy)
                if dist > 0:
                    self.vel_x = (dx/dist) * self.velocidade_magnitude
                    self.vel_y = (dy/dist) * self.velocidade_magnitude
                else:
                    self.vel_x = 0
                    self.vel_y = -self.velocidade_magnitude # Default para cima
                self.alive = True
                self.tempo_criacao = time.time()
                self.vida_util = 5
                self.atingiu = False
            def update(self, player, tela_largura, tela_altura, dt_ms=None): # Adicionado dt_ms para consistência
                if not self.alive: return
                
                fator_tempo = 1.0
                if dt_ms is not None and dt_ms > 0:
                    fator_tempo = (dt_ms / (1000.0 / 60.0))

                self.rect.x += self.vel_x * fator_tempo
                self.rect.y += self.vel_y * fator_tempo
                
                if not self.atingiu and hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and self.rect.colliderect(player.rect):
                    if hasattr(player, 'receber_dano'):
                        player.receber_dano(self.dano)
                        self.atingiu = True
                if self.rect.right < 0 or self.rect.left > tela_largura or \
                   self.rect.bottom < 0 or self.rect.top > tela_altura or \
                   self.atingiu or (time.time() - self.tempo_criacao > self.vida_util):
                    self.kill()
                    self.alive = False
            def desenhar(self, surface, camera_x, camera_y):
                if self.alive:
                    surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))


"""
Classe para o inimigo Boneco de Neve.
Herda da classe base Inimigo.
"""
class BonecoDeNeve(Inimigo):
    sprites_carregados = None # Sprites para animação de andar/idle
    # Adicionar sprites_atacar_carregados se tiver animação de ataque separada
    # sprites_atacar_carregados = None 
    tamanho_sprite_definido = (80, 80) 

    # Sons (adicionar se necessário, seguindo o padrão de outras classes)
    # som_ataque_boneco = None
    # som_dano_boneco = None
    # som_morte_boneco = None
    # sons_carregados_boneco = False # Flag para sons

    # @staticmethod
    # def carregar_recursos_boneco_neve():
    # # Carregar sprites e sons aqui
    # pass

    def __init__(self, x, y, velocidade=1.0): 
        # BonecoDeNeve.carregar_recursos_boneco_neve() # Chamaria o carregamento de recursos

        boneco_hp = 80
        boneco_contact_damage = 7
        boneco_xp_value = 30
        sprite_path_principal = "Sprites/Inimigos/Boneco de Neve/Boneco De Neve 1.png" 

        if BonecoDeNeve.sprites_carregados is None:
            caminhos = [
                sprite_path_principal, 
                "Sprites/Inimigos/Boneco de Neve/Boneco de Neve 2.png",
                "Sprites/Inimigos/Boneco de Neve/Boneco de Neve 3.png",
                # Adicione mais frames se tiver
            ]
            BonecoDeNeve.sprites_carregados = []
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            # Assumindo que BonecoDeNeve.py está numa subpasta e 'Sprites' na raiz
            game_root_dir = os.path.dirname(current_file_dir) 
            # Se BonecoDeNeve.py e 'Sprites' estiverem na mesma pasta (raiz do projeto):
            # game_root_dir = current_file_dir

            for path in caminhos:
                full_path = os.path.join(game_root_dir, path.replace("\\", "/")) # Usa / para consistência
                print(f"--- TENTANDO CARREGAR SPRITE BONECONEVE: {full_path}")
                try:
                    if os.path.exists(full_path):
                        sprite = pygame.image.load(full_path).convert_alpha()
                        sprite = pygame.transform.scale(sprite, BonecoDeNeve.tamanho_sprite_definido)
                        BonecoDeNeve.sprites_carregados.append(sprite)
                        print(f"--- SUCESSO: Sprite '{full_path}' carregado.")
                    else:
                        print(f"!!! ARQUIVO NÃO EXISTE (BonecoDeNeve): {full_path}. Usando placeholder.")
                        placeholder = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
                        pygame.draw.rect(placeholder, (0, 100, 200), (0, 0, BonecoDeNeve.tamanho_sprite_definido[0], BonecoDeNeve.tamanho_sprite_definido[1]))
                        BonecoDeNeve.sprites_carregados.append(placeholder)
                except pygame.error as e:
                    print(f"!!! ERRO PYGAME (BonecoDeNeve) ao carregar '{full_path}': {e}. Usando placeholder.")
                    placeholder = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (0, 100, 200), (0, 0, BonecoDeNeve.tamanho_sprite_definido[0], BonecoDeNeve.tamanho_sprite_definido[1]))
                    BonecoDeNeve.sprites_carregados.append(placeholder)
            
            if not BonecoDeNeve.sprites_carregados:
                print("!!! FALHA TOTAL (BonecoDeNeve): Nenhum sprite carregado. Usando placeholder final.")
                placeholder = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (0, 80, 180), (0, 0, BonecoDeNeve.tamanho_sprite_definido[0], BonecoDeNeve.tamanho_sprite_definido[1]))
                BonecoDeNeve.sprites_carregados.append(placeholder)

        super().__init__(x, y, 
                         BonecoDeNeve.tamanho_sprite_definido[0], BonecoDeNeve.tamanho_sprite_definido[1], 
                         boneco_hp, velocidade, boneco_contact_damage,
                         boneco_xp_value, sprite_path_principal)

        self.sprites = BonecoDeNeve.sprites_carregados 
        self.sprite_index = 0 
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() 
        self.intervalo_animacao = 200 # Intervalo para animação de andar/idle

        # Atributos para ataque com projétil
        self.is_attacking = False # Indica se está na "animação" ou preparação para atirar
        self.attack_duration = 0.5 # Duração da "animação" antes de atirar (em segundos)
        self.attack_timer = 0.0    # Timer para controlar a attack_duration
        self.attack_damage = 12    # Dano da bola de neve
        self.attack_range = 300    # Alcance para começar a "preparar" o tiro
        self.attack_cooldown = 2.0 # Cooldown entre tentativas de ataque (em segundos)
        self.last_attack_time = time.time() - self.attack_cooldown # Permite atacar logo no início

        self.velocidade_projetil = 7 # Velocidade específica para a bola de neve
        self.shoot_projectile_flag = False # Sinaliza que um projétil deve ser disparado

        # Define a imagem inicial corretamente
        if self.sprites and len(self.sprites) > 0 and isinstance(self.sprites[0], pygame.Surface):
            self.image = self.sprites[0]
        elif hasattr(super(), 'image') and isinstance(super().image, pygame.Surface):
            self.image = super().image
        else: # Fallback se tudo falhar
            self.image = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (0, 100, 200), self.image.get_rect())
        
        # Garante que self.rect seja definido com as dimensões corretas da imagem inicial
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


    def receber_dano(self, dano, fonte_dano_rect=None): # Adicionado fonte_dano_rect
        super().receber_dano(dano) # Chama o método da classe base
        # Adicionar som de dano específico do BonecoDeNeve aqui, se houver

    # atualizar_animacao e mover_em_direcao são herdados da classe base Inimigo.
    # Se precisar de comportamento específico, pode sobrescrevê-los.

    def atacar(self, player):
        """Prepara o Boneco de Neve para atirar uma bola de neve."""
        if not hasattr(player, 'rect'):
            return

        current_time = time.time()
        if self.esta_vivo() and not self.is_attacking and \
           (current_time - self.last_attack_time >= self.attack_cooldown):
            
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                             self.rect.centery - player.rect.centery)

            if distancia_ao_jogador <= self.attack_range: 
                self.is_attacking = True # Entra no estado de "preparação" ou "animação de ataque"
                self.attack_timer = current_time # Inicia o timer para a duração da preparação
                self.last_attack_time = current_time # Reseta o cooldown para o próximo ciclo de ataque
                self.shoot_projectile_flag = True # Define que um projétil será disparado
                # print(f"DEBUG(BonecoDeNeve): Preparando para atirar. Dist: {distancia_ao_jogador:.0f}")
                # Mudar para sprites de ataque aqui, se tiver:
                # self.sprites = BonecoDeNeve.sprites_atacar_carregados 
                # self.intervalo_animacao = self.intervalo_animacao_atacar
                # self.sprite_index = 0 
                
    def update(self, player, projeteis_inimigos_ref, tela_largura=None, altura_tela=None, dt_ms=None): # dt_ms adicionado
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or \
           not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            if self.esta_vivo(): self.atualizar_animacao()
            return

        # Movimento e animação base são tratados pelo super().update()
        # O Boneco de Neve pode parar de se mover enquanto prepara o tiro
        if not self.is_attacking:
            try:
                super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)
            except TypeError:
                super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela)
        else: # Se está "atacando" (preparando para atirar), apenas anima
            self.atualizar_animacao()


        if self.esta_vivo():
            current_time_ataque = time.time()

            if self.is_attacking: # Se está na fase de "preparar/animar o ataque"
                if current_time_ataque - self.attack_timer >= self.attack_duration:
                    # Duração da preparação/animação terminou, agora atira
                    if self.shoot_projectile_flag: 
                        if projeteis_inimigos_ref is not None and ProjetilNeve is not None: 
                            start_x = self.rect.centerx
                            start_y = self.rect.centery
                            target_x = player.rect.centerx
                            target_y = player.rect.centery
                            
                            novo_projetil = ProjetilNeve(start_x, start_y, 
                                                         target_x, target_y, 
                                                         self.attack_damage, 
                                                         self.velocidade_projetil)
                            
                            # --- CORREÇÃO DO BUG ---
                            if hasattr(projeteis_inimigos_ref, 'add'):
                                projeteis_inimigos_ref.add(novo_projetil) # USA .add() PARA GRUPOS
                            elif isinstance(projeteis_inimigos_ref, list):
                                projeteis_inimigos_ref.append(novo_projetil) # Mantém .append() se for uma lista
                            else:
                                print(f"DEBUG(BonecoDeNeve): ERRO - projeteis_inimigos_ref (tipo: {type(projeteis_inimigos_ref)}) não é lista nem grupo com 'add'.")
                            # --- FIM DA CORREÇÃO ---
                            
                            # print(f"DEBUG(BonecoDeNeve): Atirou bola de neve!")
                        self.shoot_projectile_flag = False 
                    self.is_attacking = False # Termina o estado de ataque/preparação
                    # Voltar para sprites de andar/idle, se mudou para sprites de ataque
                    # self.sprites = BonecoDeNeve.sprites_carregados 
                    # self.intervalo_animacao = self.intervalo_animacao_andar
                    # self.sprite_index = 0
            
            # Se não estiver "preparando o ataque", verifica se pode iniciar um
            if not self.is_attacking:
                # Garante que está usando os sprites corretos se não estiver atacando
                # if self.sprites != BonecoDeNeve.sprites_carregados:
                # self.sprites = BonecoDeNeve.sprites_carregados
                # self.intervalo_animacao = self.intervalo_animacao_andar
                self.atacar(player) # Tenta iniciar a preparação do ataque

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y)
        # Não há necessidade de desenhar hitbox de ataque aqui, pois é um projétil
