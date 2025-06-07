# Espantalho.py
import pygame
import os
import math
import time

# --- Importação da Classe Base Inimigo ---
# Assume que existe um arquivo 'Inimigos.py' na MESMA PASTA que este
# (Jogo/Arquivos/Inimigos/Inimigos.py) e que ele define a classe 'Inimigo' base.
# Essa classe base é referenciada como 'InimigoBase' aqui.
try:
    from .Inimigos import Inimigo as InimigoBase
    # print(f"DEBUG(Espantalho): Classe InimigoBase importada com sucesso de .Inimigos.")
except ImportError as e:
    # print(f"DEBUG(Espantalho): FALHA ao importar InimigoBase de .Inimigos: {e}. Usando placeholder local MUITO BÁSICO.")
    # Este é um placeholder MUITO SIMPLES. A classe base real deve ser mais completa
    # e ter o método _carregar_sprite principal.
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.image.fill((100, 100, 100, 100)) # Placeholder cinza escuro
            pygame.draw.rect(self.image, (255,165,0), self.image.get_rect(), 1) # Borda laranja
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.facing_right = True; self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128)
            self.contact_cooldown = 1000; self.last_contact_time = 0
            self.sprites = [self.image]; self.sprite_index = 0;
            self.intervalo_animacao = 200; self.tempo_ultimo_update_animacao = 0
            # print(f"DEBUG(InimigoBase Placeholder para Espantalho): Instanciado. Sprite path (não usado por este placeholder): {sprite_path}")

        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, ax, ay, dt=None): pass
        def atualizar_animacao(self):
            if self.sprites and len(self.sprites) > 0:
                self.image = self.sprites[0] # Mostra o primeiro (e único) sprite do placeholder
        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): self.atualizar_animacao()
        def desenhar(self, janela, camera_x, camera_y):
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))


class Espantalho(InimigoBase):
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (120, 160) # Ajuste o tamanho conforme necessário

    som_ataque_espantalho = None
    som_dano_espantalho = None
    som_morte_espantalho = None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Calcula e retorna o caminho para a pasta raiz do jogo (ex: 'Jogo/')."""
        # __file__ aqui se refere a Espantalho.py
        diretorio_script_espantalho = os.path.dirname(os.path.abspath(__file__))
        # Se Espantalho.py está em Jogo/Arquivos/Inimigos/
        # Para chegar na pasta raiz "Jogo/", subimos dois níveis.
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_espantalho, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_espantalho(caminho_relativo_a_raiz_jogo):
        pasta_raiz_jogo = Espantalho._obter_pasta_raiz_jogo()
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", "/"))

        if not os.path.exists(caminho_completo):
            # print(f"DEBUG(Espantalho._carregar_som): Arquivo de som NÃO ENCONTRADO: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            # print(f"DEBUG(Espantalho._carregar_som): Som '{caminho_completo}' carregado.")
            return som
        except pygame.error as e:
            # print(f"DEBUG(Espantalho._carregar_som): ERRO PYGAME ao carregar som '{caminho_completo}': {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino, tamanho_sprite, nome_animacao):
        pasta_raiz_jogo = Espantalho._obter_pasta_raiz_jogo()
        # print(f"DEBUG(Espantalho._carregar_lista_sprites): Carregando sprites de '{nome_animacao}'. Raiz do jogo: {pasta_raiz_jogo}")

        if lista_destino is None: # Garante que a lista de destino exista
            lista_destino = []

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", "/"))
            # print(f"DEBUG(Espantalho._carregar_lista_sprites): Tentando carregar '{nome_animacao}' sprite: {caminho_completo}")
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho_sprite)
                    lista_destino.append(sprite)
                    # print(f"DEBUG(Espantalho._carregar_lista_sprites): Sprite '{caminho_completo}' carregado para '{nome_animacao}'.")
                else:
                    # print(f"DEBUG(Espantalho._carregar_lista_sprites): ARQUIVO NÃO EXISTE para '{nome_animacao}': {caminho_completo}. Usando placeholder (marrom).")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((139, 69, 19, 180)) # Cor de palha/marrom
                    lista_destino.append(placeholder)
            except pygame.error as e:
                # print(f"DEBUG(Espantalho._carregar_lista_sprites): ERRO PYGAME ao carregar '{nome_animacao}' sprite '{caminho_completo}': {e}. Usando placeholder (marrom).")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((139, 69, 19, 180))
                lista_destino.append(placeholder)

        if not lista_destino: # Fallback se a lista ainda estiver vazia
            # print(f"DEBUG(Espantalho._carregar_lista_sprites): FALHA TOTAL em carregar sprites para '{nome_animacao}'. Usando placeholder final (marrom escuro).")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((100, 50, 10, 200))
            lista_destino.append(placeholder)
        return lista_destino


    @staticmethod
    def carregar_recursos_espantalho():
        if Espantalho.sprites_andar_carregados is None: # Flag principal para carregar tudo uma vez
            Espantalho.sprites_andar_carregados = [] # Inicializa a lista
            caminhos_andar = [
                "Sprites/Inimigos/Espantalho/Espantalho.png",
                "Sprites/Inimigos/Espantalho/Espantalho 2.png",
                "Sprites/Inimigos/Espantalho/Espantalho 3.png",
            ]
            Espantalho.sprites_andar_carregados = Espantalho._carregar_lista_sprites_estatico(
                caminhos_andar,
                Espantalho.sprites_andar_carregados,
                Espantalho.tamanho_sprite_definido,
                "Andar/Idle"
            )

            # Exemplo para sprites de ataque (descomente e ajuste os caminhos se tiver)
            # Espantalho.sprites_atacar_carregados = []
            # caminhos_atacar = [
            #     "Sprites/Inimigos/Espantalho/Espantalho_Atk1.png",
            #     "Sprites/Inimigos/Espantalho/Espantalho_Atk2.png",
            # ]
            # Espantalho.sprites_atacar_carregados = Espantalho._carregar_lista_sprites_estatico(
            #     caminhos_atacar,
            #     Espantalho.sprites_atacar_carregados,
            #     Espantalho.tamanho_sprite_definido,
            #     "Atacar"
            # )
            # Fallback para ataque se não houver sprites específicos de ataque
            if not Espantalho.sprites_atacar_carregados and Espantalho.sprites_andar_carregados:
                 Espantalho.sprites_atacar_carregados = [Espantalho.sprites_andar_carregados[0]] # Usa o primeiro frame de andar

        if not Espantalho.sons_carregados:
            # Espantalho.som_ataque_espantalho = Espantalho._carregar_som_espantalho("Sons/Espantalho/ataque.wav")
            # Espantalho.som_dano_espantalho = Espantalho._carregar_som_espantalho("Sons/Espantalho/dano.wav")
            # Espantalho.som_morte_espantalho = Espantalho._carregar_som_espantalho("Sons/Espantalho/morte.wav")
            Espantalho.sons_carregados = True


    def __init__(self, x, y, velocidade=1.3):
        Espantalho.carregar_recursos_espantalho() # Garante que os recursos da classe estão carregados

        vida_espantalho = 85
        dano_contato_espantalho = 5
        xp_espantalho = 20
        self.moedas_drop = 11 # Quantidade de moedas que o Espantalho dropa

        # O sprite_path principal deve ser relativo à pasta raiz do jogo.
        # A classe InimigoBase (herdada) usará seu método _carregar_sprite para carregá-lo.
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Espantalho/Espantalho.png"

        super().__init__(
            x, y,
            Espantalho.tamanho_sprite_definido[0], Espantalho.tamanho_sprite_definido[1],
            vida_espantalho, velocidade, dano_contato_espantalho,
            xp_espantalho, sprite_path_principal_relativo_jogo
        )

        # Define os sprites para animação desta instância
        self.sprites_andar = Espantalho.sprites_andar_carregados
        self.sprites_atacar = Espantalho.sprites_atacar_carregados if Espantalho.sprites_atacar_carregados else self.sprites_andar

        # Define a lista de sprites atual (para o método atualizar_animacao da base)
        self.sprites = self.sprites_andar # Começa com animação de andar/idle

        # Garante que self.image e self.sprites[0] são válidos após o super().__init__
        if not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            # print("DEBUG(Espantalho __init__): self.image não foi definido corretamente pelo super(). Usando primeiro sprite de animação.")
            if self.sprites and isinstance(self.sprites[0], pygame.Surface):
                self.image = self.sprites[0]
            else: # Fallback crítico
                placeholder_img = pygame.Surface(Espantalho.tamanho_sprite_definido, pygame.SRCALPHA)
                placeholder_img.fill((100, 50, 10, 150)) # Marrom escuro para erro
                self.image = placeholder_img
                if not self.sprites: self.sprites = [self.image] # Garante que self.sprites não é None ou vazio

        self.rect = self.image.get_rect(topleft=(self.x, self.y)) # Reafirma o rect com a imagem correta

        self.sprite_index = 0
        # self.tempo_ultimo_update_animacao já é inicializado na InimigoBase
        self.intervalo_animacao_andar = 220
        self.intervalo_animacao_atacar = 150
        self.intervalo_animacao = self.intervalo_animacao_andar # Começa com o intervalo de andar

        # Atributos específicos de ataque do Espantalho (ataque corpo a corpo)
        self.is_attacking = False
        self.attack_duration = 0.6 # Duração da animação/hitbox de ataque (s)
        self.attack_timer = 0.0
        self.attack_damage_especifico = 10 # Dano do ataque específico (não o de contato)
        self.attack_hitbox_size = (Espantalho.tamanho_sprite_definido[0] * 0.6, Espantalho.tamanho_sprite_definido[1] * 0.5) # Tamanho da hitbox de ataque
        self.attack_hitbox_offset_x = Espantalho.tamanho_sprite_definido[0] * 0.4 # Distância à frente para a hitbox
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.attack_range = 80 # Distância para iniciar o ataque (pixels)
        self.attack_cooldown = 2.0 # Segundos entre ataques
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)
        self.hit_player_this_swing = False # Garante que o ataque acerta apenas uma vez por "swing"

    # O método receber_dano é herdado. Pode adicionar sons aqui.
    # O método atualizar_animacao é herdado, mas pode ser ajustado para trocar entre sets de sprites.
    # O método mover_em_direcao é herdado, mas pode ser ajustado para parar durante o ataque.

    def _atualizar_hitbox_ataque(self):
        """Atualiza a posição da hitbox de ataque baseada na direção do espantalho."""
        if not self.is_attacking:
            self.attack_hitbox.size = (0,0) # Zera a hitbox se não estiver atacando
            return

        w, h = self.attack_hitbox_size
        if self.facing_right:
            # Hitbox à direita do espantalho
            self.attack_hitbox.size = (w,h)
            self.attack_hitbox.midleft = (self.rect.right, self.rect.centery)
        else:
            # Hitbox à esquerda do espantalho
            self.attack_hitbox.size = (w,h)
            self.attack_hitbox.midright = (self.rect.left, self.rect.centery)


    def atacar(self, player):
        """Inicia a sequência de ataque do Espantalho."""
        if not (hasattr(player, 'rect') and self.esta_vivo()):
            return

        agora = pygame.time.get_ticks()
        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx,
                                         self.rect.centery - player.rect.centery)

        if not self.is_attacking and \
           distancia_ao_jogador <= self.attack_range and \
           (agora - self.last_attack_time >= self.attack_cooldown * 1000):

            self.is_attacking = True
            self.attack_timer = agora # Inicia o timer da duração do ataque
            self.last_attack_time = agora # Reseta o cooldown para o próximo ataque
            self.hit_player_this_swing = False # Reseta a flag de acerto para este ataque

            self.sprites = self.sprites_atacar # Muda para sprites de ataque
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0 # Reinicia a animação de ataque
            # print(f"DEBUG(Espantalho): Iniciando ataque! Dist: {distancia_ao_jogador:.0f}")
            # if Espantalho.som_ataque_espantalho: Espantalho.som_ataque_espantalho.play()


    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        if not self.esta_vivo():
            return

        agora = pygame.time.get_ticks()

        # Verifica se o jogador e seus atributos necessários existem
        jogador_valido = (hasattr(player, 'rect') and
                          hasattr(player, 'vida') and
                          hasattr(player.vida, 'esta_vivo') and
                          hasattr(player, 'receber_dano'))

        # Lógica de Ataque
        if self.is_attacking:
            self.atualizar_animacao() # Continua a animação de ataque
            self._atualizar_hitbox_ataque()

            # Verifica colisão do ataque com o jogador
            if jogador_valido and not self.hit_player_this_swing and \
               self.attack_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_swing = True
                # print(f"DEBUG(Espantalho): Ataque MELEE acertou jogador! Dano: {self.attack_damage_especifico}")

            # Termina o estado de ataque após a duração
            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_andar # Volta para sprites de andar/idle
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0 # Reinicia animação de andar
                self.attack_hitbox.size = (0,0) # Desativa a hitbox
        else:
            # Se não está atacando, tenta iniciar um ataque ou se move
            if jogador_valido:
                self.atacar(player) # Tenta iniciar um ataque

            if not self.is_attacking and jogador_valido: # Se não iniciou um ataque, move-se
                self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)

            self.atualizar_animacao() # Animação de andar/idle

        # Dano de Contato (herdado da InimigoBase, mas precisa ser chamado se não estiver no update da base)
        if jogador_valido and self.rect.colliderect(player.rect) and \
           (agora - self.last_contact_time >= self.contact_cooldown):
            player.receber_dano(self.contact_damage)
            self.last_contact_time = agora

        # Colisão com outros inimigos (se a lógica for implementada)
        # if outros_inimigos:
        #     for outro_inimigo in outros_inimigos:
        #         if outro_inimigo != self and self.rect.colliderect(outro_inimigo.rect):
        #             # Lógica para resolver colisão entre inimigos (ex: empurrar)
        #             pass


    # O método desenhar é herdado da InimigoBase.
    # Pode-se adicionar o desenho da hitbox de ataque para debug, se desejado.
    # def desenhar(self, surface, camera_x, camera_y):
    #     super().desenhar(surface, camera_x, camera_y)
    #     if self.is_attacking and self.attack_hitbox.width > 0: # Debug hitbox
    #         debug_rect_onscreen = self.attack_hitbox.move(-camera_x, -camera_y)
    #         pygame.draw.rect(surface, (255, 0, 0, 100), debug_rect_onscreen, 1)
