import pygame
import os
import math
import time

# Importação da Classe Base Inimigo e do Projétil
try:
    # Usando importações absolutas para maior robustez
    from Inimigos.Inimigos import Inimigo as InimigoBase
    from Inimigos.ProjetilMaga import ProjetilMaga 
except ImportError as e:
    print(f"ERRO DE IMPORTAÇÃO: {e}. Verifique se 'Inimigos.py' e 'ProjetilMaga.py' estão acessíveis.")
    # Placeholders para evitar que o jogo trave
    class InimigoBase(pygame.sprite.Sprite):
        def __init__(self, x, y, l, a, vida, vel, dano, xp, path=""):
            super().__init__(); self.rect = pygame.Rect(x, y, l, a); self.hp = vida; self.contact_damage = dano; self.x, self.y = float(x), float(y); self.velocidade = vel; self.contact_cooldown = 1000; self.last_contact_time = 0
        def receber_dano(self, dano, fonte=None): self.hp -= dano
        def esta_vivo(self): return self.hp > 0
        def atualizar_animacao(self): pass
        def kill(self): super().kill()
    class ProjetilMaga:
        def __init__(self, x, y, dx, dy, dano, vel): pass


class Maga(InimigoBase):
    """
    Inimigo que ataca à distância, tentando manter o jogador
    dentro de um alcance ideal. Foge se o jogador se aproxima demais e 
    persegue se ele se afasta muito.
    """
    sprites_andar_carregados = None
    sprites_atacar_carregados = None
    tamanho_sprite_definido = (70, 90)
    som_ataque_maga, som_dano_maga, som_morte_maga, som_conjura_maga = None, None, None, None
    sons_carregados = False

    @staticmethod
    def _obter_pasta_raiz_jogo():
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos, lista_destino, tamanho):
        pasta_raiz = Maga._obter_pasta_raiz_jogo()
        if lista_destino is None: lista_destino = []
        for path_relativo in caminhos:
            caminho_completo = os.path.join(pasta_raiz, path_relativo.replace("/", os.sep))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha()
                    sprite = pygame.transform.scale(sprite, tamanho)
                    lista_destino.append(sprite)
                else:
                    print(f"AVISO: Sprite '{caminho_completo}' não encontrado. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((150, 0, 150, 180)); lista_destino.append(placeholder)
            except pygame.error as e:
                print(f"ERRO ao carregar sprite '{caminho_completo}': {e}.")
                placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((150, 0, 150, 180)); lista_destino.append(placeholder)
        if not lista_destino:
            placeholder = pygame.Surface(tamanho, pygame.SRCALPHA); placeholder.fill((100, 0, 100, 200)); lista_destino.append(placeholder)
        return lista_destino

    @staticmethod
    def carregar_recursos_maga():
        if Maga.sprites_andar_carregados is None:
            caminhos_andar = [f"Sprites/Inimigos/Maga/C ({i}).png" for i in range(1, 8)]
            Maga.sprites_andar_carregados = Maga._carregar_lista_sprites_estatico(caminhos_andar, [], Maga.tamanho_sprite_definido)
            
        if Maga.sprites_atacar_carregados is None:
            caminhos_atacar = [f"Sprites/Inimigos/Maga/A ({i}).png" for i in range(1, 4)]
            Maga.sprites_atacar_carregados = Maga._carregar_lista_sprites_estatico(caminhos_atacar, [], Maga.tamanho_sprite_definido)

        if not Maga.sons_carregados:
            Maga.sons_carregados = True

    def __init__(self, x, y, velocidade=70):
        Maga.carregar_recursos_maga()

        vida_maga = 80
        dano_contato_maga = 10
        xp_maga = 90
        sprite_path_principal = "Sprites/Inimigos/Maga/C (1).png"

        super().__init__(
            x, y,
            Maga.tamanho_sprite_definido[0], Maga.tamanho_sprite_definido[1],
            vida_maga, velocidade, dano_contato_maga,
            xp_maga, sprite_path_principal
        )

        self.moedas_drop = 12
        self.sprites_andar = Maga.sprites_andar_carregados
        self.sprites_atacar = Maga.sprites_atacar_carregados
        self.sprites = self.sprites_andar
        self.sprite_index = 0

        self.intervalo_animacao_andar = 250
        self.intervalo_animacao_atacar = 120
        self.intervalo_animacao = self.intervalo_animacao_andar
        
        self.is_attacking = False
        self.attack_duration_ms = len(self.sprites_atacar) * self.intervalo_animacao_atacar if self.sprites_atacar else 0
        self.attack_timer = 0
        self.projectile_damage = 30
        self.projectile_speed = 220 # Ajuste de velocidade para projétil teleguiado
        self.attack_range = 350
        self.attack_cooldown = 2000
        self.last_attack_time = -self.attack_cooldown

        self.distancia_minima_do_jogador = 150
        self.distancia_maxima_do_jogador = 320

    def atacar(self, player, projeteis_inimigos_ref, agora):
        if not self.is_attacking and (agora - self.last_attack_time >= self.attack_cooldown):
            self.is_attacking = True
            self.attack_timer = agora
            self.last_attack_time = agora
            self.sprites = self.sprites_atacar
            self.intervalo_animacao = self.intervalo_animacao_atacar
            self.sprite_index = 0

            # --- CORREÇÃO APLICADA ---
            # Cria o projétil teleguiado passando o jogador como o alvo.
            novo_projetil = ProjetilMaga(
                x_origem=self.rect.centerx,
                y_origem=self.rect.centery,
                alvo_obj=player,
                dano=self.projectile_damage,
                velocidade=self.projectile_speed
            )
            projeteis_inimigos_ref.add(novo_projetil)
            
            if Maga.som_conjura_maga:
                Maga.som_conjura_maga.play()

    def update(self, player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms):
        if not self.esta_vivo():
            return

        agora = pygame.time.get_ticks()
        
        # Lógica de Comportamento e IA
        distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)

        if self.is_attacking:
            # Termina a animação de ataque
            if agora - self.attack_timer >= self.attack_duration_ms:
                self.is_attacking = False
                self.sprites = self.sprites_andar
                self.intervalo_animacao = self.intervalo_animacao_andar
                self.sprite_index = 0
        else:
            # IA de Kiting: Mover-se para a posição ideal
            fator_tempo = dt_ms / 1000.0
            
            direcao_x, direcao_y = 0, 0
            if distancia_ao_jogador > self.distancia_maxima_do_jogador:
                direcao_x = player.rect.centerx - self.rect.centerx
                direcao_y = player.rect.centery - self.rect.centery
            elif distancia_ao_jogador < self.distancia_minima_do_jogador:
                direcao_x = self.rect.centerx - player.rect.centerx
                direcao_y = self.rect.centery - player.rect.centery
            else:
                self.atacar(player, projeteis_inimigos_ref, agora)

            # Mover com base na direção decidida
            if direcao_x != 0 or direcao_y != 0:
                norma = math.hypot(direcao_x, direcao_y)
                mov_x = (direcao_x / norma) * self.velocidade * fator_tempo
                mov_y = (direcao_y / norma) * self.velocidade * fator_tempo
                self.x += mov_x
                self.y += mov_y
                self.rect.topleft = (self.x, self.y)
                if mov_x > 0.1: self.facing_right = True
                elif mov_x < -0.1: self.facing_right = False

        # Atualizar Animação (usa método da classe base Inimigo)
        self.atualizar_animacao()
        
    def receber_dano(self, dano, fonte_dano_rect=None):
        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect)
        if not self.esta_vivo() and vida_antes > 0 and Maga.som_morte_maga:
            Maga.som_morte_maga.play()
        elif self.esta_vivo() and vida_antes > self.hp and Maga.som_dano_maga:
            Maga.som_dano_maga.play()
