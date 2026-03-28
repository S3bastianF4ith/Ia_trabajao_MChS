import tkinter as tk
from tkinter import messagebox


def validar_positivo(numero):
    return numero > 0


def calcular_suma_y_secuencia(n):
    secuencia = list(range(1, n + 1))
    total = sum(secuencia)
    return total, secuencia


def registrar_suma():
    try:
        n = int(entry_n.get())
        if not validar_positivo(n):
            messagebox.showerror("Error", "Ingrese un numero positivo mayor que 0.")
            lbl_resultado.config(text="Numero invalido. Debe ser positivo.")
            return

        total, secuencia = calcular_suma_y_secuencia(n)
        texto_secuencia = ' + '.join(str(x) for x in secuencia)

        lbl_resultado.config(
            text=(
                f"Secuencia: {texto_secuencia}\n"
                f"Resultado final: {total}"
            )
        )
        entry_n.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Debe ingresar un numero entero valido.")
        lbl_resultado.config(text="Numero invalido. Ingrese un entero positivo.")
        entry_n.delete(0, tk.END)


def abrir():
    global entry_n, lbl_resultado

    ventana = tk.Tk()
    ventana.title("Suma de Numeros Enteros")
    ventana.geometry("520x360")
    ventana.resizable(False, False)

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)

    tk.Label(ventana, text="Suma de los primeros n enteros", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
    tk.Label(ventana, text="Ingrese un numero positivo n:").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_n = tk.Entry(ventana)
    entry_n.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Button(ventana, text="Calcular", width=20, command=registrar_suma).grid(row=2, column=0, columnspan=2, pady=10)

    lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 12), justify="left")
    lbl_resultado.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(ventana, text="Volver", width=18, command=lambda: [ventana.destroy(), __import__('ventana').abrir()]).grid(row=4, column=0, columnspan=2, pady=15)

    ventana.mainloop()
