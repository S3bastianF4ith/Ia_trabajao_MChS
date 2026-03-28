import tkinter as tk
import ventana

USER_VALIDO = 'admin'
PASS_VALIDA = '1234'

def login():
    
    user = entry_user.get()
    pwd = entry_pass.get()
    
    if user == USER_VALIDO and pwd == PASS_VALIDA:
        root.destroy()
        ventana.abrir()
    else:
        lbl_msg.config(text="Usuario o contraseña incorrectos")
       
root = tk.Tk()
root.title("Login")

tk.Label(root, text="Usuario:").grid(row=0, column=0, padx=0, pady=5)
entry_user = tk.Entry(root)
entry_user.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Contraseña:").grid(row=1, column=0, padx=0, pady=5)
entry_pass = tk.Entry(root, show="*")
entry_pass.grid(row=1, column=1, padx=10, pady=5)

tk.Button(root, text="Login", command=login).grid(row=2, column=0, columnspan=2, pady=10)

lbl_msg = tk.Label(root, text="", fg="red")
lbl_msg.grid(row=3, column=0, columnspan=2)

root.bind('<Return>', lambda event: login())

entry_user.focus()
root.mainloop()