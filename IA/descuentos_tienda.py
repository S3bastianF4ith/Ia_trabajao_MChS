import tkinter as tk
from tkinter import messagebox

compras = []

MESES_VALIDOS = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]

PROMOCIONES = {
    "octubre": 0.15,
    "diciembre": 0.20,
    "julio": 0.10
}


def validar_mes(mes):
    if not isinstance(mes, str):
        return False
    return mes.strip().lower() in MESES_VALIDOS


def calcular_descuento(mes, importe):
    mes_normalizado = mes.strip().lower()
    porcentaje = PROMOCIONES.get(mes_normalizado, 0)
    return importe * porcentaje


def calcular_total_final(importe, descuento):
    return importe - descuento


def total_vendido():
    return sum(compra['total_final'] for compra in compras)


def mostrar_historial():
    historial_ventana = tk.Toplevel()
    historial_ventana.title("Historial de Compras")
    historial_ventana.geometry("600x400")

    tk.Label(historial_ventana, text="Compras Registradas", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    if not compras:
        tk.Label(historial_ventana, text="No hay compras registradas.").grid(row=1, column=0, columnspan=2)
    else:
        for i, compra in enumerate(compras, start=1):
            info = (
                f"{i}. Cliente: {compra['nombre']}, Mes: {compra['mes'].title()}, "
                f"Importe: S/ {compra['importe']:.2f}, Descuento: S/ {compra['descuento']:.2f}, "
                f"Total: S/ {compra['total_final']:.2f}"
            )
            tk.Label(historial_ventana, text=info).grid(row=i, column=0, columnspan=2, sticky="w", padx=20)

    tk.Button(historial_ventana, text="Cerrar", command=historial_ventana.destroy).grid(row=len(compras)+1, column=0, columnspan=2, pady=10)


def mostrar_total_dia():
    total = total_vendido()
    messagebox.showinfo("Total Vendido", f"El total vendido en el día es: S/ {total:.2f}")


def registrar_compra():
    try:
        nombre = entry_nombre.get().strip()
        mes = entry_mes.get().strip()
        importe = float(entry_importe.get())

        if not nombre:
            messagebox.showerror("Error", "El nombre del cliente no puede estar vacío.")
            return

        if not all(c.isalpha() or c.isspace() for c in nombre):
            messagebox.showerror("Error", "El nombre del cliente solo debe contener letras y espacios.")
            return

        if not validar_mes(mes):
            messagebox.showerror("Error", "Ingrese un mes válido en español, por ejemplo: julio, octubre o diciembre.")
            return

        if importe < 0:
            messagebox.showerror("Error", "El importe de compra no puede ser negativo.")
            return

        descuento = calcular_descuento(mes, importe)
        total_final = calcular_total_final(importe, descuento)

        compras.append({
            'nombre': nombre,
            'mes': mes.strip().lower(),
            'importe': importe,
            'descuento': descuento,
            'total_final': total_final
        })

        lbl_resultado.config(
            text=(
                f"Descuento aplicado: S/ {descuento:.2f}\n"
                f"Total final: S/ {total_final:.2f}"
            )
        )

        entry_nombre.delete(0, tk.END)
        entry_mes.delete(0, tk.END)
        entry_importe.delete(0, tk.END)

        messagebox.showinfo("Éxito", "Compra registrada correctamente.")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un importe válido (número).")


def abrir():
    global entry_nombre, entry_mes, entry_importe, lbl_resultado

    ventana = tk.Tk()
    ventana.title("Sistema de Descuentos en Tienda")
    ventana.geometry("520x420")
    ventana.resizable(False, False)

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)

    tk.Label(ventana, text="Registro de Compras", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
    tk.Label(ventana, text="Promociones: Octubre 15%, Diciembre 20%, Julio 10%.", font=("Helvetica", 10)).grid(row=1, column=0, columnspan=2, pady=5)

    tk.Label(ventana, text="Nombre del Cliente:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Label(ventana, text="Mes de la Compra:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_mes = tk.Entry(ventana)
    entry_mes.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    tk.Label(ventana, text="Importe de Compra:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    entry_importe = tk.Entry(ventana)
    entry_importe.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    tk.Button(ventana, text="Calcular y Registrar", width=20, command=registrar_compra).grid(row=5, column=0, columnspan=2, pady=10)

    lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 12))
    lbl_resultado.grid(row=6, column=0, columnspan=2, pady=10)

    tk.Button(ventana, text="Total Vendido del Día", width=18, command=mostrar_total_dia).grid(row=7, column=0, pady=5)
    tk.Button(ventana, text="Ver Historial", width=18, command=mostrar_historial).grid(row=7, column=1, pady=5)
    tk.Button(ventana, text="Volver", width=18, command=lambda: [ventana.destroy(), __import__('ventana').abrir()]).grid(row=8, column=0, columnspan=2, pady=15)

    ventana.mainloop()
