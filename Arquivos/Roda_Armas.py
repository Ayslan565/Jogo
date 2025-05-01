from tkinter import *
from PIL import Image, ImageTk  # Usado para redimensionar imagens

class Aplicacao(Tk):
    def __init__(self):
        super().__init__()
        self.title("Roda de Armas")
        self.roda_de_armas = RodaDeArmas(self)
        self.roda_de_armas.pack()

class RodaDeArmas(Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=500, height=500)
        
        self.armas = [
            Espada(),
        ]
        self.arma_atual = None

        # Dimensões do canvas
        largura = self.winfo_reqwidth()
        altura = self.winfo_reqheight()

        # Rótulo da arma
        self.arma_var = StringVar()
        self.arma_var.set("Arma:")
        self.rotulo_arma = Label(self, textvariable=self.arma_var)
        self.create_window(largura // 2, altura // 4 - 25, window=self.rotulo_arma)

        # Círculo externo
        circulo_x = largura // 4
        circulo_y = altura // 4
        circulo_x1 = largura - circulo_x
        circulo_y1 = altura - circulo_y
        self.circulo_externo = self.create_oval(circulo_x, circulo_y, circulo_x1, circulo_y1, tags="circulo_externo", width=2)

        # Armas na roda
        if len(self.armas) == 1:
            arma = self.armas[0]
            self.create_image(largura // 2, altura // 2, image=arma.imagem, tags=arma.tag + "_img")
            self.tag_bind(arma.tag + "_img", "<Enter>", lambda e: self.preencher_item(e, "circulo_externo", arma.cor))
            self.tag_bind(arma.tag + "_img", "<Button-1>", lambda e, arma=arma: self.atualizar_arma(e, arma))

            self.tag_bind("circulo_externo", "<Enter>", lambda e: self.preencher_item(e, "circulo_externo", arma.cor))
            self.tag_bind("circulo_externo", "<Leave>", lambda e: self.preencher_item(e, "circulo_externo", ""))
            self.tag_bind("circulo_externo", "<Button-1>", lambda e, arma=arma: self.atualizar_arma(e, arma))

    def preencher_item(self, evento, tag, cor):
        self.itemconfigure(tag, fill=cor)
        self.update()

    def atualizar_arma(self, evento, arma):
        self.arma_atual = arma
        self.arma_var.set("Arma: " + arma.nome)
        self.itemconfigure("circulo_externo", fill=arma.cor)

class Arma:
    def __init__(self):
        self.nome = "Arma"
        self.imagem = None
        self.cor = "cinza"
        self.tag = "arma"

class Espada(Arma):
    def __init__(self):
        super().__init__()
        self.nome = "Espada"

        # Carrega e redimensiona a imagem
        caminho_imagem = "Sprites/Armas/Espada.png"
        imagem_pil = Image.open(caminho_imagem).resize((200, 200))
        self.imagem = ImageTk.PhotoImage(imagem_pil)

        self.cor = "red"
        self.tag = "espada"

if __name__ == "__main__":
    app = Aplicacao()
    app.mainloop()
