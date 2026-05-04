import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter.messagebox as messagebox

# Configurar apariencia
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Funciones Lineales")
        self.geometry("600x500")
        
        # Etiquetas y entradas para m y b
        self.label_m = ctk.CTkLabel(self, text="Pendiente m:")
        self.label_m.pack(pady=10)
        self.entry_m = ctk.CTkEntry(self)
        self.entry_m.pack()
        
        self.label_b = ctk.CTkLabel(self, text="Término independiente b:")
        self.label_b.pack(pady=10)
        self.entry_b = ctk.CTkEntry(self)
        self.entry_b.pack()
        
        # Botón para graficar
        self.button = ctk.CTkButton(self, text="Graficar", command=self.plot)
        self.button.pack(pady=20)
        
        # coso para el gráfico
        self.figure = plt.Figure(figsize=(5,4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack()
    
    def plot(self):
        try:
            m = float(self.entry_m.get())
            b = float(self.entry_b.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos para m y b")
            return
        
        # Limpiar grafico anterior
        self.ax.clear()
        
        # Generar datos
        x = np.linspace(-10, 10, 100)
        y = m * x + b
        
        # Graficar
        self.ax.plot(x, y)
        self.ax.set_title(f"f(x) = {m}x + {b}")
        self.ax.grid(True)
        self.canvas.draw()

if __name__ == "__main__":
    app = App()
    app.mainloop()