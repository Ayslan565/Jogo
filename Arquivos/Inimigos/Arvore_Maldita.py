# Arvore_Maldita.py
import pygame
import os
import math
import random

# --- Importação da Classe Base Inimigo ---
try:
    # Tenta importar a classe Inimigo de um módulo local chamado Inimigos
    # O "." antes de Inimigos indica uma importação relativa,
    # significando que o módulo Inimigos.py (ou pasta Inimigos/__init__.py)
    # deve estar no mesmo diretório que Arvore_Maldita.py.
    from .Inimigos import Inimigo as InimigoBase
    print(f"DEBUG(Arvore_Maldita): Classe InimigoBase importada com sucesso.")
except ImportError as e:
    # Se a importação falhar, usa uma classe InimigoBase placeholder.
    # Isso é útil para testar Arvore_Maldita.py isoladamente ou se a classe base ainda não existe.
    print(f"DEBUG(Arvore_Maldita): FALHA ao importar InimigoBase: {e}. Usando placeholder local MUITO BÁSICO.")
    class InimigoBase(pygame.sprite.Sprite): # Placeholder
        def __init__(self, x, y, largura, altura, vida_maxima, velocidade, dano_contato, xp_value, sprite_path=""):
            super().__init__()
            self.rect = pygame.Rect(x, y, largura, altura)
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA) # SRCALPHA para transparência
            self.image.fill((80, 40, 20, 150)) # Cor marrom translúcida para placeholder
            pygame.draw.rect(self.image, (100,60,30), self.image.get_rect(), 1) # Contorno
            self.hp = vida_maxima
            self.max_hp = vida_maxima
            self.velocidade = velocidade # Armazena a velocidade
            self.contact_damage = dano_contato
            self.xp_value = xp_value
            self.facing_right = True # Direção inicial
            self.last_hit_time = 0 # Para efeito de flash ao ser atingido
            self.hit_flash_duration = 150 # Duração do flash em ms
            self.hit_flash_color = (255, 255, 255, 128) # Cor do flash (branco translúcido)
            self.contact_cooldown = 1000 # Cooldown para dano de contato em ms
            self.last_contact_time = 0 # Última vez que causou dano por contato
            self.sprites = [self.image] # Lista de sprites para animação (inicia com a imagem placeholder)
            self.sprite_index = 0 # Índice do sprite atual na animação
            self.intervalo_animacao = 200 # Intervalo entre frames da animação em ms
            self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Para controlar o tempo da animação
            self.x = float(x) # Coordenada X (float para movimento suave)
            self.y = float(y) # Coordenada Y (float para movimento suave)
            print(f"DEBUG(InimigoBase Placeholder para Arvore_Maldita): Instanciado. Velocidade: {self.velocidade}")

        def _carregar_sprite(self, path, tamanho):
            # Método placeholder para carregar um sprite individual, se necessário.
            # No contexto do placeholder, apenas cria uma superfície colorida.
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            img.fill((70,30,10, 128)) # Cor um pouco diferente para distinguir
            return img

        def receber_dano(self, dano, fonte_dano_rect=None):
            # Reduz a vida do inimigo, garantindo que não fique abaixo de 0.
            self.hp = max(0, self.hp - dano)
            self.last_hit_time = pygame.time.get_ticks() # Registra o tempo do hit para o efeito de flash

        def esta_vivo(self):
            # Verifica se o inimigo ainda tem pontos de vida.
            return self.hp > 0

        def mover_em_direcao(self, ax, ay, dt_ms=None):
            # Move o inimigo em direção a um ponto (ax, ay).
            # dt_ms é o delta time em milissegundos, para movimento consistente independente de FPS.
            if not self.velocidade > 0: return # Não se move se a velocidade for zero ou negativa
            if dt_ms is None: dt_ms = 16 # Valor padrão de delta time (aproximadamente 60 FPS)

            # Calcula o vetor direção
            dx = ax - self.rect.centerx
            dy = ay - self.rect.centery
            dist = math.hypot(dx, dy) # Distância até o alvo

            if dist > 0: # Evita divisão por zero se já estiver no alvo
                # Normaliza o vetor direção (componentes x e y entre -1 e 1)
                norm_dx = dx / dist
                norm_dy = dy / dist

                # Calcula o deslocamento baseado na velocidade, delta time e um fator de ajuste.
                # O fator 50 é arbitrário e serve para ajustar a percepção da velocidade.
                # (dt_ms / 1000.0) converte milissegundos para segundos.
                mov_x = norm_dx * self.velocidade * (dt_ms / 1000.0) * 50
                mov_y = norm_dy * self.velocidade * (dt_ms / 1000.0) * 50

                # Atualiza a posição do retângulo de colisão
                self.rect.x += mov_x
                self.rect.y += mov_y

                # Atualiza as coordenadas x e y (usadas para câmera ou lógica de posição mais precisa)
                self.x = float(self.rect.centerx)
                self.y = float(self.rect.centery)

                # Atualiza a direção para onde o inimigo está "olhando"
                if dx > 0 : self.facing_right = True
                elif dx < 0: self.facing_right = False

        def atualizar_animacao(self):
            # Atualiza o frame da animação do inimigo.
            agora = pygame.time.get_ticks()
            if not self.sprites or len(self.sprites) == 0: return # Retorna se não houver sprites

            # Verifica se é hora de mudar para o próximo frame
            if agora - self.tempo_ultimo_update_animacao > self.intervalo_animacao:
                self.tempo_ultimo_update_animacao = agora
                self.sprite_index = (self.sprite_index + 1) % len(self.sprites) # Avança o frame, ciclando
                
                base_image = self.sprites[self.sprite_index] # Pega o sprite base da lista

                # Espelha a imagem se o inimigo não estiver virado para a direita
                if hasattr(self, 'facing_right') and not self.facing_right:
                    self.image = pygame.transform.flip(base_image, True, False) # Flip horizontal
                else:
                    self.image = base_image.copy() # Usa uma cópia para não modificar o original na lista
            
            # Garante que self.image exista mesmo que a animação não tenha sido atualizada no tick exato
            # Isso é uma redundância defensiva, a lógica acima deve cobrir.
            elif not hasattr(self, 'image') or self.image is None:
                base_image = self.sprites[self.sprite_index]
                if hasattr(self, 'facing_right') and not self.facing_right:
                    self.image = pygame.transform.flip(base_image, True, False)
                else:
                    self.image = base_image.copy()

            # Aplica o efeito de flash se o inimigo foi atingido recentemente
            if hasattr(self, 'last_hit_time') and agora - self.last_hit_time < self.hit_flash_duration:
                if hasattr(self, 'image') and self.image is not None: # Certifica que self.image existe
                    flash_overlay = self.image.copy() # Cria uma cópia da imagem atual para aplicar o flash
                    try:
                        # Tenta aplicar o flash usando BLEND_RGBA_MULT para um efeito mais suave
                        flash_overlay.fill(self.hit_flash_color, special_flags=pygame.BLEND_RGBA_MULT)
                        self.image.blit(flash_overlay, (0,0))
                    except pygame.error:
                        # Fallback para um flash mais simples se BLEND_RGBA_MULT falhar (ex: em superfícies sem alfa)
                        simple_flash = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
                        simple_flash.fill(self.hit_flash_color)
                        self.image.blit(simple_flash, (0,0))

        def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
            # Método de atualização principal do inimigo (chamado a cada frame do jogo).
            # No placeholder, apenas atualiza a animação.
            # A classe derivada Arvore_Maldita terá uma lógica mais complexa aqui.
            self.atualizar_animacao()

        def desenhar(self, janela, camera_x, camera_y):
            # Desenha o inimigo na tela, ajustado pela posição da câmera.
            if self.image and self.rect:
                janela.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
        
        def kill(self):
            # Remove o sprite de todos os grupos do Pygame.
            super().kill()


class Arvore_Maldita(InimigoBase):
    # Atributos de classe para armazenar recursos carregados (sprites, sons)
    # Isso evita recarregar os mesmos arquivos para cada instância da árvore.
    sprites_idle_arvore_carregados = None
    sprites_ataque_principal_arvore_carregados = None
    tamanho_sprite_definido = (250, 300) # Tamanho padrão para os sprites da árvore

    # Sons (inicializados como None, carregados depois)
    som_ataque_arvore = None
    som_dano_arvore = None
    som_morte_arvore = None
    sons_carregados = False # Flag para controlar se os sons já foram carregados

    @staticmethod
    def _obter_pasta_raiz_jogo():
        # Determina o caminho absoluto para a pasta raiz do jogo.
        # Assume que este script (Arvore_Maldita.py) está em uma subpasta,
        # dois níveis abaixo da pasta raiz do jogo.
        # Ex: [RAIZ_DO_JOGO]/Codigo/Inimigos/Arvore_Maldita.py
        diretorio_script_atual = os.path.dirname(os.path.abspath(__file__))
        # os.path.abspath(__file__) -> caminho completo do arquivo atual
        # os.path.dirname(...) -> diretório do arquivo atual
        # os.path.join(..., "..", "..") -> sobe dois níveis de diretório
        pasta_raiz_jogo = os.path.abspath(os.path.join(diretorio_script_atual, "..", ".."))
        return pasta_raiz_jogo

    @staticmethod
    def _carregar_som_arvore_maldita(caminho_relativo_a_raiz_jogo):
        # Carrega um arquivo de som.
        pasta_raiz_jogo = Arvore_Maldita._obter_pasta_raiz_jogo()
        # Constrói o caminho completo para o arquivo de som.
        # .replace("\\", os.sep) garante que o separador de caminho seja o correto para o SO.
        caminho_completo = os.path.join(pasta_raiz_jogo, caminho_relativo_a_raiz_jogo.replace("\\", os.sep))
        if not os.path.exists(caminho_completo):
            print(f"AVISO (Arvore_Maldita): Arquivo de som não encontrado: {caminho_completo}")
            return None
        try:
            som = pygame.mixer.Sound(caminho_completo)
            print(f"DEBUG (Arvore_Maldita): Som carregado: {caminho_completo}")
            return som
        except pygame.error as e:
            print(f"ERRO (Arvore_Maldita): Falha ao carregar som {caminho_completo}: {e}")
            return None

    @staticmethod
    def _carregar_lista_sprites_estatico(caminhos_relativos_a_raiz_jogo, lista_destino_existente, tamanho_sprite, nome_animacao):
        # Carrega uma sequência de sprites de arquivos de imagem.
        pasta_raiz_jogo = Arvore_Maldita._obter_pasta_raiz_jogo()
        if lista_destino_existente is None: lista_destino_existente = [] # Garante que a lista exista

        for path_relativo in caminhos_relativos_a_raiz_jogo:
            caminho_completo = os.path.join(pasta_raiz_jogo, path_relativo.replace("\\", os.sep))
            try:
                if os.path.exists(caminho_completo):
                    sprite = pygame.image.load(caminho_completo).convert_alpha() # Carrega com transparência
                    sprite = pygame.transform.scale(sprite, tamanho_sprite) # Redimensiona
                    lista_destino_existente.append(sprite)
                    # print(f"DEBUG (Arvore_Maldita): Sprite '{nome_animacao}' carregado: {caminho_completo}")
                else:
                    print(f"AVISO (Arvore_Maldita): Sprite '{nome_animacao}' não encontrado: {caminho_completo}. Usando placeholder.")
                    placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                    placeholder.fill((60, 30, 10, 180)) # Cor placeholder específica
                    lista_destino_existente.append(placeholder)
            except pygame.error as e:
                print(f"ERRO (Arvore_Maldita): Falha ao carregar sprite '{nome_animacao}' de {caminho_completo}: {e}. Usando placeholder.")
                placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
                placeholder.fill((60, 30, 10, 180))
                lista_destino_existente.append(placeholder)
        
        if not lista_destino_existente: # Se nenhum sprite foi carregado (nem placeholder de erro individual)
            print(f"AVISO (Arvore_Maldita): Nenhum sprite carregado para '{nome_animacao}'. Adicionando placeholder genérico para a animação.")
            placeholder = pygame.Surface(tamanho_sprite, pygame.SRCALPHA)
            placeholder.fill((40, 20, 5, 200)) # Cor placeholder ainda mais genérica
            lista_destino_existente.append(placeholder)


    @staticmethod
    def carregar_recursos_arvore_maldita():
        # Método estático para carregar todos os recursos da Arvore_Maldita uma única vez.
        # Sprites de Idle (Parado)
        if Arvore_Maldita.sprites_idle_arvore_carregados is None:
            Arvore_Maldita.sprites_idle_arvore_carregados = []
            # Estes são os caminhos RELATIVOS à pasta raiz do jogo
            caminhos_idle = [
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita1.png",
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita2.png",
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita3.png",
            ]
            Arvore_Maldita._carregar_lista_sprites_estatico(caminhos_idle, Arvore_Maldita.sprites_idle_arvore_carregados, Arvore_Maldita.tamanho_sprite_definido, "ArvoreMaldita_Idle")

        # Sprites de Ataque Principal
        if Arvore_Maldita.sprites_ataque_principal_arvore_carregados is None:
            Arvore_Maldita.sprites_ataque_principal_arvore_carregados = []
            caminhos_ataque_principal = [
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita1.png", # Pode ser diferente, aqui está igual ao idle como exemplo
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita2.png",
                "Sprites\\Inimigos\\Arvore Maldita\\Arvore Maldita3.png",
            ]
            
            # Fallback: Se os sprites de ataque não existirem, usa os de idle.
            primeiro_sprite_path_completo = ""
            if caminhos_ataque_principal: # Verifica se a lista não está vazia
                primeiro_sprite_path_completo = os.path.join(Arvore_Maldita._obter_pasta_raiz_jogo(), caminhos_ataque_principal[0].replace("\\", os.sep))

            if not caminhos_ataque_principal or not os.path.exists(primeiro_sprite_path_completo):
                print(f"AVISO (Arvore_Maldita): Sprites de ataque principal não encontrados ou lista vazia. Usando sprites de idle como fallback.")
                if Arvore_Maldita.sprites_idle_arvore_carregados and len(Arvore_Maldita.sprites_idle_arvore_carregados) > 0:
                    Arvore_Maldita.sprites_ataque_principal_arvore_carregados = list(Arvore_Maldita.sprites_idle_arvore_carregados) # Cria uma cópia da lista
                else:
                    # Fallback extremo: se nem os de idle existirem, cria um placeholder para ataque
                    print(f"AVISO (Arvore_Maldita): Sprites de idle também vazios. Criando placeholder para ataque principal.")
                    placeholder_ataque = pygame.Surface(Arvore_Maldita.tamanho_sprite_definido, pygame.SRCALPHA)
                    placeholder_ataque.fill((40,20,5, 180)) # Cor placeholder
                    Arvore_Maldita.sprites_ataque_principal_arvore_carregados = [placeholder_ataque]
            else:
                Arvore_Maldita._carregar_lista_sprites_estatico(caminhos_ataque_principal, Arvore_Maldita.sprites_ataque_principal_arvore_carregados, Arvore_Maldita.tamanho_sprite_definido, "ArvoreMaldita_AtaquePrincipal")

        # Carregar Sons (descomente e ajuste os caminhos conforme necessário)
        if not Arvore_Maldita.sons_carregados:
            # Exemplo de como carregar sons (os caminhos devem existir)
            # Arvore_Maldita.som_ataque_arvore = Arvore_Maldita._carregar_som_arvore_maldita("Sons/Chefes/Arvore_Maldita/ataque_principal.wav")
            # Arvore_Maldita.som_dano_arvore = Arvore_Maldita._carregar_som_arvore_maldita("Sons/Chefes/Arvore_Maldita/dano.wav")
            # Arvore_Maldita.som_morte_arvore = Arvore_Maldita._carregar_som_arvore_maldita("Sons/Chefes/Arvore_Maldita/morte.wav")
            # print("DEBUG (Arvore_Maldita): Tentativa de carregar sons concluída.")
            Arvore_Maldita.sons_carregados = True # Marca como tentado, mesmo que alguns falhem.

    def __init__(self, x, y, velocidade=0.3): # Velocidade padrão de 0.3
        # Primeiro, garante que os recursos da classe (sprites, sons) estejam carregados.
        Arvore_Maldita.carregar_recursos_arvore_maldita()

        # Parâmetros específicos da Arvore_Maldita
        vida_arvore = 1000
        dano_contato_arvore = 25
        xp_arvore = 1000
        # O caminho do sprite principal é relativo à pasta raiz do jogo.
        # Usado se a classe base precisar de um caminho de sprite individual no construtor.
        sprite_path_principal_relativo_jogo = "Sprites/Inimigos/Arvore Maldita/Arvore Maldita1.png"

        # Chama o construtor da classe base (InimigoBase)
        super().__init__(
            x, y,
            Arvore_Maldita.tamanho_sprite_definido[0], Arvore_Maldita.tamanho_sprite_definido[1], # Largura e Altura
            vida_arvore, velocidade, dano_contato_arvore, # Vida, Velocidade, Dano Contato
            xp_arvore, sprite_path_principal_relativo_jogo # XP, Caminho Sprite (para placeholder base)
        )
        # self.velocidade já é definido no InimigoBase (placeholder) ou na classe base real.
        # Se a classe base real não definir self.velocidade, a linha abaixo seria necessária:
        # self.velocidade = velocidade

        self.x = float(x) # Garante que x e y sejam float para movimento suave
        self.y = float(y)

        # Atribui as listas de sprites carregadas às instâncias
        self.sprites_idle = Arvore_Maldita.sprites_idle_arvore_carregados
        self.sprites_ataque_principal = Arvore_Maldita.sprites_ataque_principal_arvore_carregados
        self.sprites = self.sprites_idle # Começa com a animação de idle

        # Define a imagem inicial e o rect
        if self.sprites_idle and len(self.sprites_idle) > 0 and isinstance(self.sprites_idle[0], pygame.Surface):
            self.image = self.sprites_idle[0].copy() # Usa uma cópia do primeiro sprite de idle
        # Fallback se os sprites de idle não carregaram corretamente ou se self.image não foi definido pela base
        elif not (hasattr(self, 'image') and isinstance(self.image, pygame.Surface)):
            print(f"AVISO (Arvore_Maldita instance): Sprites de idle não disponíveis ou imagem base não definida. Usando placeholder para instância.")
            placeholder_img = pygame.Surface(Arvore_Maldita.tamanho_sprite_definido, pygame.SRCALPHA)
            placeholder_img.fill((40, 20, 5, 150)) # Cor placeholder
            self.image = placeholder_img
            if not self.sprites: self.sprites = [self.image] # Garante que self.sprites tenha ao menos uma imagem

        # Define o rect baseado na imagem (se existir) ou no tamanho definido
        if hasattr(self, 'image') and self.image is not None:
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            # Fallback para criar um rect se a imagem não estiver disponível
            self.rect = pygame.Rect(self.x, self.y, Arvore_Maldita.tamanho_sprite_definido[0], Arvore_Maldita.tamanho_sprite_definido[1])
            if not hasattr(self, 'image') or self.image is None: # Se ainda não tem imagem, cria uma placeholder
                 self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
                 self.image.fill((30,15,3,100))


        # Configurações de animação específicas da Arvore_Maldita
        self.sprite_index = 0 # Reinicia o índice do sprite
        self.intervalo_animacao_idle = 450 # ms
        self.intervalo_animacao_ataque_principal = 150 # ms (ataque mais rápido)
        self.intervalo_animacao = self.intervalo_animacao_idle # Começa com o intervalo de idle
        self.tempo_ultimo_update_animacao = pygame.time.get_ticks() # Reinicia o timer da animação

        # Estado e timers para o ataque principal
        self.is_attacking_principal = False # Flag se está atualmente no meio de um ataque
        self.attack_principal_duration = 1.8 # Duração do estado de ataque em segundos
        self.attack_principal_timer = 0.0 # Timer para controlar a duração do ataque
        self.attack_principal_damage = 50 # Dano do ataque principal
        self.attack_principal_range = Arvore_Maldita.tamanho_sprite_definido[0] * 0.8 # Alcance para iniciar o ataque
        self.attack_principal_cooldown = 4.0 # Cooldown entre ataques em segundos
        # Inicia com parte do cooldown já passado para permitir um ataque mais cedo no início
        self.last_attack_principal_time = pygame.time.get_ticks() - int(self.attack_principal_cooldown * 1000 * 0.75)

        # Hitbox para o ataque principal (diferente do rect de colisão do corpo)
        self.attack_principal_hitbox_size = (Arvore_Maldita.tamanho_sprite_definido[0] * 0.7, Arvore_Maldita.tamanho_sprite_definido[1] * 0.6)
        self.attack_principal_hitbox_offset_y = -Arvore_Maldita.tamanho_sprite_definido[1] * 0.1 # Deslocamento Y da hitbox
        self.attack_principal_hitbox = pygame.Rect(0,0,0,0) # Hitbox inicializada vazia
        self.hit_player_this_attack_swing = False # Para garantir que o jogador seja atingido apenas uma vez por "swing"
        self.xp_value_boss = xp_arvore # Usado por Luta_boss.py para saber o XP do chefe

    def _atualizar_hitbox_ataque_principal(self):
        # Atualiza a posição e tamanho da hitbox de ataque.
        if not self.is_attacking_principal:
            self.attack_principal_hitbox.size = (0,0) # Hitbox zerada se não estiver atacando
            return
        
        w, h = self.attack_principal_hitbox_size
        self.attack_principal_hitbox.size = (w,h)
        # Posiciona a hitbox à frente do inimigo, dependendo da direção
        if self.facing_right:
            self.attack_principal_hitbox.left = self.rect.centerx
        else:
            self.attack_principal_hitbox.right = self.rect.centerx
        self.attack_principal_hitbox.centery = self.rect.centery + self.attack_principal_hitbox_offset_y

    def iniciar_ataque_principal(self, player):
        # Verifica se pode iniciar o ataque principal.
        if not (hasattr(player, 'rect') and self.esta_vivo()): return # Jogador inválido ou árvore morta

        agora = pygame.time.get_ticks()
        distancia_ao_jogador = float('inf')
        if hasattr(player, 'rect') and player.rect is not None: # Verifica se player.rect existe
            distancia_ao_jogador = math.hypot(self.rect.centerx - player.rect.centerx, self.rect.centery - player.rect.centery)

        # Condições para atacar: não estar atacando, jogador no alcance, cooldown finalizado
        if not self.is_attacking_principal and \
           distancia_ao_jogador <= self.attack_principal_range and \
           (agora - self.last_attack_principal_time >= self.attack_principal_cooldown * 1000):
            
            self.is_attacking_principal = True
            self.attack_principal_timer = agora # Inicia o timer da duração do ataque
            self.last_attack_principal_time = agora # Registra o tempo do último ataque (para cooldown)
            self.hit_player_this_attack_swing = False # Reseta o flag de hit por swing
            
            self.sprites = self.sprites_ataque_principal # Muda para sprites de ataque
            self.intervalo_animacao = self.intervalo_animacao_ataque_principal # Animação de ataque mais rápida
            self.sprite_index = 0 # Reinicia animação de ataque
            self.tempo_ultimo_update_animacao = agora # Sincroniza timer da animação
            
            if Arvore_Maldita.som_ataque_arvore: Arvore_Maldita.som_ataque_arvore.play()

    def update(self, player, outros_inimigos=None, projeteis_inimigos_ref=None, tela_largura=None, altura_tela=None, dt_ms=None):
        # Método de atualização principal da Arvore_Maldita.
        if not self.esta_vivo(): return # Não faz nada se estiver morta

        agora = pygame.time.get_ticks()
        # Calcula delta time se não for fornecido
        if dt_ms is None:
            dt_ms = agora - getattr(self, '_last_update_time', agora) # getattr para evitar erro se _last_update_time não existir
            self._last_update_time = agora
            if dt_ms <= 0 : dt_ms = 16 # Evita dt_ms zero ou negativo, usa valor padrão

        # Verifica se o jogador é um objeto válido com os atributos esperados
        jogador_valido = (player is not None and 
                          hasattr(player, 'rect') and player.rect is not None and 
                          hasattr(player, 'receber_dano'))

        # Lógica de virar para o jogador
        if jogador_valido:
            if player.rect.centerx < self.rect.centerx: self.facing_right = False
            else: self.facing_right = True
        
        # Lógica de Ataque Principal
        if self.is_attacking_principal:
            self._atualizar_hitbox_ataque_principal() # Mantém a hitbox de ataque atualizada
            
            # Verifica colisão da hitbox de ataque com o jogador
            if jogador_valido and not self.hit_player_this_attack_swing and \
               self.attack_principal_hitbox.colliderect(player.rect):
                player.receber_dano(self.attack_principal_damage, self.rect) # Causa dano ao jogador
                self.hit_player_this_attack_swing = True # Marca que já atingiu neste "swing"
            
            # Verifica se a duração do ataque terminou
            if agora - self.attack_principal_timer >= self.attack_principal_duration * 1000:
                self.is_attacking_principal = False # Termina o estado de ataque
                self.sprites = self.sprites_idle # Volta para sprites de idle
                self.intervalo_animacao = self.intervalo_animacao_idle # Restaura intervalo de animação de idle
                self.sprite_index = 0 # Reinicia animação de idle
                self.tempo_ultimo_update_animacao = agora
                self.attack_principal_hitbox.size = (0,0) # Esconde/desativa a hitbox de ataque
        else:
            # Se não está atacando, tenta iniciar um ataque ou se mover
            if jogador_valido: self.iniciar_ataque_principal(player)
            
            # Movimento ocorre se não estiver atacando E tiver velocidade > 0
            if not self.is_attacking_principal and self.velocidade > 0:
                if jogador_valido:
                    # Move em direção ao jogador
                    self.mover_em_direcao(player.rect.centerx, player.rect.centery, dt_ms)
        
        # Chama o update da classe base (InimigoBase), que cuida da animação e outros comportamentos base.
        super().update(player, outros_inimigos, projeteis_inimigos_ref, tela_largura, altura_tela, dt_ms)

        # Atualiza as coordenadas x, y da Arvore_Maldita com base no seu rect.
        # Importante se a câmera ou outra lógica depender de self.x e self.y precisos.
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)


    def receber_dano(self, dano, fonte_dano_rect=None):
        # Sobrescreve o método receber_dano para adicionar lógica específica (sons).
        if not self.esta_vivo(): return # Já morto, não recebe mais dano

        vida_antes = self.hp
        super().receber_dano(dano, fonte_dano_rect) # Chama o método da classe base

        if self.esta_vivo(): # Se ainda estiver vivo após o dano
            if vida_antes > self.hp: # Verifica se realmente tomou dano (vida diminuiu)
                if Arvore_Maldita.som_dano_arvore: Arvore_Maldita.som_dano_arvore.play()
                self.last_hit_time = pygame.time.get_ticks() # Ativa o flash de hit
        elif vida_antes > 0: # Se morreu neste hit (vida_antes > 0 e agora hp <= 0)
            if Arvore_Maldita.som_morte_arvore: Arvore_Maldita.som_morte_arvore.play()
            # Outras lógicas de morte (ex: dropar item, dar XP) podem ser adicionadas aqui ou no loop principal do jogo.

    def desenhar(self, surface, camera_x, camera_y):
        # Chama o método de desenho da classe base.
        super().desenhar(surface, camera_x, camera_y)
        
        # DEBUG: Desenha a hitbox de ataque (descomente para visualizar)
        # if self.is_attacking_principal and self.attack_principal_hitbox.width > 0:
        #     # Cria um rect temporário para desenhar a hitbox na posição correta da tela (ajustada pela câmera)
        #     debug_rect_onscreen = self.attack_principal_hitbox.move(-camera_x, -camera_y)
        #     # Desenha um retângulo verde semi-transparente
        #     temp_surface = pygame.Surface(debug_rect_onscreen.size, pygame.SRCALPHA)
        #     temp_surface.fill((0, 255, 0, 100)) # Verde com alfa 100
        #     surface.blit(temp_surface, debug_rect_onscreen.topleft)
        #     pygame.draw.rect(surface, (0, 255, 0), debug_rect_onscreen, 2) # Contorno verde sólido


# Exemplo de como usar (requer inicialização do Pygame e um loop de jogo)
if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init() # Inicializa o mixer para os sons

    # Configurações da tela
    largura_tela = 800
    altura_tela = 600
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Teste Arvore Maldita")
    clock = pygame.time.Clock()

    # Cria um jogador placeholder para teste
    class JogadorTeste(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((50,50), pygame.SRCALPHA)
            self.image.fill((0,0,255, 150)) # Azul para o jogador
            self.rect = self.image.get_rect(center=(x,y))
            self.hp = 1000
        def receber_dano(self, dano, fonte_dano_rect=None):
            self.hp -= dano
            print(f"Jogador recebeu {dano} de dano. HP: {self.hp}")
        def update(self):
            pass # Jogador simples, não se move sozinho neste teste
        def desenhar(self, s, cx, cy):
            s.blit(self.image, (self.rect.x - cx, self.rect.y - cy))

    # Cria uma instância da Arvore_Maldita
    # A velocidade aqui é um valor arbitrário para teste, ajuste conforme necessário.
    # 0.3 é uma velocidade baixa, 1.0 média, >2.0 alta, dependendo do fator no mover_em_direcao.
    arvore = Arvore_Maldita(largura_tela // 2, altura_tela // 2, velocidade=0.5)
    
    # Cria um jogador de teste
    jogador = JogadorTeste(largura_tela // 3, altura_tela // 2)

    # Grupo de sprites para facilitar o desenho e atualização
    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(arvore)
    todos_sprites.add(jogador) # Adiciona jogador ao grupo se ele for um sprite

    camera_x, camera_y = 0, 0 # Simulação de câmera simples

    rodando = True
    while rodando:
        dt_ms = clock.tick(60) # Limita a 60 FPS e retorna o delta time em ms

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Tecla espaço para causar dano na árvore (teste)
                    print("Jogador atacou a árvore!")
                    arvore.receber_dano(50)
                if event.key == pygame.K_ESCAPE:
                    rodando = False
        
        # Movimento do jogador (exemplo simples com as setas)
        keys = pygame.key.get_pressed()
        player_speed = 300 * (dt_ms / 1000.0) # Velocidade do jogador em pixels por segundo
        if keys[pygame.K_LEFT]:
            jogador.rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            jogador.rect.x += player_speed
        if keys[pygame.K_UP]:
            jogador.rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            jogador.rect.y += player_speed


        # Atualiza a árvore (passando o jogador como alvo)
        # O jogador placeholder não tem um método update complexo, então não chamamos jogador.update()
        # mas a árvore precisa do jogador para sua lógica de IA.
        arvore.update(jogador, dt_ms=dt_ms) # Passa dt_ms para a árvore

        # Lógica de câmera simples (centraliza no jogador, se ele se mover muito)
        # camera_x = jogador.rect.centerx - largura_tela // 2
        # camera_y = jogador.rect.centery - altura_tela // 2

        # Desenho
        tela.fill((30, 30, 30)) # Fundo cinza escuro

        # Desenha todos os sprites do grupo (respeitando a ordem de adição)
        # for sprite in todos_sprites:
        #    if hasattr(sprite, 'desenhar'): # Se o sprite tiver um método desenhar customizado
        #        sprite.desenhar(tela, camera_x, camera_y)
        #    else: # Desenho padrão do Pygame para sprites (se self.image e self.rect existem)
        #        tela.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y - camera_y))
        
        # Desenho individual para garantir a ordem ou se não estiverem em um grupo gerenciado
        jogador.desenhar(tela, camera_x, camera_y)
        arvore.desenhar(tela, camera_x, camera_y) # Desenha a árvore
        
        # Desenha a vida da árvore (exemplo)
        if arvore.esta_vivo():
            pygame.draw.rect(tela, (255,0,0), (arvore.rect.x - camera_x, arvore.rect.y - 10 - camera_y, arvore.rect.width, 5))
            vida_percentual = arvore.hp / arvore.max_hp
            pygame.draw.rect(tela, (0,255,0), (arvore.rect.x - camera_x, arvore.rect.y - 10 - camera_y, arvore.rect.width * vida_percentual, 5))
        else:
            # Se a árvore morreu, pode-se exibir uma mensagem ou remover ela
            fonte_morte = pygame.font.SysFont(None, 50)
            texto_morte = fonte_morte.render("Árvore Derrotada!", True, (255,200,200))
            tela.blit(texto_morte, (largura_tela//2 - texto_morte.get_width()//2, altura_tela//2 - texto_morte.get_height()//2))
            # arvore.kill() # Remove dos grupos de sprites se estiver usando-os para update/draw


        pygame.display.flip() # Atualiza a tela inteira

    pygame.quit()
