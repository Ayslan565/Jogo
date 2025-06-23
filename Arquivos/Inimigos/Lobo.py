import pygame
import os
import math
import time

# --- Importação da Classe Base Inimigo ---
try:
    from .Inimigos import Inimigo as InimigoBase
except ImportError:
    # Placeholder para InimigoBase caso a importação falhe, garantindo que a classe Lobo possa ser definida.
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            self.hp = self.max_hp = vida_maxima
            self.velocidade = velocidade
            self.contact_damage = dano_contato
            self.xp_value = xp_value
            self.moedas_drop = 0
            self.x, self.y = float(x), float(y)
            self.last_contact_time = 0
            self.facing_right = True
            self.rect_colisao = self.rect.inflate(-10, -10) # Exemplo de rect de colisão
        
        def esta_vivo(self): return self.hp > 0
        def receber_dano(self, dano, fonte_dano_rect=None): self.hp = max(0, self.hp - dano)
        def update(self, *args, **kwargs): pass
        def desenhar(self, janela, cam_x, cam_y): janela.blit(self.image, (self.rect.x - cam_x, self.rect.y - cam_y))
        def kill(self): super().kill()


class Lobo(InimigoBase):
    # Recursos da classe (sprites e sons) para serem carregados uma única vez
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (150, 100)
    som_ataque_lobo, som_dano_lobo, som_morte_lobo, som_uivo_lobo = None, None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        """Encontra o diretório raiz do projeto para carregar os assets corretamente."""
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho):
        """Carrega uma lista de sprites a partir de caminhos relativos à raiz do projeto."""
        pasta_raiz = Lobo._obter_pasta_raiz_jogo()
        if lista_destino is None: lista_destino = []
        for path_relativo in caminhos:
            caminho_completo = os.path.join(pasta_raiz, path_relativo.replace("/", os.sep))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                else:
                    # Adiciona um placeholder se o arquivo não for encontrado
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((100, 100, 100, 180)); lista_destino.append(placeholder)
            except pygame.error:
                # Adiciona um placeholder em caso de erro de carregamento
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((100, 100, 100, 180)); lista_destino.append(placeholder)
        if not lista_destino:
            # Garante que a lista não fique vazia
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((80, 80, 80, 200)); lista_destino.append(placeholder)
        return lista_destino

    @staticmethod
    def carregar_recursos_lobo():
        """Carrega todos os sprites e sons do Lobo, se ainda não foram carregados."""
        if Lobo.sprites_andar_carregados is None:
            # CORRIGIDO: Alterado de .jpg para .png
            caminhos_andar = [
                "Sprites/Inimigos/Lobo/A (1).png",
                "Sprites/Inimigos/Lobo/A (2).png",
                "Sprites/Inimigos/Lobo/A (3).png",
                "Sprites/Inimigos/Lobo/A (4).png",
                "Sprites/Inimigos/Lobo/A (5).png",
                "Sprites/Inimigos/Lobo/A (6).png",
                "Sprites/Inimigos/Lobo/A (7).png",
                "Sprites/Inimigos/Lobo/A (8).png",
                "Sprites/Inimigos/Lobo/A (9).png",
                "Sprites/Inimigos/Lobo/A (10).png",
            ]
            Lobo.sprites_andar_carregados = []
            Lobo._carregar_lista_sprites_estatico(caminhos_andar, Lobo.sprites_andar_carregados, Lobo.tamanho_sprite_definido)
            
        if Lobo.sprites_atacar_carregados is None:
            # CORRIGIDO: Alterado de .jpg para .png
            caminhos_atacar = [
                "Sprites/Inimigos/Lobo/A (1).png",
                "Sprites/Inimigos/Lobo/A (2).png",
                "Sprites/Inimigos/Lobo/A (3).png",
                "Sprites/Inimigos/Lobo/A (4).png",
                "Sprites/Inimigos/Lobo/A (5).png",
                "Sprites/Inimigos/Lobo/A (6).png",
                "Sprites/Inimigos/Lobo/A (7).png",
                "Sprites/Inimigos/Lobo/A (8).png",
                "Sprites/Inimigos/Lobo/A (9).png",
                "Sprites/Inimigos/Lobo/A (10).png",
            ]
            Lobo.sprites_atacar_carregados = []
            Lobo._carregar_lista_sprites_estatico(caminhos_atacar, Lobo.sprites_atacar_carregados, Lobo.tamanho_sprite_definido)
            
            # Fallback caso os sprites de ataque não sejam encontrados
            if not Lobo.sprites_atacar_carregados and Lobo.sprites_andar_carregados:
                Lobo.sprites_atacar_carregados = [Lobo.sprites_andar_carregados[0]]
        
        if not Lobo.sons_carregados:
            # Futuramente, carregar os sons aqui
            Lobo.sons_carregados = True

    def __init__(self, x, y, velocidade=1.8):
        Lobo.carregar_recursos_lobo()

        super().__init__(
            x, y,
            Lobo.tamanho_sprite_definido[0], Lobo.tamanho_sprite_definido[1],
            vida_maxima=95,
            velocidade=velocidade,
            dano_contato=8,
            xp_value=45,
            sprite_path="Sprites/Inimigos/Lobo/Lobo4.png" # Este também deve ser .png
        )
        self.moedas_drop = 15

        self.sprites_andar = Lobo.sprites_andar_carregados
        self.sprites_atacar = Lobo.sprites_atacar_carregados
        self.sprites = self.sprites_andar

        self.image = self.sprites[0] if self.sprites else pygame.Surface(Lobo.tamanho_sprite_definido, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.sprite_index = 0
        self.intervalo_animacao_andar = 100
        self.intervalo_animacao_atacar = 80
        self.intervalo_animacao = self.intervalo_animacao_andar
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Adicionado para animação

        self.is_attacking = False
        self.attack_duration = 0.5
        self.attack_timer = 0.0
        self.attack_damage_especifico = 15
        self.attack_range = 70
        self.attack_cooldown = 1.8
        self.last_attack_time = pygame.time.get_ticks() - int(self.attack_cooldown * 1000)
        self.attack_hitbox = pygame.Rect(0, 0, 0, 0)
        self.hit_player_this_bite = False

    def _atualizar_hitbox_ataque(self):
        """Calcula a posição e o tamanho da hitbox de ataque."""
        if not self.is_attacking:
            self.attack_hitbox.size = (0, 0)
            return
        
        largura_hitbox = self.rect.width * 0.8
        altura_hitbox = self.rect.height * 0.6
        self.attack_hitbox.size = (largura_hitbox, altura_hitbox)

        offset_x = 20
        if self.facing_right:
            self.attack_hitbox.midleft = (self.rect.right - offset_x / 2, self.rect.centery)
        else:
            self.attack_hitbox.midright = (self.rect.left + offset_x / 2, self.rect.centery)

    def atacar(self, player):
        """Inicia a animação e a lógica de ataque quando o jogador está no alcance."""
        if not (hasattr(player, 'rect') and self.esta_vivo()): return
        
        agora = pygame.time.get_ticks()
        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
        
        if not self.is_attacking and distancia_ao_jogador <= self.attack_range and (agora - self.last_attack_time >= self.attack_cooldown * 1000):
            self.is_attacking = True
            self.attack_timer = agora
            self.last_attack_time = agora
            self.hit_player_this_bite = False
            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0

    def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        """Atualiza o estado do lobo a cada frame."""
        if not self.esta_vivo():
            self.kill() # O GerenciadorDeInimigos cuidará das recompensas.
            return

        agora = pygame.time.get_ticks()
        jogador_valido = player and hasattr(player, 'rect') and hasattr(player, 'esta_vivo') and player.esta_vivo()

        # Chama o update da classe base (controla movimento, animação base, etc.)
        super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)

        if self.is_attacking:
            self._atualizar_hitbox_ataque()
            if jogador_valido and not self.hit_player_this_bite and hasattr(player, 'rect_colisao') and self.attack_hitbox.colliderect(player.rect_colisao):
                player.receber_dano(self.attack_damage_especifico)
                self.hit_player_this_bite = True
            
            if agora - self.attack_timer >= self.attack_duration * 1000:
                self.is_attacking = False
                self.sprites = self.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0
                self.attack_hitbox.size = (0, 0)
        else:
            if jogador_valido:
                self.atacar(player)

        # Dano de contato com cooldown
        if jogador_valido and hasattr(player, 'rect_colisao') and self.rect.colliderect(player.rect_colisao) and (agora - self.last_contact_time >= self.contact_cooldown):
            player.receber_dano(self.contact_damage)
            self.last_contact_time = agora

    def receber_dano(self, dano, fonte_dano_rect=None):
        """Processa o dano recebido e toca os sons correspondentes."""
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if not self.esta_vivo() and vida_antes > 0 and Lobo.som_morte_lobo:
            Lobo.som_morte_lobo.play()
        elif self.esta_vivo() and vida_antes > self.hp and Lobo.som_dano_lobo:
            Lobo.som_dano_lobo.play()