# Roda_Armas.py
# DEBUG: Confirmação de que Roda_Armas.py está sendo carregado e atualizado.
print("DEBUG: Roda_Armas.py está sendo carregado e atualizado.")

import tkinter as tk
from tkinter import PhotoImage # Explicit import for PhotoImage
import math
import os
import threading # Import threading para referenciar o tipo Event, se necessário para type hints

# Importa as classes de arma do seu jogo
# Certifique-se de que os caminhos e nomes das classes estão corretos.
try:
    from Armas.weapon import Weapon 
    from Armas.AdagaFogo import AdagaFogo
    from Armas.EspadaBrasas import EspadaBrasas
    from Armas.EspadaCaida import EspadaCaida
    from Armas.EspadaFogoAzul import EspadaFogoAzul
    from Armas.EspadaLua import EspadaLua
    from Armas.EspadaPenitencia import EspadaPenitencia
    # from Armas.EspadaSacraDasBrasas import EspadaSacraDasBrasas # Descomente se existir
    from Armas.MachadoBarbaro import MachadoBarbaro
    from Armas.MachadoCeruleo import MachadoCeruleo
    from Armas.MachadoMacabro import MachadoMacabro
    from Armas.MachadoMarfim import MachadoMarfim
    # from Armas.MachadoCeruleoDaEstrelaCadente import MachadoCeruleoDaEstrelaCadente # Descomente se existir
except ImportError as e:
    print(f"DEBUG(Roda_Armas): Erro ao importar classes de armas: {e}. A roda de armas pode não funcionar corretamente.")
    # Define fallbacks para evitar crash imediato se as importações falharem
    Weapon = AdagaFogo = EspadaBrasas = EspadaCaida = EspadaFogoAzul = EspadaLua = None
    EspadaPenitencia = MachadoBarbaro = MachadoCeruleo = MachadoMacabro = MachadoMarfim = None


class WeaponWheelUI:
    # __init__ AGORA ESPERA 4 ARGUMENTOS (parent_game_instance pode ser None)
    def __init__(self, parent_game_instance, on_weapon_selected_callback, player_owned_weapons_ref, active_event_ref: threading.Event):
        self.parent_game_instance = parent_game_instance 
        self.on_weapon_selected_callback = on_weapon_selected_callback
        self.player_weapons_ref = player_owned_weapons_ref 
        self.active_event_ref = active_event_ref # Armazena a referência ao evento do Game.py

        self.tk_root = None
        self.toplevel_window = None
        self.canvas = None
        
        self.cur_weapon_instance = None 
        self._weapon_images_tk = {}  # Cache para PhotoImage objects para evitar garbage collection

        self.wheel_config = {
            "width": 500,
            "height": 500,
            "bg_color": "gray20", 
            "border_color": "black",
            "border_thickness": 2,
            "label_font": ("Arial", 14, "bold"),
            "label_bg": "gray25",
            "label_fg": "white",
            "item_font": ("Arial", 9, "bold"),
            "item_text_color": "white",
            "arc_outline": "gray40",
            "arc_width": 1,
            "highlight_color_arc": "dodgerblue", 
            "highlight_width_arc": 3,
            "icon_size": (40, 40) # Tamanho desejado para os ícones na roda (largura, altura)
        }

    def _get_project_root(self):
        """Retorna o diretório raiz do projeto (assumindo que Roda_Armas.py está em Arquivos)."""
        base_dir_script = os.path.dirname(os.path.abspath(__file__)) # .../Jogo/Arquivos
        project_root = os.path.dirname(base_dir_script) # .../Jogo
        return project_root

    def _load_tk_image(self, weapon_instance):
        """Carrega e redimensiona uma imagem para Tkinter, ou retorna None."""
        icon_path_attr = getattr(weapon_instance, 'ui_icon_path', None)
        if not icon_path_attr:
            # print(f"DEBUG(Roda_Armas): Arma '{weapon_instance.name}' não possui 'ui_icon_path'.")
            return None

        project_root = self._get_project_root()
        full_icon_path = os.path.join(project_root, icon_path_attr.replace("\\", os.sep))

        if not os.path.exists(full_icon_path):
            print(f"DEBUG(Roda_Armas): Ícone UI não encontrado para {weapon_instance.name}: {full_icon_path}")
            return None
        try:
            # Tenta usar Pillow se disponível para melhor suporte a formatos como PNG e redimensionamento
            from PIL import Image, ImageTk
            pil_image = Image.open(full_icon_path)
            pil_image = pil_image.resize(self.wheel_config["icon_size"], Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(pil_image)
            self._weapon_images_tk[weapon_instance.name + "_icon"] = img_tk # Cache
            return img_tk
        except ImportError: # Pillow não está instalada, tenta com tk.PhotoImage (limitado a GIF/PGM/PPM)
            try:
                img_tk = PhotoImage(file=full_icon_path)
                # PhotoImage não tem redimensionamento fácil como Pillow.
                # Para redimensionar, use subamostra (pode perder qualidade ou não ser preciso)
                # Ex: img_tk = img_tk.subsample(original_width // target_width, original_height // target_height)
                # É melhor preparar as imagens no tamanho correto se não usar Pillow.
                self._weapon_images_tk[weapon_instance.name + "_icon"] = img_tk
                return img_tk
            except tk.TclError as e_tk:
                print(f"DEBUG(Roda_Armas): Erro Tcl/Tk ao carregar (provavelmente formato não suportado sem Pillow?) '{full_icon_path}': {e_tk}")
                return None
        except Exception as e:
            print(f"DEBUG(Roda_Armas): Erro geral ao carregar imagem '{full_icon_path}': {e}")
            return None


    def create_wheel_window(self):
        if self.tk_root is None or not self.tk_root.winfo_exists():
            self.tk_root = tk.Tk()
            self.tk_root.withdraw() 

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = tk.Toplevel(self.tk_root)
            self.toplevel_window.title("Seleção de Arma")
            
            w = self.wheel_config["width"]
            h = self.wheel_config["height"]
            self.toplevel_window.geometry(f"{w}x{h}")
            self.toplevel_window.resizable(False, False)
            
            self.toplevel_window.attributes("-topmost", True)  
            self.toplevel_window.overrideredirect(True)   

            screen_width = self.toplevel_window.winfo_screenwidth()
            screen_height = self.toplevel_window.winfo_screenheight()
            x_pos = (screen_width // 2) - (w // 2)
            y_pos = (screen_height // 2) - (h // 2)
            self.toplevel_window.geometry(f"+{x_pos}+{y_pos}") 

            self.canvas = tk.Canvas(self.toplevel_window, width=w, height=h, 
                                    bg=self.wheel_config["bg_color"], 
                                    highlightbackground=self.wheel_config["border_color"], 
                                    highlightthickness=self.wheel_config["border_thickness"])
            self.canvas.pack(fill="both", expand=True)

            self.weapon_var = tk.StringVar()
            self.weapon_var.set("Selecione uma Arma")
            self.weapon_lbl = tk.Label(self.canvas, textvariable=self.weapon_var, 
                                       bg=self.wheel_config["label_bg"], fg=self.wheel_config["label_fg"],
                                       font=self.wheel_config["label_font"])
            self.canvas.create_window(w // 2, 30, window=self.weapon_lbl)

            self.out_circle_coords = (w*0.15, h*0.15, w*0.85, h*0.85) 
            self.canvas.create_oval(*self.out_circle_coords, tags="out_circle", 
                                    outline=self.wheel_config["arc_outline"], 
                                    width=self.wheel_config["arc_width"] +1) 

            self.canvas.bind("<Button-1>", self.on_canvas_click)
            self.toplevel_window.bind("<Escape>", self.hide_wheel) 
        
        self._redraw_wheel_content()


    def _redraw_wheel_content(self):
        if not self.canvas or not self.toplevel_window.winfo_exists():
            return

        self.canvas.delete("weapon_arc") 
        self.canvas.delete("weapon_image_tk") 
        self.canvas.delete("weapon_text") 
        self._weapon_images_tk.clear() 

        self._draw_weapon_arcs_and_images()
        self.canvas.update_idletasks()

    def _draw_weapon_arcs_and_images(self):
        w, h = self.wheel_config["width"], self.wheel_config["height"]
        ox0, oy0, ox1, oy1 = self.out_circle_coords
        
        num_weapons = len(self.player_weapons_ref)
        if num_weapons == 0:
            self.canvas.create_text(w // 2, h // 2, text="Nenhuma arma equipável.", 
                                    fill=self.wheel_config["item_text_color"], 
                                    font=self.wheel_config["item_font"], tags="weapon_text")
            return

        angle_step = 360 / num_weapons
        current_angle = 90 - (angle_step / 2) 

        center_x, center_y = w // 2, h // 2
        radius = (ox1 - ox0) / 2.0
        icon_display_radius = radius * 0.7 

        for i, weapon_instance in enumerate(self.player_weapons_ref):
            if not isinstance(weapon_instance, Weapon): continue

            weapon_tag = getattr(weapon_instance, 'tag', f"weapon_{weapon_instance.name.replace(' ', '_').lower()}_{i}")
            if not hasattr(weapon_instance, 'tag'):
                weapon_instance.tag = weapon_tag
            
            fill_color = getattr(weapon_instance, 'fill_color', "gray") 

            arc_id = self.canvas.create_arc(ox0, oy0, ox1, oy1,
                                            start=current_angle, extent=angle_step,
                                            fill="", outline=self.wheel_config["arc_outline"], 
                                            width=self.wheel_config["arc_width"],
                                            tags=(weapon_tag, "weapon_arc", f"arc_for_{weapon_instance.name.replace(' ','_')}"))

            mid_angle_rad = math.radians(current_angle + angle_step / 2)
            item_x = center_x + icon_display_radius * math.cos(mid_angle_rad)
            item_y = center_y - icon_display_radius * math.sin(mid_angle_rad) 

            tk_img = self._load_tk_image(weapon_instance)
            element_tag_suffix = "_img" if tk_img else "_text"
            full_element_tag = weapon_tag + element_tag_suffix

            if tk_img:
                self.canvas.create_image(item_x, item_y, image=tk_img, tags=(full_element_tag, weapon_tag, "weapon_image_tk"))
            else:
                self.canvas.create_text(item_x, item_y, text=weapon_instance.name[:12], 
                                        fill=self.wheel_config["item_text_color"], 
                                        font=self.wheel_config["item_font"], 
                                        tags=(full_element_tag, weapon_tag, "weapon_text"))

            for tag_to_bind in [arc_id, full_element_tag]:
                self.canvas.tag_bind(tag_to_bind, "<Enter>", lambda e, wt=weapon_tag, wn=weapon_instance.name: self.highlight_item(wt, wn))
                self.canvas.tag_bind(tag_to_bind, "<Leave>", lambda e, wt=weapon_tag: self.unhighlight_item(wt))
                self.canvas.tag_bind(tag_to_bind, "<Button-1>", lambda e, wp=weapon_instance: self.update_weapon(wp))

            current_angle += angle_step

    def highlight_item(self, tag_prefix, weapon_name):
        self.canvas.itemconfigure(tag_prefix, fill=self.wheel_config["highlight_color_arc"], width=self.wheel_config["highlight_width_arc"])
        self.canvas.itemconfigure("out_circle", outline=self.wheel_config["highlight_color_arc"])
        self.weapon_var.set(f"Selecionar: {weapon_name}")

    def unhighlight_item(self, tag_prefix):
        self.canvas.itemconfigure(tag_prefix, fill="", width=self.wheel_config["arc_width"])
        self.canvas.itemconfigure("out_circle", outline=self.wheel_config["arc_outline"])
        self.weapon_var.set("Selecione uma Arma")

    def update_weapon(self, weapon_instance: Weapon): # type: ignore
        if not isinstance(weapon_instance, Weapon): return
        
        self.cur_weapon_instance = weapon_instance 
        self.weapon_var.set("Equipada: " + weapon_instance.name)
        
        if self.on_weapon_selected_callback:
            self.on_weapon_selected_callback(self.cur_weapon_instance) 

        self.hide_wheel() 

    def on_canvas_click(self, event):
        item_id = self.canvas.find_closest(event.x, event.y)
        if item_id:
            tags = self.canvas.gettags(item_id[0])
            is_on_weapon_element = any(tag.startswith("weapon_") or tag == "weapon_arc" or tag == "weapon_image_tk" or tag == "weapon_text" for tag in tags)
            if not is_on_weapon_element:
                self.hide_wheel()
        else: 
             self.hide_wheel()

    def show_wheel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.create_wheel_window() 
        else:
             self._redraw_wheel_content() 

        self.toplevel_window.deiconify() 
        self.toplevel_window.grab_set()  
        self.toplevel_window.focus_force() 

    def hide_wheel(self, event=None): 
        if self.toplevel_window and self.toplevel_window.winfo_exists():
            self.toplevel_window.grab_release() 
            self.toplevel_window.withdraw() 
        
        if self.active_event_ref: 
            self.active_event_ref.clear() 

    def process_events(self): 
        if self.tk_root and self.tk_root.winfo_exists():
            self.tk_root.update_idletasks()
            self.tk_root.update()

    def refresh_weapon_list(self):
        if self.canvas and self.toplevel_window and self.toplevel_window.winfo_exists() and self.toplevel_window.winfo_viewable():
            self._redraw_wheel_content()
