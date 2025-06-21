# Arquivo: Arquivos/testar_imports.py

def testar_importacao_inimigos():
    """
    Testa a importação de todas as classes de inimigos de forma explícita
    e exibe o status de cada uma.
    """
    print("DEBUG: Iniciando importação de todas as classes de inimigos...")

    # --- Importando Inimigos da Natureza e Floresta ---
    print("\n--- Importando Inimigos da Natureza e Floresta ---")
    try:
        from Inimigos.Arvore_Maldita import Arvore_Maldita
        print("  (+) Arvore_Maldita importada.")
    except ImportError:
        print("  (-) AVISO: Arvore_Maldita não encontrada.")

    try:
        from Inimigos.Planta_Carnivora import Planta_Carnivora
        print("  (+) Planta_Carnivora importada.")
    except ImportError:
        print("  (-) AVISO: Planta_Carnivora não encontrada.")

    try:
        from Inimigos.Espantalho import Espantalho
        print("  (+) Espantalho importado.")
    except ImportError:
        print("  (-) AVISO: Espantalho não encontrado.")

    try:
        from Inimigos.Mae_Natureza import Mae_Natureza
        print("  (+) Mae_Natureza importada.")
    except ImportError:
        print("  (-) AVISO: Mae_Natureza não encontrada.")

    try:
        from Inimigos.Espirito_Das_Flores import Espirito_Das_Flores
        print("  (+) Espirito_Das_Flores importado.")
    except ImportError:
        print("  (-) AVISO: Espirito_Das_Flores não encontrado.")

    try:
        from Inimigos.Lobo import Lobo
        print("  (+) Lobo importado.")
    except ImportError:
        print("  (-) AVISO: Lobo não encontrado.")

    try:
        from Inimigos.Urso import Urso
        print("  (+) Urso importado.")
    except ImportError:
        print("  (-) AVISO: Urso não encontrado.")

    # --- Importando Inimigos Gélidos ---
    print("\n--- Importando Inimigos Gélidos ---")
    try:
        from Inimigos.BonecoDeNeve import BonecoDeNeve
        print("  (+) BonecoDeNeve importado.")
    except ImportError:
        print("  (-) AVISO: BonecoDeNeve não encontrado.")

    try:
        from Inimigos.Golem_Neve import Golem_Neve
        print("  (+) Golem_Neve importado.")
    except ImportError:
        print("  (-) AVISO: Golem_Neve não encontrado.")

    # --- Importando Inimigos Sobrenaturais e Mortos-Vivos ---
    print("\n--- Importando Inimigos Sobrenaturais e Mortos-Vivos ---")
    try:
        from Inimigos.Fantasma import Fantasma
        print("  (+) Fantasma importado.")
    except ImportError:
        print("  (-) AVISO: Fantasma não encontrado.")

    try:
        from Inimigos.Vampiro import Vampiro
        print("  (+) Vampiro importado.")
    except ImportError:
        print("  (-) AVISO: Vampiro não encontrado.")

    try:
        from Inimigos.Demonio import Demonio
        print("  (+) Demonio importado.")
    except ImportError:
        print("  (-) AVISO: Demonio não encontrado.")

    # --- Importando Inimigos Mágicos e Elementais ---
    print("\n--- Importando Inimigos Mágicos e Elementais ---")
    try:
        from Inimigos.Fenix import Fenix
        print("  (+) Fenix importada.")
    except ImportError:
        print("  (-) AVISO: Fenix não encontrada.")

    try:
        from Inimigos.Maga import Maga
        print("  (+) Maga importada.")
    except ImportError:
        print("  (-) AVISO: Maga não encontrada.")

    # --- Importando Inimigos Humanoides ---
    print("\n--- Importando Inimigos Humanoides ---")
    try:
        from Inimigos.Troll import Troll
        print("  (+) Troll importado.")
    except ImportError:
        print("  (-) AVISO: Troll não encontrado.")

    try:
        from Inimigos.Goblin import Goblin
        print("  (+) Goblin importado.")
    except ImportError:
        print("  (-) AVISO: Goblin não encontrado.")

    try:
        from Inimigos.Cavaleiro import Cavaleiro
        print("  (+) Cavaleiro importado.")
    except ImportError:
        print("  (-) AVISO: Cavaleiro não encontrado.")

    print("\nDEBUG: Importação de inimigos concluída.")


# --- Execução do Teste ---
# A função é chamada diretamente para executar os testes quando o arquivo for rodado.
testar_importacao_inimigos()