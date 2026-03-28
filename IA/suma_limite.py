import tkinter as tk
from tkinter import messagebox

numeros = []
suma_actual = 0


def es_entero_valido(texto):
    try:
        int(texto)
        return True
    except ValueError:
        return False


def registrar_numero():
    global suma_actual
    texto = entry_numero.get().strip()

    if not es_entero_valido(texto):
        messagebox.showerror("Error", "Ingrese un numero entero valido.")
        lbl_resultado.config(text="Numero invalido. Ingrese un entero.")
        entry_numero.delete(0, tk.END)
        return

    numero = int(texto)
    numeros.append(numero)
    suma_actual += numero
    entry_numero.delete(0, tk.END)

    if suma_actual > 100:
        mensaje = (
            f"Suma final: {suma_actual}\n"
            f"Cantidad de numeros ingresados: {len(numeros)}\n"
            f"Lista de numeros: {', '.join(str(x) for x in numeros)}"
        )
        lbl_resultado.config(text=mensaje)
        messagebox.showinfo("Proceso detenido", "La suma supero 100. Proceso finalizado.")
        entry_numero.config(state="disabled")
        btn_registrar.config(state="disabled")
        return

    lbl_resultado.config(
        text=(
            f"Numeros ingresados: {', '.join(str(x) for x in numeros)}\n"
            f"Suma parcial: {suma_actual}"
        )
    )


def abrir():
    global entry_numero, lbl_resultado, btn_registrar, numeros, suma_actual
    numeros = []
    suma_actual = 0

    ventana = tk.Tk()
    ventana.title("Suma con Limite")
    ventana.geometry("520x380")
    ventana.resizable(False, False)

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)

    tk.Label(ventana, text="Suma de Numeros Enteros", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
    tk.Label(ventana, text="Ingrese numeros enteros. El proceso se detiene cuando la suma supere 100:").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_numero = tk.Entry(ventana)
    entry_numero.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    btn_registrar = tk.Button(ventana, text="Agregar", width=20, command=registrar_numero)
    btn_registrar.grid(row=2, column=0, columnspan=2, pady=10)

    lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 12), justify="left")
    lbl_resultado.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(ventana, text="Volver", width=18, command=lambda: [ventana.destroy(), __import__('ventana').abrir()]).grid(row=4, column=0, columnspan=2, pady=15)

    ventana.mainloop()
