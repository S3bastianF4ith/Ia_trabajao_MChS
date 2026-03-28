import tkinter as tk
from tkinter import messagebox

intentos = 0
errores = 0
historial_intentos = []


def validar_rango(numero, minimo=0, maximo=20):
    return minimo < numero < maximo


def registrar_intento():
    global intentos, errores, historial_intentos
    intento_texto = entry_numero.get().strip()
    intentos += 1

    try:
        numero = int(intento_texto)
        valido = validar_rango(numero)

        historial_intentos.append({
            'valor': numero,
            'valido': valido
        })

        if valido:
            lbl_resultado.config(
                text=(
                    f"Numero valido ingresado: {numero}\n"
                    f"Intentos realizados: {intentos}\n"
                    f"Intentos incorrectos: {errores}"
                )
            )
            entry_numero.delete(0, tk.END)
            messagebox.showinfo("Exito", "Numero valido dentro del rango.")
        else:
            errores += 1
            lbl_resultado.config(
                text=(
                    "Numero fuera del rango. Debe estar entre 0 y 20.\n"
                    f"Intentos realizados: {intentos}\n"
                    f"Intentos incorrectos: {errores}"
                )
            )
            entry_numero.delete(0, tk.END)
            messagebox.showerror("Error", "El numero debe estar entre 0 y 20. Intente nuevamente.")
    except ValueError:
        errores += 1
        historial_intentos.append({
            'valor': intento_texto,
            'valido': False,
            'error': 'no entero'
        })
        lbl_resultado.config(
            text=(
                "Error: ingrese un numero entero valido.\n"
                f"Intentos realizados: {intentos}\n"
                f"Intentos incorrectos: {errores}"
            )
        )
        entry_numero.delete(0, tk.END)
        messagebox.showerror("Error", "Debe ingresar un numero entero valido.")


def mostrar_historial():
    historial_ventana = tk.Toplevel()
    historial_ventana.title("Historial de Intentos")
    historial_ventana.geometry("600x400")
    historial_ventana.resizable(False, False)

    tk.Label(historial_ventana, text="Historial de Intentos", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    if not historial_intentos:
        tk.Label(historial_ventana, text="No hay intentos registrados.").grid(row=1, column=0, columnspan=2, pady=5)
    else:
        for i, intento in enumerate(historial_intentos, start=1):
            estado = "Valido" if intento['valido'] else "Incorrecto"
            valor = intento['valor']
            detalle = f"{i}. Valor: {valor} - {estado}"
            tk.Label(historial_ventana, text=detalle).grid(row=i, column=0, columnspan=2, sticky="w", padx=20)

    tk.Button(historial_ventana, text="Cerrar", command=historial_ventana.destroy).grid(row=len(historial_intentos)+1, column=0, columnspan=2, pady=10)


def abrir():
    global entry_numero, lbl_resultado, intentos, errores, historial_intentos
    intentos = 0
    errores = 0
    historial_intentos = []

    ventana = tk.Tk()
    ventana.title("Validacion de Numeros en Rango")
    ventana.geometry("520x380")
    ventana.resizable(False, False)

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)

    tk.Label(ventana, text="Validacion de Numero en Rango", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
    tk.Label(ventana, text="Ingrese un numero entero entre 0 y 20:").grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_numero = tk.Entry(ventana)
    entry_numero.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Button(ventana, text="Verificar", width=20, command=registrar_intento).grid(row=2, column=0, columnspan=2, pady=10)
    tk.Button(ventana, text="Ver historial", width=20, command=mostrar_historial).grid(row=3, column=0, columnspan=2, pady=5)

    lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 12))
    lbl_resultado.grid(row=4, column=0, columnspan=2, pady=10)

    tk.Button(ventana, text="Volver", width=18, command=lambda: [ventana.destroy(), __import__('ventana').abrir()]).grid(row=5, column=0, columnspan=2, pady=15)

    ventana.mainloop()
