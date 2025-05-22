# C:\Users\aysla\Documents\Jogo_Asrahel\Jogo\Arquivos\Roda_Armas.py
# DEBUG: Confirmação de que Roda_Armas.py está sendo carregado
print("DEBUG: Roda_Armas.py está sendo carregado e atualizado.")

import tkinter as tk
import math
import os

# Importa as classes de arma do seu jogo
# O PATH DEVE ESTAR CORRETO PARA ONDE SUAS CLASSES DE ARMA ESTÃO
# Assumindo que este arquivo 'Roda_Armas.py' está na mesma pasta 'Arquivos'
# que a pasta 'Armas', então os imports relativos à 'Arquivos' funcionam.
from Armas.weapon import Weapon # Classe base Weapon
from Armas.AdagaFogo import AdagaFogo
from Armas.EspadaBrasas import EspadaBrasas
from Armas.EspadaCaida import EspadaCaida
from Armas.EspadaFogoAzul import EspadaFogoAzul
from Armas.EspadaLua import EspadaLua
from Armas.EspadaPenitencia import EspadaPenitencia
from Armas.EspadaSacraDasBrasas import EspadaSacraDasBrasas
from Armas.MachadoBarbaro import MachadoBarbaro
from Armas.MachadoCeruleo import MachadoCeruleo
from Armas.MachadoMacabro import MachadoMacabro
from Armas.MachadoMarfim import MachadoMarfim

# Adicione mais armas conforme necessário

class WeaponWheelUI: # <--- ESTA É A CLASSE QUE Game.py TENTA IMPORTAR
    # MODIFICADO: Adicionado player_owned_weapons_ref ao __init__
    def __init__(self, parent_game_instance, on_weapon_selected_callback, player_owned_weapons_ref):
        self.parent_game_instance = parent_game_instance
        self.on_weapon_selected_callback = on_weapon_selected_callback

        self.tk_root = None
        self.toplevel_window = None
        self.canvas = None

        # MODIFICADO: A lista de armas agora é a referência passada pelo jogador
        self.weapons = player_owned_weapons_ref 
        
        self.cur_weapon = None
        self._weapon_images = {}

    def create_wheel_window(self):
        # Crie uma janela Toplevel (uma janela independente) para a roda
        self.tk_root = tk.Tk() # Cria uma instância Tkinter Root temporária para o Toplevel
        self.tk_root.withdraw() # Esconde a janela Root principal vazia

        self.toplevel_window = tk.Toplevel(self.tk_root)
        self.toplevel_window.title("Seleção de Arma")
        self.toplevel_window.geometry("500x500")
        self.toplevel_window.resizable(False, False)
        self.toplevel_window.attributes("-topmost", True)
        self.toplevel_window.overrideredirect(True)

        screen_width = self.toplevel_window.winfo_screenwidth()
        screen_height = self.toplevel_window.winfo_screenheight()
        x = (screen_width // 2) - (500 // 2)
        y = (screen_height // 2) - (500 // 2)
        self.toplevel_window.geometry(f"500x500+{x}+{y}")

        self.canvas = tk.Canvas(self.toplevel_window, width=500, height=500, bg="lightgray", highlightbackground="black", highlightthickness=2)
        self.canvas.pack(fill="both", expand=True)

        can_w = 500
        can_h = 500

        self.weapon_var = tk.StringVar()
        self.weapon_var.set("Arma Atual: Nenhuma")

        self.weapon_lbl = tk.Label(self.canvas, textvariable=self.weapon_var, bg=self.canvas["bg"], font=("Arial", 14, "bold"))
        self.canvas.create_window(can_w // 2, 50, window=self.weapon_lbl)

        out_circle_x = can_w // 4
        out_circle_y = can_h // 4
        out_circle_x1 = can_w - out_circle_x
        out_circle_y1 = can_h - out_circle_y

        self.out_circle = self.canvas.create_oval(out_circle_x, out_circle_y, out_circle_x1, out_circle_y1, tags="out_circle", width=2)

        self._draw_weapon_arcs_and_images(can_w, can_h, out_circle_x, out_circle_y, out_circle_x1, out_circle_y1)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.toplevel_window.bind("<Escape>", self.hide_wheel)

    # NOVO MÉTODO: Redesenha o conteúdo da roda com as armas atuais
    def _redraw_wheel_content(self):
        if self.canvas:
            self.canvas.delete("weapon_arc") # Deleta todos os arcos existentes
            self.canvas.delete("weapon_image") # Deleta todas as imagens existentes
            self.canvas.delete("weapon_text") # Deleta todos os textos existentes
            self._weapon_images = {} # Limpa as imagens em cache

            can_w = 500
            can_h = 500
            out_circle_x = can_w // 4
            out_circle_y = can_h // 4
            out_circle_x1 = can_w - out_circle_x
            out_circle_y1 = can_h - out_circle_y

            self._draw_weapon_arcs_and_images(can_w, can_h, out_circle_x, out_circle_y, out_circle_x1, out_circle_y1)
            self.canvas.update_idletasks() # Força a atualização do canvas

    def _draw_weapon_arcs_and_images(self, can_w, can_h, out_circle_x, out_circle_y, out_circle_x1, out_circle_y1):
        num_weapons = len(self.weapons)
        if num_weapons == 0:
            # Se não houver armas, exibe uma mensagem
            self.canvas.create_text(can_w // 2, can_h // 2, text="Nenhuma arma no inventário.", fill="black", font=("Arial", 12, "bold"))
            return

        angle_step = 360 / num_weapons
        start_angle = 90

        center_x = can_w // 2
        center_y = can_h // 2
        radius = (out_circle_x1 - out_circle_x) // 2

        for i, weapon in enumerate(self.weapons):
            end_angle = start_angle + angle_step

            arc_id = self.canvas.create_arc(out_circle_x, out_circle_y, out_circle_x1, out_circle_y1,
                                            start=start_angle, extent=angle_step,
                                            fill="", outline="black", width=1,
                                            tags=(weapon.tag, "weapon_arc"))

            mid_angle_rad = math.radians(start_angle + angle_step / 2)

            image_x = center_x + (radius * 0.75) * math.cos(mid_angle_rad)
            image_y = center_y - (radius * 0.75) * math.sin(mid_angle_rad)

            if hasattr(weapon, 'img_path') and weapon.img_path:
                try:
                    game_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    full_img_path = os.path.join(game_dir, weapon.img_path)

                    if not os.path.exists(full_img_path):
                        print(f"ATENÇÃO: Imagem não encontrada para {weapon.name}: {full_img_path}. Usando texto.")
                        raise FileNotFoundError

                    img_loaded = tk.PhotoImage(file=full_img_path)
                    self._weapon_images[weapon.name] = img_loaded # Armazena a referência para evitar que seja coletada pelo garbage collector
                    self.canvas.create_image(image_x, image_y, image=img_loaded, tags=(weapon.tag + "_img", weapon.tag, "weapon_image"))

                    self.canvas.tag_bind(weapon.tag + "_img", "<Enter>", lambda e, w_tag=weapon.tag, w_fill=weapon.fill_color: self.highlight_item(w_tag, w_fill))
                    self.canvas.tag_bind(weapon.tag + "_img", "<Leave>", lambda e, w_tag=weapon.tag: self.unhighlight_item(w_tag))
                    self.canvas.tag_bind(weapon.tag + "_img", "<Button-1>", lambda e, weapon_obj=weapon: self.update_weapon(weapon_obj))

                except (tk.TclError, FileNotFoundError) as e:
                    print(f"Erro ao carregar imagem para {weapon.name}: {e}. Desenhando texto.")
                    self.canvas.create_text(image_x, image_y, text=weapon.name, fill="black", font=("Arial", 8), tags=(weapon.tag + "_text", weapon.tag, "weapon_text"))
            else:
                self.canvas.create_text(image_x, image_y, text=weapon.name, fill="black", font=("Arial", 8), tags=(weapon.tag + "_text", weapon.tag, "weapon_text"))

            self.canvas.tag_bind(arc_id, "<Enter>", lambda e, w_tag=weapon.tag, w_fill=weapon.fill_color: self.highlight_item(w_tag, w_fill))
            self.canvas.tag_bind(arc_id, "<Leave>", lambda e, w_tag=weapon.tag: self.unhighlight_item(w_tag))
            self.canvas.tag_bind(arc_id, "<Button-1>", lambda e, weapon_obj=weapon: self.update_weapon(weapon_obj))

            start_angle = end_angle

    def highlight_item(self, tag, color):
        self.canvas.itemconfigure(tag, fill=color, width=3)
        self.canvas.itemconfigure("out_circle", outline=color, width=3)
        self.canvas.update()

    def unhighlight_item(self, tag):
        self.canvas.itemconfigure(tag, fill="", width=1)
        self.canvas.itemconfigure("out_circle", outline="black", width=2)
        self.canvas.update()

    def update_weapon(self, weapon):
        for w_obj in self.weapons:
            self.canvas.itemconfigure(w_obj.tag, fill="")

        self.cur_weapon = weapon
        self.weapon_var.set("Arma Atual: " + weapon.name)

        self.canvas.itemconfigure(weapon.tag, fill=weapon.fill_color)

        print(f"Arma Selecionada: {self.cur_weapon.name}")

        if self.on_weapon_selected_callback:
            self.on_weapon_selected_callback(self.cur_weapon)

        self.hide_wheel()

    def on_canvas_click(self, event):
        clicked_items = self.canvas.find_withtag("current")
        if not any("weapon_arc" in self.canvas.gettags(item) or "weapon_image" in self.canvas.gettags(item) for item in clicked_items):
            self.hide_wheel()

    def show_wheel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.create_wheel_window()
        
        # Sempre redesenha o conteúdo da roda ao mostrar para refletir o inventário atual do jogador
        self._redraw_wheel_content() 

        self.toplevel_window.deiconify()
        self.toplevel_window.grab_set()
        self.toplevel_window.focus_set()
        self.tk_root.update_idletasks()

    def hide_wheel(self, event=None):
        if self.toplevel_window and self.toplevel_window.winfo_exists():
            self.toplevel_window.grab_release()
            self.toplevel_window.withdraw()
            # self.tk_root.quit() # Comentado para permitir reabrir
            # A Root pode permanecer para ser reusada.
            # Se fechar o tk_root, precisará de uma nova Root na próxima vez que mostrar a roda.
            # Para evitar problemas com tk_root.mainloop(), manter ela viva mas escondida é melhor.

    def process_events(self):
        if self.tk_root and self.tk_root.winfo_exists():
            self.tk_root.update_idletasks()
            self.tk_root.update()

    # NOVO MÉTODO: Adiciona uma arma à lista de exibição e redesenha a roda
    def add_weapon_to_display_list(self, weapon_instance: Weapon):
        # A lista self.weapons já é a referência para jogador.owned_weapons,
        # então, se a arma já foi adicionada ao jogador, ela já está aqui.
        # Apenas forçamos a redesenhar a roda.
        if self.toplevel_window and self.toplevel_window.winfo_exists():
            self._redraw_wheel_content()
        print(f"DEBUG(WeaponWheelUI): Roda de armas atualizada com nova arma: {weapon_instance.name}")


# --- Suas classes de Arma (devem vir dos seus arquivos Armas/*.py) ---
# Coloquei aqui apenas para o exemplo standalone,
# no seu weapon_wheel_tkinter.py elas devem vir dos imports.

class Weapon:
    def __init__(self):
        self.name = "Arma Padrão"
        self.img_path = None
        self.fill_color = "gray"
        self.tag = f"weapon_{self.name.replace(' ', '_').lower()}" # Gerando um tag único
        self.level = 1.0 # Nível padrão para a arma base
        self.damage = 10.0 # Dano padrão
        self.attack_range = 50.0 # Alcance padrão
        self.cooldown = 0.5 # Cooldown padrão
        self.attack_animation_duration = 300 # Duração padrão da animação em ms

class AdagaFogo(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Adaga de Fogo"
        self.img_path = "Sprites/Armas/AdagaFogo50x50.png"
        self.fill_color = "orange"
        self.tag = "adaga_fogo"
        self.damage = 15.0
        self.attack_range = 60.0
        self.cooldown = 0.4
        self.level = 1.5

class EspadaBrasas(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Espada Brasas"
        self.img_path = "Sprites/Armas/EspadaBrasas50x50.png"
        self.fill_color = "darkred"
        self.tag = "espada_brasas"
        self.damage = 20.0
        self.attack_range = 70.0
        self.cooldown = 0.6
        self.level = 2.0

class EspadaCaida(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Espada Caída"
        self.img_path = "Sprites/Armas/EspadaCaida50x50.png"
        self.fill_color = "darkgray"
        self.tag = "espada_caida"
        self.damage = 12.0
        self.attack_range = 65.0
        self.cooldown = 0.5
        self.level = 1.0

class EspadaFogoAzul(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Espada Fogo Azul"
        self.img_path = "Sprites/Armas/EspadaFogoAzul50x50.png"
        self.fill_color = "blue"
        self.tag = "espada_fogo_azul"
        self.damage = 25.0
        self.attack_range = 75.0
        self.cooldown = 0.55
        self.level = 2.5

class EspadaLua(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Espada da Lua"
        self.img_path = "Sprites/Armas/EspadaLua50x50.png"
        self.fill_color = "lightblue"
        self.tag = "espada_lua"
        self.damage = 30.0
        self.attack_range = 80.0
        self.cooldown = 0.7
        self.level = 3.0

class EspadaPenitencia(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Espada Penitência"
        self.img_path = "Sprites/Armas/EspadaPenitencia50x50.png"
        self.fill_color = "purple"
        self.tag = "espada_penitencia"
        self.damage = 28.0
        self.attack_range = 70.0
        self.cooldown = 0.65
        self.level = 2.8

class EspadaSacraDasBrasas(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Espada Sacra das Brasas"
        self.img_path = "Sprites/Armas/EspadaSacraDasBrasas50x50.png"
        self.fill_color = "gold"
        self.tag = "espada_sacra_brasas"
        self.damage = 35.0
        self.attack_range = 85.0
        self.cooldown = 0.75
        self.level = 3.0

class MachadoBarbaro(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Machado Bárbaro"
        self.img_path = "Sprites/Armas/MachadoBarbaro50x50.png"
        self.fill_color = "brown"
        self.tag = "machado_barbaro"
        self.damage = 22.0
        self.attack_range = 55.0
        self.cooldown = 0.8
        self.level = 2.0

class MachadoCeruleo(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Machado Cerúleo"
        self.img_path = "Sprites/Armas/MachadoCeruleo50x50.png"
        self.fill_color = "cadetblue"
        self.tag = "machado_ceruleo"
        self.damage = 27.0
        self.attack_range = 60.0
        self.cooldown = 0.7
        self.level = 2.5

class MachadoCeruleoDaEstrelaCadente(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Machado da Estrela Cadente"
        self.img_path = "Sprites/Armas/MachadoCeruleoDaEstrelaCadente50x50.png"
        self.fill_color = "darkblue"
        self.tag = "machado_estrela_cadente"
        self.damage = 32.0
        self.attack_range = 65.0
        self.cooldown = 0.85
        self.level = 3.0

class MachadoMacabro(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Machado Macabro"
        self.img_path = "Sprites/Armas/MachadoMacabro50x50.png"
        self.fill_color = "darkgreen"
        self.tag = "machado_macabro"
        self.damage = 24.0
        self.attack_range = 58.0
        self.cooldown = 0.75
        self.level = 2.2

class MachadoMarfim(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Machado Marfim"
        self.img_path = "Sprites/Armas/MachadoMarfim50x50.png"
        self.fill_color = "ivory"
        self.tag = "machado_marfim"
        self.damage = 26.0
        self.attack_range = 62.0
        self.cooldown = 0.72
        self.level = 2.4

# Dummy class for Sword if not imported from elsewhere
class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Espada Padrão"
        self.img_path = "Sprites/Armas/EspadaPadrao50x50.png" # EX.: Ajuste o caminho da imagem
        self.fill_color = "red"
        self.tag = "sword_default"
        self.damage = 10.0
        self.attack_range = 50.0
        self.cooldown = 0.5
        self.level = 1.0
