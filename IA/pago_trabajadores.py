import tkinter as tk
from tkinter import messagebox


def calcular_pago_normales(horas_normales, pago_hora):
    return horas_normales * pago_hora


def calcular_pago_extras(horas_extras, pago_hora):
    pago_extra_por_hora = pago_hora * 1.5
    return horas_extras * pago_extra_por_hora


def validar_entero(texto):
    try:
        int(texto)
        return True
    except ValueError:
        return False


def validar_nombre(nombre):
    return bool(nombre.strip()) and all(c.isalpha() or c.isspace() for c in nombre)


def registrar_trabajador():
    nombre = entry_nombre.get().strip()
    horas_normales_texto = entry_horas_normales.get().strip()
    pago_hora_texto = entry_pago_hora.get().strip()
    horas_extras_texto = entry_horas_extras.get().strip()
    hijos_texto = entry_hijos.get().strip()

    if not validar_nombre(nombre):
        messagebox.showerror("Error", "Ingrese un nombre valido (solo letras y espacios).")
        return

    if not (validar_entero(horas_normales_texto) and validar_entero(pago_hora_texto) and validar_entero(horas_extras_texto) and validar_entero(hijos_texto)):
        messagebox.showerror("Error", "Todos los valores numericos deben ser enteros.")
        return

    horas_normales = int(horas_normales_texto)
    pago_hora = int(pago_hora_texto)
    horas_extras = int(horas_extras_texto)
    hijos = int(hijos_texto)

    if horas_normales < 0 or pago_hora < 0 or horas_extras < 0 or hijos < 0:
        messagebox.showerror("Error", "Los valores numericos no pueden ser negativos.")
        return

    pago_normales = calcular_pago_normales(horas_normales, pago_hora)
    pago_extras = calcular_pago_extras(horas_extras, pago_hora)
    bonificacion_hijos = hijos * 0.5
    pago_total = pago_normales + pago_extras + bonificacion_hijos

    lbl_resultado.config(
        text=(
            f"Pago por horas normales: S/ {pago_normales:.2f}\n"
            f"Pago por horas extras: S/ {pago_extras:.2f}\n"
            f"Bonificacion por hijos: S/ {bonificacion_hijos:.2f}\n"
            f"Pago total: S/ {pago_total:.2f}"
        )
    )

    entry_nombre.delete(0, tk.END)
    entry_horas_normales.delete(0, tk.END)
    entry_pago_hora.delete(0, tk.END)
    entry_horas_extras.delete(0, tk.END)
    entry_hijos.delete(0, tk.END)

    messagebox.showinfo("Exito", "Calculo de pago realizado correctamente.")


def abrir():
    global entry_nombre, entry_horas_normales, entry_pago_hora, entry_horas_extras, entry_hijos, lbl_resultado

    ventana = tk.Tk()
    ventana.title("Pago de Trabajadores")
    ventana.geometry("560x420")
    ventana.resizable(False, False)

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)

    tk.Label(ventana, text="Calculo de Pago de Trabajadores", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

    tk.Label(ventana, text="Nombre del trabajador:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(ventana, text="Horas normales trabajadas:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_horas_normales = tk.Entry(ventana)
    entry_horas_normales.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(ventana, text="Pago por hora normal:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_pago_hora = tk.Entry(ventana)
    entry_pago_hora.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    tk.Label(ventana, text="Horas extras trabajadas:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_horas_extras = tk.Entry(ventana)
    entry_horas_extras.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    tk.Label(ventana, text="Numero de hijos:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    entry_hijos = tk.Entry(ventana)
    entry_hijos.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    tk.Button(ventana, text="Calcular Pago", width=20, command=registrar_trabajador).grid(row=6, column=0, columnspan=2, pady=15)

    lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 12), justify="left")
    lbl_resultado.grid(row=7, column=0, columnspan=2, pady=10)

    tk.Button(ventana, text="Volver", width=18, command=lambda: [ventana.destroy(), __import__('ventana').abrir()]).grid(row=8, column=0, columnspan=2, pady=15)

    ventana.mainloop()
