import tkinter as tk
from tkinter import messagebox

visitantes = []

def calcular_precio(edad, cantidad_juegos):
    precio_base = cantidad_juegos * 50
    if edad < 10:
        descuento = precio_base * 0.25
    elif 10 <= edad <= 17:
        descuento = precio_base * 0.10
    else:
        descuento = 0
    total_pagar = precio_base - descuento
    return precio_base, descuento, total_pagar

def mostrar_total_recaudado():
    total_recaudado = sum(visitante['total_pagar'] for visitante in visitantes)
    messagebox.showinfo("Total Recaudado", f"El parque ha recaudado un total de S/ {total_recaudado:.2f}")

def registrar_visitante():
    try:
        nombre = entry_nombre.get().strip()
        edad = int(entry_edad.get())
        cantidad_juegos = int(entry_juegos.get())

        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return
        
        if not nombre.isalpha():
            messagebox.showerror("Error", "El nombre del visitante solo debe contener letras.")
            return

        if edad < 0:
            messagebox.showerror("Error", "La edad no puede ser negativa.")
            return

        if cantidad_juegos < 0:
            messagebox.showerror("Error", "La cantidad de juegos no puede ser negativa.")
            return

        precio_base, descuento, total_pagar = calcular_precio(edad, cantidad_juegos)

        lbl_resultado.config(text=f"Precio Base: S/ {precio_base:.2f}\nDescuento: S/ {descuento:.2f}\nTotal a Pagar: S/ {total_pagar:.2f}")

        visitantes.append({
            'nombre': nombre,
            'edad': edad,
            'cantidad_juegos': cantidad_juegos,
            'total_pagar': total_pagar
        })

        entry_nombre.delete(0, tk.END)
        entry_edad.delete(0, tk.END)
        entry_juegos.delete(0, tk.END)

        messagebox.showinfo("Éxito", "Visitante registrado correctamente.")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos (edad y cantidad de juegos deben ser números enteros).")

def abrir():
    global entry_nombre, entry_edad, entry_juegos, lbl_resultado

    ventana = tk.Tk()
    ventana.title("Sistema de Pagos en una Feria")
    ventana.geometry("500x500")
    ventana.resizable(False, False)

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)

    tk.Label(ventana, text="Registro de Visitante", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

    tk.Label(ventana, text="Cada juego cuesta 50 Soles.", font=("Helvetica", 10)).grid(row=1, column=0, columnspan=2, pady=5)
    tk.Label(ventana, text="Descuentos: Menores de 10 años descuento del 25%, 10-17 años descuento del 10%, Adultos descuento del 0%", font=("Helvetica", 10)).grid(row=2, column=0, columnspan=2, pady=5)

    tk.Label(ventana, text="Nombre del Visitante:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    tk.Label(ventana, text="Edad:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_edad = tk.Entry(ventana)
    entry_edad.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    tk.Label(ventana, text="Cantidad de Juegos Utilizados:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    entry_juegos = tk.Entry(ventana)
    entry_juegos.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    tk.Button(ventana, text="Calcular y Registrar", width=20, command=registrar_visitante).grid(row=6, column=0, columnspan=2, pady=10)

    lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 12))
    lbl_resultado.grid(row=7, column=0, columnspan=2, pady=10)

    tk.Button(ventana, text="Total Recaudado", width=15, command=mostrar_total_recaudado).grid(row=8, column=0, pady=5)
    tk.Button(ventana, text="Volver", width=15, command=lambda: [ventana.destroy(), __import__('ventana').abrir()]).grid(row=8, column=1, pady=5)

    ventana.mainloop()
