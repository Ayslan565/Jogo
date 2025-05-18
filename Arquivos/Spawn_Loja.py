# Spawn_Loja.py

# Este arquivo define a probabilidade e o intervalo mínimo de spawn da loja especial no jogo.

# Probabilidade de a loja aparecer (valor entre 0.0 e 1.0)
# Esta probabilidade é verificada quando um novo bloco de mapa é gerado ao redor do jogador,
# MAS apenas se o intervalo mínimo desde o último spawn da loja tiver passado.
# Por exemplo:
# 0.1 significa 10% de chance
# 0.5 significa 50% de chance
# 1.0 significa 100% de chance (sempre aparece se as condições de intervalo forem atendidas)
# 0.0 significa 0% de chance (nunca aparece)

PROBABILIDADE_SPAWN_LOJA = 0.2  # Defina aqui a probabilidade desejada (ex: 20%)

# Intervalo mínimo em segundos entre os spawns bem-sucedidos da loja.
# A loja só poderá spawnar se o tempo atual for pelo menos este intervalo após o último spawn.
INTERVALO_MINIMO_SPAWN_LOJA = 300 # Definido para 300 segundos (5 minutos)

# Você pode adicionar outras configurações relacionadas ao spawn da loja aqui, se necessário.
# Por exemplo:
# CONDICAO_ESPECIAL_SPAWN = True # Flag para ativar ou desativar spawns especiais

# Exemplo de como usar estas variáveis em outro arquivo (por exemplo, no seu loop principal ou gerenciador de eventos):
# import random
# import time
# from Spawn_Loja import PROBABILIDADE_SPAWN_LOJA, INTERVALO_MINIMO_SPAWN_LOJA

# last_shop_spawn_time = 0 # Inicialize no início do seu jogo

# def tentar_spawnar_loja(current_time):
#     global last_shop_spawn_time
#     if current_time - last_shop_spawn_time >= INTERVALO_MINIMO_SPAWN_LOJA:
#         if random.random() < PROBABILIDADE_SPAWN_LOJA:
#             print("A loja apareceu!")
#             last_shop_spawn_time = current_time # Atualiza o tempo do último spawn
#             # Lógica para criar e posicionar a loja
#             return True # Loja spawnada
#         else:
#             print("A probabilidade de spawn da loja falhou desta vez.")
#             return False # Probabilidade falhou
#     else:
#         # print("Intervalo mínimo de spawn da loja ainda não passou.") # Opcional: debug
#         return False # Intervalo mínimo não passou

# # Chame tentar_spawnar_loja(time.time()) no seu loop de jogo ou em um evento apropriado
# # (por exemplo, quando um novo bloco de mapa é gerado).
# Spawn_Loja.py

# Este arquivo define a probabilidade e o intervalo mínimo de spawn da loja especial no jogo.

# Probabilidade de a loja aparecer (valor entre 0.0 e 1.0)
# Esta probabilidade é verificada quando um novo bloco de mapa é gerado ao redor do jogador,
# MAS apenas se o intervalo mínimo desde o último spawn da loja tiver passado.
# Por exemplo:
# 0.1 significa 10% de chance
# 0.5 significa 50% de chance
# 1.0 significa 100% de chance (sempre aparece se as condições de intervalo forem atendidas)
# 0.0 significa 0% de chance (nunca aparece)

PROBABILIDADE_SPAWN_LOJA = 1.0  # Defina aqui a probabilidade desejada (ex: 20%)

# Intervalo mínimo em segundos entre os spawns bem-sucedidos da loja.
# A loja só poderá spawnar se o tempo atual for pelo menos este intervalo após o último spawn.
INTERVALO_MINIMO_SPAWN_LOJA = 10 # Definido para 300 segundos (5 minutos)

# Você pode adicionar outras configurações relacionadas ao spawn da loja aqui, se necessário.
# Por exemplo:
# CONDICAO_ESPECIAL_SPAWN = True # Flag para ativar ou desativar spawns especiais

# Exemplo de como usar estas variáveis em outro arquivo (por exemplo, no seu loop principal ou gerenciador de eventos):
# import random
# import time
# from Spawn_Loja import PROBABILIDADE_SPAWN_LOJA, INTERVALO_MINIMO_SPAWN_LOJA

# last_shop_spawn_time = 0 # Inicialize no início do seu jogo

# def tentar_spawnar_loja(current_time):
#     global last_shop_spawn_time
#     if current_time - last_shop_spawn_time >= INTERVALO_MINIMO_SPAWN_LOJA:
#         if random.random() < PROBABILIDADE_SPAWN_LOJA:
#             print("A loja apareceu!")
#             last_shop_spawn_time = current_time # Atualiza o tempo do último spawn
#             # Lógica para criar e posicionar a loja
#             return True # Loja spawnada
#         else:
#             print("A probabilidade de spawn da loja falhou desta vez.")
#             return False # Probabilidade falhou
#     else:
#         # print("Intervalo mínimo de spawn da loja ainda não passou.") # Opcional: debug
#         return False # Intervalo mínimo não passou

# # Chame tentar_spawnar_loja(time.time()) no seu loop de jogo ou em um evento apropriado
# # (por exemplo, quando um novo bloco de mapa é gerado).
