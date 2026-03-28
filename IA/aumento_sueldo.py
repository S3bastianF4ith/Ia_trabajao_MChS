import tkinter as tk
from tkinter import messagebox

trabajadores = [] #Segun un video debo de hacer una lista jajas no se programar chido

def calculo_aumento(sueldo_basico):
    if sueldo_basico < 4000:
        aumento = sueldo_basico * 0.15
    elif 4000 <= sueldo_basico <= 7000:
        aumento = sueldo_basico * 0.10
    else:
        aumento = sueldo_basico * 0.08
    nuevo_sueldo = sueldo_basico + aumento
    return aumento, nuevo_sueldo

def mostrar_historial():
    historial_ventana = tk.Toplevel()
    historial_ventana.title("Historial de Trabajadores")
    historial_ventana.geometry("600x400")

    tk.Label(historial_ventana, text="Historial de Trabajadores Procesados", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    if not trabajadores:
        tk.Label(historial_ventana, text="No hay trabajadores registrados.").grid(row=1, column=0, columnspan=2)
    else:
        for i, trabajador in enumerate(trabajadores, start=1):
            info = f"{i}. Nombre: {trabajador['nombre']}, Sueldo Básico: {trabajador['sueldo_basico']:.2f}, Nuevo Sueldo: {trabajador['nuevo_sueldo']:.2f}"
            tk.Label(historial_ventana, text=info).grid(row=i, column=0, columnspan=2, sticky="w", padx=20)

    tk.Button(historial_ventana, text="Cerrar", command=historial_ventana.destroy).grid(row=len(trabajadores)+1, column=0, columnspan=2, pady=10)

def registrar_trabajador():
    try:
        nombre = str(entry_nombre.get().strip())
        sueldo_basico = float(entry_sueldo.get())

        if not nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío.")
            return
        
        if not nombre.isalpha():
            messagebox.showerror("Error", "El nombre del trabajador solo debe contener letras.")
            return

        aumento, nuevo_sueldo = calculo_aumento(sueldo_basico)

        lbl_resultado.config(text=f"Aumento: {aumento:.2f}\nNuevo Sueldo: {nuevo_sueldo:.2f}")

        trabajadores.append({
            'nombre': nombre,
            'sueldo_basico': sueldo_basico,
            'nuevo_sueldo': nuevo_sueldo
        })

        entry_nombre.delete(0, tk.END)
        entry_sueldo.delete(0, tk.END)

        messagebox.showinfo("Éxito", "Trabajador registrado correctamente.")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese un sueldo válido (número).")
       

def abrir():
    global entry_nombre, entry_sueldo, lbl_resultado

    ventana = tk.Tk()
    ventana.title("Sistema de Aumento de Sueldo")
    ventana.geometry("500x400")
    ventana.resizable(False, False)

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)

    tk.Label(ventana, text="Registro de Trabajador", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

    tk.Label(ventana, text="Nombre del Trabajador:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = tk.Entry(ventana)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(ventana, text="Sueldo Básico:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_sueldo = tk.Entry(ventana)
    entry_sueldo.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    tk.Button(ventana, text="Calcular y Registrar", width=20, command=registrar_trabajador).grid(row=3, column=0, columnspan=2, pady=10)

    lbl_resultado = tk.Label(ventana, text="", font=("Helvetica", 12))
    lbl_resultado.grid(row=4, column=0, columnspan=2, pady=10)

    tk.Button(ventana, text="Ver Historial", width=12, command=mostrar_historial).grid(row=5, column=0, pady=5)
    tk.Button(ventana, text="Volver", width=12, command=lambda: [ventana.destroy(), __import__('ventana').abrir()]).grid(row=5, column=1, pady=5)

    ventana.mainloop()
    #aqui viene lo curioso solo tomo ver muchos videos y genuinamente sigo sin saber muy bien como le hice para que no saliera mal aunque supongo que tener como 50 errores fue normal
