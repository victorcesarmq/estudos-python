import tkinter as tk
from tkinter import messagebox
import pyautogui
import easyocr
import numpy as np
import cv2
from PIL import Image, ImageTk
import threading
from pynput import keyboard
import pyperclip  # Biblioteca para lidar com o Ctrl+C
import time


# Inicializa o motor de leitura
print("Carregando IA (EasyOCR)... Aguarde.")
reader = easyocr.Reader(['en'])




class PlateClipper:
   def __init__(self, root):
       self.root = root
       self.root.title("Plate Clipper RGB")
       self.root.geometry("400x500")
       self.root.attributes("-topmost", True)
       self.root.configure(bg="#121212")


       # --- UI ---
       tk.Label(root, text="PLATE CLIPPER", font=("Impact", 18), bg="#121212", fg="#00FF00").pack(pady=10)


       self.info_label = tk.Label(
           root,
           text="Pressione ALT + Q para capturar\nA placa será copiada (Ctrl+C) automaticamente",
           font=("Arial", 9), bg="#121212", fg="#aaaaaa"
       )
       self.info_label.pack(pady=5)


       # Visualização da última captura
       self.canvas_img = tk.Label(root, bg="#000", width=350, height=150)
       self.canvas_img.pack(pady=15)


       # Label da última placa detectada
       self.placa_var = tk.StringVar(value="AGUARDANDO...")
       self.placa_label = tk.Label(
           root, textvariable=self.placa_var,
           font=("Arial Black", 24), bg="#1e1e1e", fg="#00FF00",
           relief="flat", padx=10, pady=10
       )
       self.placa_label.pack(pady=10, fill="x", padx=40)


       self.status_var = tk.StringVar(value="Status: Pronto")
       tk.Label(root, textvariable=self.status_var, bg="#121212", fg="gray").pack(side="bottom", pady=10)


       # Listener de Teclado
       self.hotkey = keyboard.GlobalHotKeys({'<alt>+q': self.disparar_selecao})
       self.hotkey.start()


   def disparar_selecao(self):
       # Chama a interface de seleção em uma thread separada
       threading.Thread(target=self.abrir_seletor, daemon=True).start()


   def abrir_seletor(self):
       # Janela de seleção (Snipping Tool)
       selector = tk.Toplevel()
       selector.attributes("-fullscreen", True, "-alpha", 0.3, "-topmost", True)
       selector.config(cursor="cross")


       canvas = tk.Canvas(selector, bg="grey", cursor="cross")
       canvas.pack(fill="both", expand=True)


       def on_button_down(event):
           self.start_x, self.start_y = event.x, event.y
           self.rect = canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='cyan', width=2)


       def on_move(event):
           canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)


       def on_button_up(event):
           x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
           x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
           largura, altura = x2 - x1, y2 - y1


           selector.destroy()
           if largura > 10 and altura > 10:
               self.processar_captura((x1, y1, largura, altura))


       canvas.bind("<ButtonPress-1>", on_button_down)
       canvas.bind("<B1-Motion>", on_move)
       canvas.bind("<ButtonRelease-1>", on_button_up)


   def processar_captura(self, coords):
       self.status_var.set("Status: Lendo placa...")


       # 1. Screenshot da área
       screenshot = pyautogui.screenshot(region=coords)
       frame = np.array(screenshot)
       img_cv = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


       # 2. OCR
       results = reader.readtext(img_cv)


       if results:
           # Pega o texto da detecção com maior probabilidade
           texto_bruto = results[0][1]
           # Limpeza básica (letras e números apenas)
           placa = texto_bruto.upper().replace(" ", "").replace("-", "").strip()


           # 3. Copiar para o Clipboard (Área de Transferência)
           pyperclip.copy(placa)


           # 4. Atualizar UI
           self.placa_var.set(placa)
           self.status_var.set("Status: COPIADO!")


           # Mostrar imagem na UI
           screenshot.thumbnail((350, 150))
           img_tk = ImageTk.PhotoImage(screenshot)
           self.canvas_img.config(image=img_tk)
           self.canvas_img.image = img_tk
       else:
           self.status_var.set("Status: Erro na leitura")
           self.placa_var.set("NÃO LIDO")




if __name__ == "__main__":
   root = tk.Tk()
   app = PlateClipper(root)
   root.mainloop()

