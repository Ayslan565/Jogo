import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos

# Certifique-se de que Inimigo está acessível
try:
    # Tenta importar a classe base real.
    # Assumimos que 'Inimigos.py' está no mesmo diretório ou acessível via PYTHONPATH.
    from Inimigos import Inimigo 
    print("DEBUG(Vampiro): Classe base Inimigo importada com sucesso.")
except ImportError:
    print("DEBUG(Vampiro): ERRO: Módulo 'Inimigos.py' não encontrado. Usando classe Inimigo placeholder.")
    # Placeholder para Inimigo, caso Inimigos.py não seja encontrado
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
            self.sprite_path_base = sprite_path # Store the base path for reference

            # Path for _carregar_sprite should be relative to the script if this placeholder is used from Vampiro.py
            # However, Vampiro.py passes sprite_path_ref which is already "Sprites/Inimigos/Vampiro/..."
            # This placeholder's _carregar_sprite needs to handle that if it's to be truly general.
            # For now, it assumes 'sprite_path' is directly loadable or a simple file name.
            if os.path.exists(sprite_path): # Basic check if it's a direct file path
                try:
                    self.image = pygame.image.load(sprite_path).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (largura, altura))
                except pygame.error:
                    self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
                    pygame.draw.rect(self.image, (100, 100, 100), (0, 0, largura, altura)) # Placeholder color
            else: # If not a direct path, or if it was a directory like "Sprites/Inimigos/Vampiro/"
                  # Use the _carregar_sprite logic which expects a path relative to Vampiro.py's location
                  # This part is tricky because sprite_path_ref can be a directory.
                  # For simplicity, the placeholder will just draw a rect if complex path.
                self.image = self._carregar_sprite(sprite_path if not sprite_path.endswith('/') else sprite_path + "some_default_image.png", (largura, altura))


            self.rect = self.image.get_rect(topleft=(x, y))

            self.last_hit_time = 0
            self.hit_flash_duration = 150 # milliseconds
            self.hit_flash_color = (255, 255, 255, 128) # White flash with alpha

            self.is_attacking = False
            self.attack_hitbox = pygame.Rect(0, 0, 0, 0) 
            self.hit_by_player_this_attack = False 
            self.contact_cooldown = 1000 # milliseconds
            self.last_contact_time = pygame.time.get_ticks() # Initialize last contact time
            self.facing_right = True # Default facing direction

            # Animation attributes
            self.sprites = [self.image] # Default to a single sprite if not overridden
            self.sprite_index = 0 
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.intervalo_animacao = 200 # milliseconds

        def _carregar_sprite(self, path, tamanho):
            """
            Carrega um sprite de imagem do caminho especificado.
            Se o sprite não for encontrado ou houver um erro, retorna um placeholder.
            A resolução do caminho é relativa ao diretório deste arquivo (Vampiro.py, if called from there).
            IMPORTANT: This placeholder's loader assumes 'path' is relative to THIS SCRIPT's location,
            or it's a full path. Vampiro.py passes "Sprites/Inimigos/Vampiro[/filename.png]",
            which implies it should be relative to an asset root.
            """
            # This path logic is tricky for a generic placeholder when used by Vampiro.py's specific structure.
            # For robust loading, this should ideally know the game_assets_root_dir.
            # For this placeholder, we'll try a simple relative load from script dir.
            
            # Heuristic: if path starts with "Sprites/" or "Sons/", it's likely relative to an asset root.
            # This placeholder is too simple to correctly guess the asset root if Vampiro.py is nested.
            # It will likely fail to load complex paths like "Sprites/Inimigos/Vampiro/Imagem.png"
            # unless Vampiro.py is in the asset root itself.
            
            # Get the directory of the current file (Vampiro.py if this class is defined and used there)
            base_dir = os.path.dirname(os.path.abspath(__file__)) 
            
            # This placeholder assumes 'path' is relative to where Vampiro.py is.
            # This will NOT work correctly if Vampiro.py is in "Jogo/Inimigos" and 'path' is "Sprites/..."
            # because it will look for "Jogo/Inimigos/Sprites/..."
            # The Vampiro class itself has better loading logic.
            full_path = os.path.join(base_dir, path.replace("/", os.sep))

            if not os.path.exists(full_path):
                # Attempt to find it one level up if it looks like an asset path
                # This is a hack for the placeholder.
                if path.startswith("Sprites" + os.sep) or path.startswith("Sons" + os.sep):
                    alt_full_path = os.path.join(os.path.dirname(base_dir), path.replace("/", os.sep))
                    if os.path.exists(alt_full_path):
                        full_path = alt_full_path
                    else:
                        print(f"DEBUG(InimigoPlaceholder): Sprite não encontrado em '{full_path}' ou '{alt_full_path}'. Usando placeholder.")
                        img = pygame.Surface(tamanho, pygame.SRCALPHA)
                        pygame.draw.rect(img, (100,100,100), (0, 0, tamanho[0], tamanho[1]))
                        return img
                else:
                    print(f"DEBUG(InimigoPlaceholder): Sprite não encontrado em '{full_path}'. Usando placeholder.")
                    img = pygame.Surface(tamanho, pygame.SRCALPHA)
                    pygame.draw.rect(img, (100,100,100), (0, 0, tamanho[0], tamanho[1]))
                    return img
            try:
                img = pygame.image.load(full_path).convert_alpha()
                img = pygame.transform.scale(img, tamanho)
                return img
            except pygame.error as e:
                print(f"DEBUG(InimigoPlaceholder): Erro ao carregar sprite '{full_path}': {e}. Usando placeholder.")
                img = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(img, (100,100,100), (0, 0, tamanho[0], tamanho[1]))
                return img

        def receber_dano(self, dano):
            self.hp -= dano
            self.last_hit_time = pygame.time.get_ticks() # Record time of hit for flash effect
            if self.hp <= 0:
                self.hp = 0
                # self.kill() # Pygame sprite group removal

        def esta_vivo(self):
            return self.hp > 0

        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): 
            if self.esta_vivo() and self.velocidade > 0:
                dx = alvo_x - self.rect.centerx
                dy = alvo_y - self.rect.centery
                dist = math.hypot(dx, dy)
                
                fator_tempo = 1.0 # Default if dt_ms is not provided
                if dt_ms is not None and dt_ms > 0:
                    # Normalize speed based on delta time, assuming base speed is pixels per frame at 60 FPS
                    fator_tempo = (dt_ms / (1000.0 / 60.0)) 

                if dist > 0: # Check if not already at the target
                    dx_norm = dx / dist
                    dy_norm = dy / dist
                    self.rect.x += dx_norm * self.velocidade * fator_tempo
                    self.rect.y += dy_norm * self.velocidade * fator_tempo
                    
                    # Update facing direction based on movement
                    if dx > 0:
                        self.facing_right = True
                    elif dx < 0:
                        self.facing_right = False
        
        def atualizar_animacao(self):
            """
            Atualiza o sprite atual do inimigo para a animação.
            Garante que o sprite esteja virado para a direção correta.
            """
            agora = pygame.time.get_ticks()
            if self.sprites and len(self.sprites) > 1 and self.esta_vivo(): # Only animate if multiple sprites and alive
                if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                    self.tempo_ultimo_update_animacao = agora
                    self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            
            if self.sprites: # Ensure there are sprites to animate
                idx = int(self.sprite_index % len(self.sprites)) if len(self.sprites) > 0 else 0
                if idx < len(self.sprites):
                    base_image = self.sprites[idx]
                    if hasattr(self, 'facing_right') and not self.facing_right:
                        self.image = pygame.transform.flip(base_image, True, False)
                    else:
                        self.image = base_image
                elif len(self.sprites) > 0: # Fallback to first sprite if index is somehow out of bounds (should not happen with %)
                    self.image = self.sprites[0]
                # If self.sprites is empty, self.image remains as initialized (or from _carregar_sprite)
            elif not hasattr(self, 'image') or self.image is None: # Ensure self.image exists
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (100,100,100), (0,0,self.largura,self.altura))


        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            """
            Atualiza o estado do inimigo.
            Move em direção ao jogador e lida com dano por contato.
            """
            if self.esta_vivo():
                if hasattr(player, 'rect'): # Check if player object is valid
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
                self.atualizar_animacao()
                
                # Contact damage logic
                current_ticks = pygame.time.get_ticks()
                if hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                   self.rect.colliderect(player.rect) and \
                   (current_ticks - self.last_contact_time >= self.contact_cooldown):
                    if hasattr(player, 'receber_dano'):
                        player.receber_dano(self.contact_damage)
                        self.last_contact_time = current_ticks # Reset cooldown timer

        def desenhar(self, janela, camera_x, camera_y):
            """
            Desenha o inimigo na tela, aplicando o deslocamento da câmera.
            Inclui lógica para flash de dano e barra de vida.
            """
            if not hasattr(self, 'image') or self.image is None: # Ensure image exists
                # Fallback: Create a placeholder image if none is loaded
                self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                pygame.draw.rect(self.image, (100,100,100), (0,0,self.largura,self.altura))
                if not hasattr(self, 'rect'): # Ensure rect exists
                    self.rect = self.image.get_rect(topleft=(self.x, self.y))

            screen_x = self.rect.x - camera_x
            screen_y = self.rect.y - camera_y
            
            janela.blit(self.image, (screen_x, screen_y))

            # Damage flash effect
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time < self.hit_flash_duration:
                # Create a temporary surface for the flash effect
                flash_image_overlay = self.image.copy()
                # Fill with the flash color (RGB part) and use BLEND_RGB_ADD to lighten
                flash_image_overlay.fill(self.hit_flash_color[:3] + (0,), special_flags=pygame.BLEND_RGB_ADD) 
                # Set the alpha of the overlay for transparency
                flash_image_overlay.set_alpha(self.hit_flash_color[3]) 
                janela.blit(flash_image_overlay, (screen_x, screen_y))

            # Health bar
            if self.hp < self.max_hp and self.hp > 0: # Only draw if damaged but alive
                bar_width = self.largura
                bar_height = 5
                health_percentage = self.hp / self.max_hp
                current_bar_width = int(bar_width * health_percentage)
                
                bar_x = screen_x
                bar_y = screen_y - bar_height - 5 # Position above the sprite
                
                # Background of the health bar (red)
                pygame.draw.rect(janela, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height), border_radius=2) 
                # Current health (green)
                pygame.draw.rect(janela, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height), border_radius=2) 
                # Border for the health bar (white)
                pygame.draw.rect(janela, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=2) 


"""
Classe para o inimigo Vampiro.
Herda da classe base Inimigo.
"""
class Vampiro(Inimigo):
    # Variáveis de classe para armazenar sprites e sons carregados uma única vez
    sprites_originais = None 
    sprites_andar = None
    sprites_atacar = None
    sprites_idle = None # Opcional
    tamanho_sprite_definido = (80, 90) # Definir um tamanho padrão para os sprites do Vampiro

    som_ataque_vampiro = None
    som_dano_vampiro = None
    som_morte_vampiro = None
    som_spawn_vampiro = None 
    som_teleporte_vampiro = None 
    sons_carregados = False

    @staticmethod
    def _carregar_som_vampiro(caminho_relativo_a_raiz_assets):
        """
        Carrega um arquivo de som.
        O caminho_relativo_a_raiz_assets é relativo à pasta raiz de assets do jogo 
        (ex: 'Sons/Vampiro/som.wav').
        """
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        # Assume que este script (Vampiro.py) está em uma subpasta (ex: 'Inimigos')
        # da pasta raiz do jogo onde 'Sons' está localizada.
        # Ex: Jogo/
        #     ├── Sons/
        #     └── Inimigos/  <-- Vampiro.py está aqui
        #         └── Vampiro.py
        # game_assets_root_dir aponta para 'Jogo/'
        game_assets_root_dir = os.path.abspath(os.path.join(current_script_dir, ".."))
        
        full_path = os.path.join(game_assets_root_dir, caminho_relativo_a_raiz_assets.replace("/", os.sep))
        
        if not os.path.exists(full_path):
            print(f"DEBUG(Vampiro): Arquivo de som não encontrado: {full_path}")
            # Try an alternative path if the script is in the root asset folder itself
            alt_full_path = os.path.join(current_script_dir, caminho_relativo_a_raiz_assets.replace("/", os.sep))
            if os.path.exists(alt_full_path):
                full_path = alt_full_path
            else:
                print(f"DEBUG(Vampiro): Tentativa alternativa de caminho de som também falhou: {alt_full_path}")
                return None
                
        try:
            som = pygame.mixer.Sound(full_path)
            print(f"DEBUG(Vampiro): Som carregado com sucesso: {full_path}")
            return som
        except pygame.error as e:
            print(f"DEBUG(Vampiro): Erro ao carregar som '{full_path}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_assets, lista_destino, tamanho, tipo_animacao):
        """
        Método auxiliar estático para carregar uma lista de sprites.
        caminhos_relativos_a_raiz_assets são relativos à pasta raiz de assets do jogo 
        (ex: ['Sprites/Inimigos/Vampiro/img1.png', 'Sprites/Inimigos/Vampiro/img2.png']).
        """
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        # Mesma lógica de game_assets_root_dir como em _carregar_som_vampiro
        game_assets_root_dir = os.path.abspath(os.path.join(current_script_dir, ".."))
        
        for path_rel_a_assets in caminhos_relativos_a_raiz_assets:
            full_path = os.path.join(game_assets_root_dir, path_rel_a_assets.replace("/", os.sep))
            
            sprite_carregado = False
            if not os.path.exists(full_path):
                # Try an alternative path if the script is in the root asset folder itself
                # This makes it more flexible if Vampiro.py is in Jogo/ or Jogo/Inimigos/
                alt_full_path = os.path.join(current_script_dir, path_rel_a_assets.replace("/", os.sep))
                if os.path.exists(alt_full_path):
                    full_path = alt_full_path # Use alternative path
                else: # If both paths fail
                    print(f"DEBUG(Vampiro): Sprite {tipo_animacao} não encontrado em '{full_path}' ou '{alt_full_path}'. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                    pygame.draw.rect(placeholder, (100, 100, 120), placeholder.get_rect()) # Cor placeholder distinta
                    lista_destino.append(placeholder)
                    continue # Próximo sprite na lista
            
            try:
                sprite = pygame.image.load(full_path).convert_alpha()
                sprite = pygame.transform.scale(sprite, tamanho)
                lista_destino.append(sprite)
                sprite_carregado = True
                print(f"DEBUG(Vampiro): Sprite {tipo_animacao} carregado: {full_path}")
            except pygame.error as e:
                print(f"DEBUG(Vampiro): Erro ao carregar sprite {tipo_animacao} '{full_path}': {e}. Usando placeholder.")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (100, 100, 120), placeholder.get_rect())
                lista_destino.append(placeholder)
        
        if not lista_destino: # Se, após todas as tentativas, a lista ainda estiver vazia
            print(f"DEBUG(Vampiro): Nenhum sprite de {tipo_animacao} carregado. Usando placeholder final para {tipo_animacao}.")
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA)
            # Cor placeholder ainda mais distinta para "falha total"
            pygame.draw.rect(placeholder, (80, 80, 100), placeholder.get_rect()) 
            lista_destino.append(placeholder)

    @staticmethod
    def carregar_recursos_vampiro():
        """
        Carrega todos os recursos (sprites e sons) do Vampiro.
        Este método é estático e garante que os recursos sejam carregados apenas uma vez.
        Os caminhos para sprites e sons são relativos à pasta raiz de assets do jogo.
        """
        if Vampiro.sprites_andar is None: # Usando sprites_andar como flag principal para carregar sprites
            # Caminho base para os sprites do vampiro, relativo à pasta raiz de assets (ex: Jogo/)
            base_sprite_path_rel_assets = "Sprites/Inimigos/Vampiro/" 
            
            nomes_sprites_andar = ["Imagem.png", "Imagem1.png"] 
            Vampiro.sprites_andar = []
            Vampiro._carregar_lista_sprites_estatico(
                [base_sprite_path_rel_assets + nome for nome in nomes_sprites_andar], 
                Vampiro.sprites_andar, Vampiro.tamanho_sprite_definido, "Andar"
            )

            nomes_sprites_atacar = ["Imagem.png", "Imagem1.png"] # Usar os mesmos por enquanto
            Vampiro.sprites_atacar = []
            Vampiro._carregar_lista_sprites_estatico(
                [base_sprite_path_rel_assets + nome for nome in nomes_sprites_atacar],
                Vampiro.sprites_atacar, Vampiro.tamanho_sprite_definido, "Atacar"
            )
            if not Vampiro.sprites_atacar and Vampiro.sprites_andar:
                Vampiro.sprites_atacar = [Vampiro.sprites_andar[0]] # Fallback

            # Opcional: Sprites Idle
            # nomes_sprites_idle = ["Vampiro_Idle_1.png", "Vampiro_Idle_2.png"]
            # Vampiro.sprites_idle = []
            # Vampiro._carregar_lista_sprites_estatico(
            #     [base_sprite_path_rel_assets + nome for nome in nomes_sprites_idle],
            #     Vampiro.sprites_idle, Vampiro.tamanho_sprite_definido, "Idle"
            # )
            # if not Vampiro.sprites_idle and Vampiro.sprites_andar:
            #     Vampiro.sprites_idle = [Vampiro.sprites_andar[0]]


        if not Vampiro.sons_carregados:
            # Caminhos relativos à pasta raiz de assets (ex: Jogo/)
            Vampiro.som_ataque_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/ataque_mordida.wav") 
            Vampiro.som_dano_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/dano.wav")
            Vampiro.som_morte_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/morte_poeira.wav")
            Vampiro.som_spawn_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/spawn_risada.wav") 
            Vampiro.som_teleporte_vampiro = Vampiro._carregar_som_vampiro("Sons/Vampiro/teleporte_fumaca.wav")
            Vampiro.sons_carregados = True


    def __init__(self, x, y, velocidade=3.5): 
        Vampiro.carregar_recursos_vampiro() # Garante que os recursos sejam carregados

        vampiro_hp = 90
        vampiro_contact_damage = 8 
        vampiro_xp_value = 60
        sprite_path_ref = "Sprites/Inimigos/Vampiro/Vampiro_Walk_1.png" if Vampiro.sprites_andar else "placeholder_vampiro.png"

        super().__init__(x, y,
                         Vampiro.tamanho_sprite_definido[0], Vampiro.tamanho_sprite_definido[1],
                         vampiro_hp, velocidade, vampiro_contact_damage,
                         vampiro_xp_value, sprite_path_ref)

        self.sprites = Vampiro.sprites_andar if Vampiro.sprites_andar else [self.image] # Começa com animação de andar
        self.sprite_index = 0
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
        self.intervalo_animacao_andar = 120 
        self.intervalo_animacao_atacar = 90 # Ataque mais rápido
        self.intervalo_animacao = self.intervalo_animacao_andar # Padrão para andar

        self.is_attacking = False 
        self.attack_duration = 0.4 # segundos
        self.attack_timer = 0.0  # Usar time.time()
        self.attack_damage = 25   
        self.life_steal_percent = 0.3 
        self.attack_hitbox_size = (50, 50) # Largura, Altura da hitbox de ataque
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0) # Será inicializada no ataque
        self.attack_range = 80    # Distância para iniciar o ataque
        self.attack_cooldown = 1.8 # segundos
        self.last_attack_time = time.time() - self.attack_cooldown # Para poder atacar imediatamente

        self.can_dash = True
        self.dash_cooldown = 5.0 # segundos
        self.last_dash_time = time.time() - self.dash_cooldown # Para poder dar dash imediatamente
        self.dash_range = 200 # Distância do dash
        self.is_dashing = False
        self.dash_duration = 0.2 # segundos (duração do estado de dash)
        self.dash_timer = 0.0 # Usar time.time()
        self.dash_target_pos = None # Para onde o dash está indo (x, y)

        # Define a imagem inicial do sprite com base nos sprites carregados
        if self.sprites and len(self.sprites) > 0:
            idx = int(self.sprite_index % len(self.sprites))
            self.image = self.sprites[idx]
        # Se self.sprites estiver vazio (falha no carregamento), self.image já foi definido pelo super().__init__
        # ou pelo placeholder Inimigo. Se ainda assim for None, criar um Surface.
        elif not hasattr(self, 'image') or self.image is None:
            self.image = pygame.Surface(Vampiro.tamanho_sprite_definido, pygame.SRCALPHA)
            pygame.draw.rect(self.image, (100,100,120), (0,0,self.largura,self.altura)) # Cor de Vampiro placeholder
            if not hasattr(self, 'rect'): # Garante que o rect exista
                self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # Atualiza o rect se a imagem mudou
        if hasattr(self, 'image') and self.image is not None:
             self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))


        if Vampiro.som_spawn_vampiro:
            Vampiro.som_spawn_vampiro.play()

    def receber_dano(self, dano):
        vida_antes = self.hp
        super().receber_dano(dano) 
        if self.esta_vivo():
            if vida_antes > self.hp and Vampiro.som_dano_vampiro:
                Vampiro.som_dano_vampiro.play()
        else: # Morreu
            if vida_antes > 0 and Vampiro.som_morte_vampiro: # Toca som de morte apenas uma vez
                Vampiro.som_morte_vampiro.play()
                # Poderia adicionar self.kill() aqui se estiver em um grupo de sprites e quiser remover
                # self.kill() 

    def _perform_dash(self, player_x, player_y):
        self.is_dashing = True
        self.dash_timer = time.time() # Início do dash
        self.last_dash_time = self.dash_timer # Reseta cooldown do dash
        self.can_dash = False 

        if Vampiro.som_teleporte_vampiro:
            Vampiro.som_teleporte_vampiro.play()

        dx = player_x - self.rect.centerx
        dy = player_y - self.rect.centery
        dist_to_player = math.hypot(dx, dy)

        if dist_to_player > 0:
            # Dash na direção do jogador, até o dash_range
            self.dash_target_pos = (
                self.rect.centerx + (dx / dist_to_player) * self.dash_range,
                self.rect.centery + (dy / dist_to_player) * self.dash_range
            )
        else: # Se já estiver em cima do jogador, dash para uma posição aleatória próxima
            angle = random.uniform(0, 2 * math.pi)
            self.dash_target_pos = (
                self.rect.centerx + self.dash_range * 0.5 * math.cos(angle), # Dash mais curto
                self.rect.centery + self.dash_range * 0.5 * math.sin(angle)
            )
        # print(f"DEBUG(Vampiro): Dash para {self.dash_target_pos}")


    def atacar(self, player):
        if not hasattr(player, 'rect'):
            return

        current_time = time.time()
        if self.esta_vivo() and not self.is_attacking and not self.is_dashing and \
           (current_time - self.last_attack_time >= self.attack_cooldown):
            
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                             self.rect.centery - player.rect.centery)

            if distancia_ao_jogador <= self.attack_range:
                self.is_attacking = True
                self.attack_timer = current_time # Início do ataque
                self.last_attack_time = current_time # Reseta cooldown do ataque
                self.hit_by_player_this_attack = False # Reseta flag de acerto por ataque

                self.sprites = Vampiro.sprites_atacar if Vampiro.sprites_atacar else Vampiro.sprites_andar # Fallback
                self.intervalo_animacao = self.intervalo_animacao_atacar
                self.sprite_index = 0 # Reinicia animação de ataque

                # Inicializa a hitbox de ataque com o tamanho definido
                attack_hitbox_width = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[0]
                attack_hitbox_height = getattr(self, 'attack_hitbox_size', (self.rect.width, self.rect.height))[1]
                self.attack_hitbox = pygame.Rect(0, 0, attack_hitbox_width, attack_hitbox_height)
                # A hitbox será posicionada no update do ataque
                
                if Vampiro.som_ataque_vampiro:
                    Vampiro.som_ataque_vampiro.play()

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not (hasattr(player, 'rect') and hasattr(player, 'vida') and 
                hasattr(player.vida, 'esta_vivo') and hasattr(player, 'receber_dano')):
            if self.esta_vivo(): self.atualizar_animacao() 
            # print("DEBUG(Vampiro): Objeto player inválido ou faltando atributos.")
            return

        current_time_sec = time.time() # Tempo em segundos para timers de cooldown/duração
        dt_sec = dt_ms / 1000.0 if dt_ms is not None and dt_ms > 0 else (1.0/60.0) # Delta time em segundos

        if not self.can_dash and (current_time_sec - self.last_dash_time >= self.dash_cooldown):
            self.can_dash = True

        if self.is_dashing:
            if self.dash_target_pos:
                target_x, target_y = self.dash_target_pos
                dx = target_x - self.rect.centerx
                dy = target_y - self.rect.centery
                dist_to_target = math.hypot(dx, dy)
                
                # Velocidade de dash muito alta para parecer teleporte, ajustada por dt_sec
                # A "velocidade" aqui é mais um fator de quão rápido ele chega ao alvo dentro da dash_duration
                # Movimento linear simples para o alvo durante o dash
                dash_speed_pixels_per_sec = self.dash_range / self.dash_duration 
                
                move_x = (dx / dist_to_target) * dash_speed_pixels_per_sec * dt_sec if dist_to_target > 0 else 0
                move_y = (dy / dist_to_target) * dash_speed_pixels_per_sec * dt_sec if dist_to_target > 0 else 0

                # Evitar overshoot
                if abs(move_x) > abs(dx): move_x = dx
                if abs(move_y) > abs(dy): move_y = dy
                
                self.rect.x += move_x
                self.rect.y += move_y

                # Checa se chegou perto o suficiente ou se o tempo de dash acabou
                if dist_to_target < 10 or (current_time_sec - self.dash_timer >= self.dash_duration): # 10 pixels de tolerância
                    self.rect.centerx = target_x # Snap para o final
                    self.rect.centery = target_y
                    self.is_dashing = False
                    self.dash_target_pos = None
                    self.sprites = Vampiro.sprites_andar if Vampiro.sprites_andar else [self.image]
                    self.intervalo_animacao = self.intervalo_animacao_andar
            
            # Garantir que o dash termine após a duração máxima
            if current_time_sec - self.dash_timer >= self.dash_duration:
                self.is_dashing = False
                self.dash_target_pos = None # Limpa o alvo
                if not self.is_attacking: # Só muda se não estiver no meio de um ataque
                    self.sprites = Vampiro.sprites_andar if Vampiro.sprites_andar else [self.image]
                    self.intervalo_animacao = self.intervalo_animacao_andar
            
            self.atualizar_animacao()
            return # Não faz mais nada durante o dash

        # Comportamento normal (movimento e ataque) se não estiver em dash
        if not self.is_attacking:
            # Chama o update da classe base para movimento normal e dano de contato
            # A classe base Inimigo (placeholder ou real) deve lidar com dt_ms ou dt_sec
            # Passando dt_ms para manter consistência com a assinatura original
            super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)
        else: # Se estiver atacando, apenas atualiza a animação de ataque (movimento é pausado)
            self.atualizar_animacao()


        if self.esta_vivo():
            dist_to_player = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
            
            # Lógica para iniciar o dash
            # O vampiro dá dash se puder, não estiver atacando, e o jogador estiver a uma distância específica.
            if self.can_dash and not self.is_attacking and \
               dist_to_player > self.attack_range * 1.5 and dist_to_player < self.dash_range * 1.2: # Ajustar ranges
                # Chance de dash, ajustada pelo delta time para consistência
                # (0.02 chance per frame at 60fps) -> 0.02 * 60 = 1.2 chances per second on average
                if random.random() < (1.2 * dt_sec): 
                    self._perform_dash(player.rect.centerx, player.rect.centery)
                    return # Retorna para processar o dash no próximo frame

            # Lógica de ataque
            if self.is_attacking:
                # Posiciona a hitbox de ataque à frente do vampiro
                offset_x_hitbox = self.attack_hitbox_size[0] / 3 # Quão à frente a hitbox fica
                if self.facing_right:
                    self.attack_hitbox.centerx = self.rect.centerx + self.rect.width / 2 # Começa na borda do vampiro
                    self.attack_hitbox.centerx += offset_x_hitbox 
                else:
                    self.attack_hitbox.centerx = self.rect.centerx - self.rect.width / 2
                    self.attack_hitbox.centerx -= offset_x_hitbox
                self.attack_hitbox.centery = self.rect.centery

                # Verifica se o ataque terminou
                if current_time_sec - self.attack_timer >= self.attack_duration:
                    self.is_attacking = False
                    self.hit_by_player_this_attack = False # Reseta para o próximo ataque
                    self.sprites = Vampiro.sprites_andar if Vampiro.sprites_andar else [self.image]
                    self.intervalo_animacao = self.intervalo_animacao_andar
                else:
                    # Aplica dano e roubo de vida se a hitbox colidir com o jogador
                    if not self.hit_by_player_this_attack and self.attack_hitbox.colliderect(player.rect):
                        if player.vida.esta_vivo():
                            player.receber_dano(self.attack_damage)
                            vida_roubada = int(self.attack_damage * self.life_steal_percent)
                            self.hp = min(self.max_hp, self.hp + vida_roubada)
                            self.hit_by_player_this_attack = True # Só acerta uma vez por animação de ataque
            
            # Tenta atacar se não estiver em dash e não estiver já atacando
            if not self.is_attacking: # and not self.is_dashing (já tratado acima)
                # Garante que o sprite de andar seja usado se não houver idle específico
                # ou se acabou de sair de um ataque/dash
                current_animation_set = self.sprites
                expected_animation_set = Vampiro.sprites_idle if Vampiro.sprites_idle else Vampiro.sprites_andar
                
                if current_animation_set != expected_animation_set and \
                   current_animation_set != Vampiro.sprites_atacar : # Evita trocar se já estiver em ataque
                    self.sprites = expected_animation_set if expected_animation_set else [self.image]
                    self.intervalo_animacao = self.intervalo_animacao_andar # Ou um intervalo_animacao_idle
                    self.sprite_index = 0 # Reset animation

                self.atacar(player) # Tenta iniciar um novo ataque

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y) # Desenha o sprite e a barra de vida base
        
        # Opcional: Desenhar a hitbox de ataque para debug
        # if self.is_attacking and hasattr(self, 'attack_hitbox') and self.attack_hitbox.width > 0:
        #     debug_hitbox_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
        #     # Cria uma surface para a hitbox com transparência
        #     s = pygame.Surface((self.attack_hitbox.width, self.attack_hitbox.height), pygame.SRCALPHA)
        #     s.fill((180, 0, 0, 100))  # Vermelho semi-transparente
        #     surface.blit(s, (debug_hitbox_rect_onscreen.x, debug_hitbox_rect_onscreen.y))

