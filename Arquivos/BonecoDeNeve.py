# BonecoDeNeve.py
import pygame
import random
import math # Importa math para a função hypot
import time # Importa time para usar time.time() ou pygame.time.get_ticks()
import os # Importa os para verificar a existência de arquivos

# Importa a classe base Inimigo do ficheiro Inimigos.py
try:
    from Inimigos import Inimigo
    # Tenta importar o projétil real aqui também
    from Projetil_BolaNeve import ProjetilNeve as ProjetilNeveReal # Tenta importar a classe real
    print("DEBUG(BonecoDeNeve): Classe Inimigo e ProjetilNeveReal importadas.")
except ImportError:
    print("DEBUG(BonecoDeNeve): Aviso: Falha ao importar Inimigo ou ProjetilNeveReal. Usando placeholders.")
    ProjetilNeveReal = None # Define como None se não puder ser importado

    class Inimigo(pygame.sprite.Sprite): # Placeholder para Inimigo
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path):
            super().__init__()
            self.x = x; self.y = y; self.largura = largura; self.altura = altura
            self.hp = vida_maxima; self.max_hp = vida_maxima; self.velocidade = velocidade
            self.contact_damage = dano_contato; self.xp_value = xp_value
            self.sprite_path_base = sprite_path 
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 255), (0, 0, largura, altura)) 
            self.rect = self.image.get_rect(topleft=(x, y))
            self.last_hit_time = 0; self.hit_flash_duration = 150
            self.hit_flash_color = (255, 255, 255, 128); self.facing_right = True
            self.sprites = [self.image]; self.sprite_index = 0
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks()
            self.intervalo_animacao = 200; self.is_attacking = False
            self.attack_hitbox = pygame.Rect(0,0,0,0); self.hit_by_player_this_attack = False
            self.contact_cooldown = 1000; self.last_contact_time = pygame.time.get_ticks()
        def _carregar_sprite(self, path, tamanho): 
            base_dir = os.path.dirname(os.path.abspath(__file__))
            game_dir = os.path.dirname(base_dir)
            full_path = os.path.join(game_dir, path.replace("/", os.sep))
            if not os.path.exists(full_path):
                img = pygame.Surface(tamanho, pygame.SRCALPHA); pygame.draw.rect(img, (255,0,255), (0,0,tamanho[0],tamanho[1])); return img
            try:
                img = pygame.image.load(full_path).convert_alpha(); img = pygame.transform.scale(img, tamanho); return img
            except pygame.error:
                img = pygame.Surface(tamanho, pygame.SRCALPHA); pygame.draw.rect(img, (255,0,255), (0,0,tamanho[0],tamanho[1])); return img
        def receber_dano(self, dano, fonte_dano_rect=None): self.hp -= dano; self.last_hit_time = pygame.time.get_ticks(); self.hp = max(0, self.hp)
        def esta_vivo(self): return self.hp > 0
        def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): 
            if self.esta_vivo() and self.velocidade > 0:
                dx = alvo_x - self.rect.centerx; dy = alvo_y - self.rect.centery
                dist = math.hypot(dx, dy)
                if dist > 0:
                    fator_tempo = (dt_ms / 1000.0) if dt_ms else 1 
                    mov_x = (dx / dist) * self.velocidade * fator_tempo * 60 
                    mov_y = (dy / dist) * self.velocidade * fator_tempo * 60
                    self.rect.x += mov_x; self.rect.y += mov_y
                    self.facing_right = dx > 0
        def atualizar_animacao(self): 
            agora = pygame.time.get_ticks()
            if self.sprites and self.esta_vivo() and agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                self.tempo_ultimo_update_animacao = agora
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            if self.sprites: 
                idx = int(self.sprite_index % len(self.sprites)) if len(self.sprites) > 0 else 0
                if idx < len(self.sprites): base_image = self.sprites[idx]
                elif len(self.sprites) > 0: base_image = self.sprites[0]
                else: return 
                self.image = pygame.transform.flip(base_image, not self.facing_right, False)
        def update(self, player, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None): 
            if self.esta_vivo():
                if hasattr(player, 'rect'): self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
                self.atualizar_animacao() 
                current_ticks = pygame.time.get_ticks()
                if hasattr(player, 'rect') and hasattr(player, 'vida') and hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                   self.rect.colliderect(player.rect) and \
                   (current_ticks - self.last_contact_time >= self.contact_cooldown):
                    if hasattr(player, 'receber_dano'): player.receber_dano(self.contact_damage); self.last_contact_time = current_ticks
        def desenhar(self, janela, camera_x, camera_y): 
            screen_x = self.rect.x - camera_x; screen_y = self.rect.y - camera_y
            janela.blit(self.image, (screen_x, screen_y))
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time < self.hit_flash_duration:
                flash_surface = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
                flash_surface.fill(self.hit_flash_color); janela.blit(flash_surface, (screen_x, screen_y))
            if self.hp < self.max_hp and self.hp > 0: # Mostra barra de vida apenas se não estiver com HP máximo e estiver vivo
                bar_w = self.largura; bar_h = 5; health_p = self.hp / self.max_hp; curr_bar_w = int(bar_w * health_p)
                bar_x = screen_x; bar_y = screen_y - bar_h - 5 
                pygame.draw.rect(janela, (255,0,0), (bar_x, bar_y, bar_w, bar_h),0,2)
                pygame.draw.rect(janela, (0,255,0), (bar_x, bar_y, curr_bar_w, bar_h),0,2)
                pygame.draw.rect(janela, (255,255,255), (bar_x, bar_y, bar_w, bar_h), 1,2)

    # Placeholder para ProjetilNeve se ProjetilNeveReal não for importado
    if ProjetilNeveReal is None:
        print("DEBUG(BonecoDeNeve): Usando placeholder para ProjetilNeve.")
        class ProjetilNeve(pygame.sprite.Sprite): 
            def __init__(self, x_origem, y_origem, x_alvo, y_alvo, dano, velocidade=5, tamanho=10, cor=(200, 200, 255)):
                super().__init__()
                self.image = pygame.Surface((tamanho*2,tamanho*2), pygame.SRCALPHA)
                pygame.draw.circle(self.image, cor, (tamanho, tamanho), tamanho)
                self.rect = self.image.get_rect(center=(x_origem,y_origem))
                self.dano = dano 
                self.velocidade_magnitude = velocidade
                dx = x_alvo - x_origem; dy = y_alvo - y_origem
                dist = math.hypot(dx,dy)
                if dist > 0: self.direcao_x_norm = dx / dist; self.direcao_y_norm = dy / dist
                else: self.direcao_x_norm = 0; self.direcao_y_norm = -1 
                self.pos_x_float = float(self.rect.centerx); self.pos_y_float = float(self.rect.centery)
                self.alive = True; self.tempo_criacao = time.time(); self.vida_util = 5; self.atingiu = False
            def update(self, player, tela_largura, tela_altura, dt_ms=None): 
                if not self.alive: return
                fator_tempo_segundos = (dt_ms / 1000.0) if dt_ms is not None and dt_ms > 0 else (1.0 / 60.0)
                movimento_x = self.direcao_x_norm * self.velocidade_magnitude * fator_tempo_segundos * 60 
                movimento_y = self.direcao_y_norm * self.velocidade_magnitude * fator_tempo_segundos * 60
                self.pos_x_float += movimento_x; self.pos_y_float += movimento_y
                self.rect.centerx = round(self.pos_x_float); self.rect.centery = round(self.pos_y_float)
                if not self.atingiu and hasattr(player, 'rect') and hasattr(player, 'vida') and \
                   hasattr(player.vida, 'esta_vivo') and player.vida.esta_vivo() and \
                   self.rect.colliderect(player.rect):
                    if hasattr(player, 'receber_dano'): player.receber_dano(self.dano); self.atingiu = True 
                if self.rect.right < 0 or self.rect.left > tela_largura or \
                   self.rect.bottom < 0 or self.rect.top > tela_altura or \
                   self.atingiu or (time.time() - self.tempo_criacao > self.vida_util):
                    self.kill(); self.alive = False
            def desenhar(self, surface, camera_x, camera_y):
                if self.alive: surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
    else: 
        ProjetilNeve = ProjetilNeveReal


class BonecoDeNeve(Inimigo):
    sprites_carregados = None
    tamanho_sprite_definido = (80, 80) 

    def __init__(self, x, y, velocidade=1.0): 
        boneco_hp = 80; boneco_contact_damage = 7; boneco_xp_value = 30
        sprite_path_principal = "Sprites/Inimigos/Boneco de Neve/Boneco De Neve 1.png" 

        if BonecoDeNeve.sprites_carregados is None:
            caminhos = [sprite_path_principal, "Sprites/Inimigos/Boneco de Neve/Boneco de Neve 2.png", "Sprites/Inimigos/Boneco de Neve/Boneco de Neve 3.png"]
            BonecoDeNeve.sprites_carregados = []
            current_file_dir = os.path.dirname(os.path.abspath(__file__)); game_root_dir = os.path.dirname(current_file_dir) 
            for path in caminhos:
                full_path = os.path.join(game_root_dir, path.replace("/", os.sep))
                try:
                    if os.path.exists(full_path): sprite = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), BonecoDeNeve.tamanho_sprite_definido)
                    else: sprite = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA); pygame.draw.rect(sprite, (0,100,200), sprite.get_rect())
                    BonecoDeNeve.sprites_carregados.append(sprite)
                except pygame.error: sprite = pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA); pygame.draw.rect(sprite, (0,100,200), sprite.get_rect()); BonecoDeNeve.sprites_carregados.append(sprite)
            if not BonecoDeNeve.sprites_carregados: BonecoDeNeve.sprites_carregados.append(pygame.Surface(BonecoDeNeve.tamanho_sprite_definido, pygame.SRCALPHA))

        super().__init__(x, y, BonecoDeNeve.tamanho_sprite_definido[0], BonecoDeNeve.tamanho_sprite_definido[1], boneco_hp, velocidade, boneco_contact_damage, boneco_xp_value, sprite_path_principal)
        self.sprites = BonecoDeNeve.sprites_carregados; self.sprite_index = 0 
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks(); self.intervalo_animacao = 200 
        self.is_attacking = False; self.attack_duration = 0.5; self.attack_timer = 0.0 
        self.attack_damage = 12; self.attack_range = 300; self.attack_cooldown = 2.0 
        self.last_attack_time = time.time() - self.attack_cooldown 
        self.velocidade_projetil = 6; self.shoot_projectile_flag = False 
        if self.sprites: idx = int(self.sprite_index % len(self.sprites)) if len(self.sprites) > 0 else 0; self.image = self.sprites[idx] if idx < len(self.sprites) and len(self.sprites)>0 else self.sprites[0] if len(self.sprites)>0 else self.image

    def receber_dano(self, dano, fonte_dano_rect=None): super().receber_dano(dano, fonte_dano_rect) 
    def atualizar_animacao(self): super().atualizar_animacao()
    def mover_em_direcao(self, alvo_x, alvo_y, dt_ms=None): super().mover_em_direcao(alvo_x, alvo_y, dt_ms)

    def atacar(self, player):
        if not hasattr(player, 'rect'): return
        current_time = time.time()
        if self.esta_vivo() and not self.is_attacking and (current_time - self.last_attack_time >= self.attack_cooldown):
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)
            if distancia_ao_jogador <= self.attack_range: 
                self.is_attacking = True; self.attack_timer = current_time 
                self.last_attack_time = current_time; self.shoot_projectile_flag = True 
                
    def update(self, player, projeteis_inimigos_ref, tela_largura=None, altura_tela=None, dt_ms=None): 
        if not hasattr(player, 'rect') or not hasattr(player, 'vida') or \
           not hasattr(player.vida, 'esta_vivo') or not hasattr(player, 'receber_dano'):
            return 

        try:
            super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)
        except TypeError:
            try:
                super().update(player, projeteis_inimigos_ref, tela_largura, altura_tela)
            except TypeError:
                try:
                    super().update(player, projeteis_inimigos_ref)
                except TypeError:
                    try:
                        super().update(player) 
                    except Exception as e_final:
                        print(f"DEBUG(BonecoDeNeve): ERRO CRÍTICO ao chamar super().update(). Nenhuma assinatura compatível. Erro: {e_final}")
                        pass 


        if self.esta_vivo():
            current_time_ataque = time.time()
            if self.is_attacking: 
                if current_time_ataque - self.attack_timer >= self.attack_duration:
                    if self.shoot_projectile_flag: 
                        if projeteis_inimigos_ref is not None and ProjetilNeve is not None: 
                            start_x = self.rect.centerx; start_y = self.rect.centery
                            target_x = player.rect.centerx; target_y = player.rect.centery
                            novo_projetil = ProjetilNeve(start_x, start_y, target_x, target_y, self.attack_damage, self.velocidade_projetil)
                            
                            # --- CORREÇÃO DIRETA DO BUG ---
                            # Assumindo que projeteis_inimigos_ref é um pygame.sprite.Group
                            # (conforme definido em GerenciadorDeInimigos.py)
                            if hasattr(projeteis_inimigos_ref, 'add'):
                                projeteis_inimigos_ref.add(novo_projetil)
                            else:
                                # Fallback muito improvável se a estrutura mudar drasticamente
                                print(f"DEBUG(BonecoDeNeve): ERRO - projeteis_inimigos_ref (tipo: {type(projeteis_inimigos_ref)}) não tem método 'add'. Não foi possível adicionar projétil.")
                            # --- FIM DA CORREÇÃO DIRETA ---
                        
                        self.shoot_projectile_flag = False 
                    self.is_attacking = False 
            
            if not self.is_attacking: 
                self.atacar(player)

    def desenhar(self, surface, camera_x, camera_y):
        super().desenhar(surface, camera_x, camera_y)
