import tkinter as tk
from tkinter import font
import aumento_sueldo
import pagos_feria
import descuentos_tienda
import numero_menor_10
import numero_rango
import suma_enteros
import suma_acumulativa
import suma_limite
import pago_trabajadores

def abrir():
    ventana = tk.Tk()
    ventana.geometry("1000x400")
    
    titulo_font = font.Font(family="Helvetica", size=16, weight="bold")
    
    tk.Label(ventana, text="Pagina principal", font=titulo_font).grid(row=0, column=0, columnspan=5, padx=50, pady=30)
    
    tk.Button(ventana, text="Sistema de aumento de sueldo", bg="gray", fg="white", command=lambda: [ventana.destroy(), aumento_sueldo.abrir()]).grid(row=1, column=0, padx=10, pady=15)
    tk.Button(ventana, text="Sistema de pagos en una feria", bg="gray", fg="white", command=lambda: [ventana.destroy(), pagos_feria.abrir()]).grid(row=1, column=1, padx=10, pady=15)
    tk.Button(ventana, text="Descuentos mensuales en una tienda", bg="gray", fg="white", command=lambda: [ventana.destroy(), descuentos_tienda.abrir()]).grid(row=1, column=2, padx=10, pady=15)
    tk.Button(ventana, text="Validacion de numeros menores a 10", bg="gray", fg="white", command=lambda: [ventana.destroy(), numero_menor_10.abrir()]).grid(row=1, column=3, padx=10, pady=15)
    tk.Button(ventana, text="Validacion de numeros en un rango", bg="gray", fg="white", command=lambda: [ventana.destroy(), numero_rango.abrir()]).grid(row=1, column=4, padx=10, pady=15)
    tk.Button(ventana, text="Suma de numeros enteros", bg="gray", fg="white", command=lambda: [ventana.destroy(), suma_enteros.abrir()]).grid(row=2, column=1, padx=10, pady=15)
    tk.Button(ventana, text="Suma acumulativa", bg="gray", fg="white", command=lambda: [ventana.destroy(), suma_acumulativa.abrir()]).grid(row=2, column=2, padx=10, pady=15)
    tk.Button(ventana, text="Suma de numeros hasta superar un limite", bg="gray", fg="white", command=lambda: [ventana.destroy(), suma_limite.abrir()]).grid(row=2, column=3, padx=10, pady=15)
    tk.Button(ventana, text="Pago de Trabajadores", bg="gray", fg="white", command=lambda: [ventana.destroy(), pago_trabajadores.abrir()]).grid(row=2, column=4, padx=10, pady=15)

    
    tk.Button(ventana, text="Salir", command=ventana.destroy).grid(row=3, column=0, columnspan=5, padx=10, pady=20)
    
    ventana.mainloop()