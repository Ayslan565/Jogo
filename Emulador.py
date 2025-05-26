import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
import os
import platform
import subprocess # Adicionado para executar subprocessos
import sys # Adicionado para sys.exit() e sys.executable

# --- Configurações de Estilo (CORES) ---
COR_FUNDO = "#1e1e2e"
COR_TEXTO = "#cdd6f4"
COR_DESTAQUE = "#89b4fa"
COR_BOTAO = "#313244"
COR_BOTAO_HOVER = "#45475a"
COR_BOTAO_TEXTO = "#cdd6f4"
COR_BORDA_BOTAO = COR_DESTAQUE

# --- Variáveis Globais para Fontes (para serem definidas uma vez) ---
FONTE_TITULO_GLOBAL = None
FONTE_BOTAO_GLOBAL = None

# --- Variáveis Globais para a GUI (serão recriadas) ---
janela_atual = None


# --- Classe para Botões Estilizados ---
class BotaoEstilizado(tk.Button):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)
        # Assegura que FONTE_BOTAO_GLOBAL está definida antes de ser usada
        font_a_usar = FONTE_BOTAO_GLOBAL if FONTE_BOTAO_GLOBAL else ("Arial", 16) # Fallback
        self.config(
            font=font_a_usar, bg=COR_BOTAO, fg=COR_BOTAO_TEXTO,
            activebackground=COR_BOTAO_HOVER, activeforeground=COR_DESTAQUE,
            relief=tk.FLAT, borderwidth=2, highlightthickness=2,
            highlightbackground=COR_BORDA_BOTAO, highlightcolor=COR_DESTAQUE,
            pady=12, padx=25
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    def on_enter(self, e): self.config(bg=COR_BOTAO_HOVER, fg=COR_DESTAQUE)
    def on_leave(self, e): self.config(bg=COR_BOTAO, fg=COR_BOTAO_TEXTO)


# --- Função para lançar jogo externo, fechar seletor, e reabrir seletor ---
def lancar_jogo_e_reabrir_seletor(nome_jogo, jogo_info):
    global janela_atual

    # 1. Destruir a janela atual do seletor
    if janela_atual and janela_atual.winfo_exists():
        print("A fechar o seletor para iniciar o jogo...")
        janela_atual.destroy() # Isto termina o mainloop atual
        janela_atual = None # Limpa a referência

    # 2. Executar o jogo externo (usando subprocess.call para bloquear)
    caminho_script_relativo = jogo_info["script"]
    
    # USA O EXECUTÁVEL PYTHON QUE ESTÁ A RODAR ESTE SCRIPT
    comando_python = sys.executable 
    print(f"A usar o interpretador Python: {comando_python}")

    try:
        caminho_base_seletor = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        caminho_base_seletor = os.getcwd()
        print(f"Aviso: __file__ não definido. A usar o diretório de trabalho atual como base: {caminho_base_seletor}")
        
    caminho_absoluto_jogo = os.path.join(caminho_base_seletor, caminho_script_relativo)

    if not os.path.exists(caminho_absoluto_jogo):
        print(f"ERRO: O ficheiro do jogo '{nome_jogo}' não foi encontrado em: {caminho_absoluto_jogo}.")
    else:
        # Envolve o caminho do interpretador e do script com aspas para lidar com espaços
        comando_final = f"\"{comando_python}\" \"{caminho_absoluto_jogo}\""
        print(f"A executar o jogo: {comando_final}. O seletor será reaberto após o jogo fechar.")
        try:
            exit_code = subprocess.call(comando_final, shell=True) # shell=True pode ser necessário
            print(f"Jogo '{nome_jogo}' finalizado com código de saída: {exit_code}")
        except Exception as e_exec:
            print(f"Ocorreu um erro ao executar o jogo '{nome_jogo}': {e_exec}")

    # 3. Após o jogo (ou erro na execução/ficheiro não encontrado), re-chamar a função para criar a GUI
    print("A reabrir o seletor de jogos...")
    criar_e_rodar_seletor_gui()


# --- Função principal para criar e rodar a GUI do seletor ---
def criar_e_rodar_seletor_gui():
    global janela_atual
    global FONTE_TITULO_GLOBAL, FONTE_BOTAO_GLOBAL

    janela_atual = tk.Tk()
    janela_atual.title("🕹️ ARCADE LEGENDS SELECTOR 🕹️")
    janela_atual.configure(bg=COR_FUNDO)

    if FONTE_TITULO_GLOBAL is None:
        try:
            FONTE_TITULO_GLOBAL = tkFont.Font(family="Impact", size=30, weight="bold")
            FONTE_BOTAO_GLOBAL = tkFont.Font(family="Consolas", size=16, weight="bold")
        except tk.TclError:
            FONTE_TITULO_GLOBAL = ("Arial", 28, "bold")
            FONTE_BOTAO_GLOBAL = ("Arial", 16, "bold")
            print("Aviso: Fonte 'Impact' ou 'Consolas' não encontrada. A usar fontes padrão.")

    largura_janela = 700
    altura_janela = 500
    largura_tela = janela_atual.winfo_screenwidth()
    altura_tela = janela_atual.winfo_screenheight()
    x_pos = (largura_tela // 2) - (largura_janela // 2)
    y_pos = (altura_tela // 2) - (altura_janela // 2)
    janela_atual.geometry(f'{largura_janela}x{altura_janela}+{x_pos}+{y_pos}')
    janela_atual.resizable(False, False)

    frame_principal = tk.Frame(janela_atual, bg=COR_FUNDO)
    frame_principal.pack(pady=30, padx=30, expand=True, fill=tk.BOTH)

    label_titulo = tk.Label(frame_principal, text="SELECT YOUR LEGEND", font=FONTE_TITULO_GLOBAL, fg=COR_DESTAQUE, bg=COR_FUNDO, pady=25)
    label_titulo.pack()

    jogos = [
        {
            "nome": "✨ LENDA DE ASHAEL (Janela Separada) ✨",
            "script": os.path.join("Jogo", "Arquivos", "Game.py")
        },
        {
            "nome": "🚀 GALACTIC BLASTER (Externo)",
            "script": os.path.join("SpaceShooter", "main_shooter.py") # Exemplo
        },
        {
            "nome": "🐍 PYTHON PITFALL (Externo)",
            "script": os.path.join("SnakeGame", "snake.py") # Exemplo
        },
    ]

    for jogo_info_item in jogos:
        comando_botao = lambda j_info=jogo_info_item: lancar_jogo_e_reabrir_seletor(j_info["nome"], j_info)
        botao = BotaoEstilizado(
            frame_principal,
            text=jogo_info_item["nome"],
            command=comando_botao
        )
        botao.pack(pady=15, fill=tk.X, padx=60)

    botao_sair_app = BotaoEstilizado(
        frame_principal,
        text="EXIT ARCADE",
        command=lambda: sys.exit(0)
    )
    botao_sair_app.config(highlightbackground="#e64553", pady=15)
    botao_sair_app.pack(pady=(30,20), side=tk.BOTTOM, padx=60)

    janela_atual.mainloop()

# --- Ponto de Entrada Principal do Script ---
if __name__ == "__main__":
    criar_e_rodar_seletor_gui()
