from tkinter import *

class Root(Tk):
	def __init__(self):
		super().__init__()
		
		self.title("Weapon Wheel")
		
		self.weapon_wheel = WeaponWheel(self)
		
class WeaponWheel(Canvas):
	def __init__(self, parent):
		super().__init__(parent, width=500, height=500)
		
		self.weapons = [
			Sword(),
		]
		
		self.cur_weapon = None
		
		#Canvas Dimensions
		can_w = self.winfo_reqwidth()
		can_h = self.winfo_reqheight()
		
		#Weapon Label
		self.weapon_var = StringVar()
		self.weapon_var.set("Weapon:")
		
		self.weapon_lbl = Label(self, textvariable=self.weapon_var)
		self.create_window(can_w // 2, can_h // 4 - 25, window=self.weapon_lbl)
		
		#Outer Circle
		out_circle_x = can_w // 4
		out_circle_y = can_h // 4
		
		out_circle_x1 = can_w - out_circle_x
		out_circle_y1 = can_h - out_circle_y
		
		self.out_circle = self.create_oval(out_circle_x, out_circle_y, out_circle_x1, out_circle_y1, tags="out_circle", width=2)
		
		#Weapon Arcs
		if len(self.weapons) == 1:
			weapon = self.weapons[0]
			
			self.create_image(can_w // 2, can_h // 2, image=weapon.img, tags=weapon.tag + "_img")
			self.tag_bind(weapon.tag + "_img", "<Enter>", lambda e: self.fill_item(e, "out_circle", weapon.fill_color))
			self.tag_bind(weapon.tag + "_img", "<Button-1>", lambda e, weapon=weapon: self.update_weapon(e, weapon))
			
			self.tag_bind(self.out_circle, "<Enter>", lambda e: self.fill_item(e, "out_circle", weapon.fill_color))
			self.tag_bind(self.out_circle, "<Leave>", lambda e: self.fill_item(e, "out_circle", ""))
			self.tag_bind(self.out_circle, "<Button-1>", lambda e, weapon=weapon: self.update_weapon(e, weapon))
		
		self.pack()
		
	def fill_item(self, e, tag, color):
		self.itemconfigure(tag, fill=color)
		
		self.update()
		
	def update_weapon(self, e, weapon):
		self.cur_weapon = weapon
		
		self.weapon_var.set("Weapon: " + weapon.name)
		
		self.itemconfigure(weapon.tag, fill=weapon.fill_color)
		
class Weapon:
	def __init__(self):
		self.name = "Weapon"
		
		self.img = None
		
		self.fill_color = "gray"
		
		self.tag = "weapon"
		
class Sword(Weapon):
	def __init__(self):
		super().__init__()
		
		self.name = "Sword"
		
		self.img = PhotoImage(file="Sword 50x50.png")
		
		self.fill_color = "red"
		
		self.tag = "sword"
		
if __name__ == "__main__":
	root = Root()
	
	root.mainloop()