import tkinter as tk
from tkinter import messagebox

intentos = 0


def validar_numero_menor_10(numero):
    return numero < 10


def registrar_intento():
    global intentos
    try:
        numero = int(entry_numero.get())
        intentos += 1

        if validar_numero_menor_10(numero):
            lbl_resultado.config(
                text=(
                    f"Número correcto ingresado: {numero}\n"
                    f"Intentos realizados: {intentos}"
                )
            )
            entry_numero.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Número válido ingresado.")
        else:
            lbl_resultado.config(text="Número incorrecto. Debe ser menor que 10.")
            messagebox.showerror("Error", "El número debe ser menor que 10. Intente nuevamente.")
            entry_numero.delete(0, tk.END)
    except ValueError:
        intentos += 1
        lbl_resultado.config(text="Error: ingrese un número entero válido.")
        messagebox.showerror("Error", "Debe ingresar un número entero válido.")
        entry_numero.delete(0, tk.END)


def abrir():
    global entry_numero, lbl_resultado, intentos
    intentos = 0

    ventana = tk.Tk()
    ventana.title("Validación de Números Menores a 10")
    ventana.geometry("520x300")
    ventana.resizable(False, False)

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)

    tk.Label(ventana, text="Ingresar úmero Entero", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
    tk.Label(ventana, text="Ingrese un número menor que 10:").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_numero = tk.Entry(ventana)
    entry_numero.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Button(ventana, text="Verificar", width=20, command=registrar_intento).grid(row=2, column=0, columnspan=2, pady=10)

    lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 12))
    lbl_resultado.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(ventana, text="Volver", width=18, command=lambda: [ventana.destroy(), __import__('ventana').abrir()]).grid(row=4, column=0, columnspan=2, pady=15)

    ventana.mainloop()
