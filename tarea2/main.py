import os
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


class WineDashboard(ctk.CTk):
    """
    Clase principal para el dashboard de análisis de vinos.
    Maneja login, carga de datos y visualización de consultas.
    """
    def __init__(self):
        super().__init__()
       
        self.title("Consultas complejas de Vino")
        self.geometry("1280x760")
        self.minsize(1100, 680)
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue")

        self.credentials = self.load_credentials()
        self.dataset = self.load_data()

        self.current_canvas = None
        self.current_figure_frame = None
        self.current_title = None
        self.current_index = None

        self.login_frame = None
        self.app_frame = None

        self.create_login_frame()

    def load_credentials(self):
        """
        Carga las credenciales desde el archivo credentials.csv.
        Retorna un diccionario con usuario como clave y contraseña como valor.
         
        """
        file_path = os.path.join(os.path.dirname(__file__), "credentials.csv")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No se encontró el archivo de credenciales: {file_path}")
        credentials = pd.read_csv(file_path, dtype=str).fillna("")
        return dict(zip(credentials["username"].str.strip(), credentials["password"].str.strip()))

    def load_data(self):
        """
        Carga el dataset de vinos desde winequalityN.csv.
        Limpia los nombres de columnas y convierte numéricas.
         Aclaro que el dataset debera de estar en la misma carpeta que el codigo porque si no las consultas no se podran hacer
         y por lo tanto directamente el codigo se hara inutilizable, por lo que se recomienda tener el dataset en la misma carpeta que el codigo para evitar problemas de carga.
        """
        local_path = os.path.join(os.path.dirname(__file__), "winequalityN.csv")
        parent_path = os.path.join(os.path.dirname(__file__), "..", "winequalityN.csv")
        data_path = local_path if os.path.exists(local_path) else parent_path
        if not os.path.exists(data_path):
            raise FileNotFoundError("No se encontró el archivo winequalityN.csv.")
        data = pd.read_csv(data_path)
        data.columns = [col.strip() for col in data.columns]
        numeric_columns = [col for col in data.columns if col != "type"]
        for col in numeric_columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
        data = data.dropna(subset=numeric_columns).reset_index(drop=True)
        data["type"] = data["type"].astype(str).str.strip()
        return data

    def create_login_frame(self):
        self.login_frame = ctk.CTkFrame(self, corner_radius=12)
        self.login_frame.pack(fill="both", expand=True, padx=40, pady=40)
        ctk.CTkLabel(self.login_frame, text="Iniciar sesión", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(24, 16))
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Usuario", width=320)
        self.username_entry.pack(pady=(0, 12))
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Contraseña", width=320, show="*")
        self.password_entry.pack(pady=(0, 24))
        ctk.CTkButton(self.login_frame, text="Entrar", width=240, command=self.validate_login).pack(pady=(0, 16))
        
    def validate_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Validación", "El usuario y la contraseña son obligatorios.")
            return

        stored_password = self.credentials.get(username)
        if stored_password is None or password != stored_password:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            return

        self.login_frame.pack_forget()
        self.create_app_frame()

    def create_app_frame(self):
        self.app_frame = ctk.CTkFrame(self, corner_radius=0)
        self.app_frame.pack(fill="both", expand=True)
        top_frame = ctk.CTkFrame(self.app_frame, corner_radius=0)
        top_frame.pack(fill="x")
        ctk.CTkLabel(top_frame, text="Dashboard de Análisis de Vinos", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=12)
        content_frame = ctk.CTkFrame(self.app_frame, corner_radius=0)
        content_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        query_frame = ctk.CTkFrame(content_frame, width=280)
        query_frame.pack(side="left", fill="y", padx=(0, 12), pady=12)
        query_frame.pack_propagate(False)
        self.figure_parent = ctk.CTkFrame(content_frame)
        self.figure_parent.pack(side="left", fill="both", expand=True, pady=12)
        self.build_query_panel(query_frame)
        self.build_result_panel(self.figure_parent)

    def build_query_panel(self, parent):
        ctk.CTkLabel(parent, text="Consultas disponibles", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(12, 8))
        buttons = [
            ("1. Distribución de tipos de vino", self.query_type_distribution_pie),
            ("2. Histograma de alcohol", self.query_alcohol_histogram),
            ("3. Boxplot de calidad por tipo", self.query_quality_boxplot_by_type),
            ("4. Dispersión azúcar vs alcohol", self.query_sugar_alcohol_scatter),
            ("5. Mapa de correlación", self.query_correlation_heatmap),
            ("6. Línea: sulfatos por calidad", self.query_sulphates_line_quality),
            ("7. Área de pH", self.query_ph_area_by_type),
            ("8. Burbuja: sulfuros", self.query_sulfur_bubble),
            ("9. Barras: acidez volátil", self.query_acidity_bar_quality),
            ("10. Histograma de densidad", self.query_density_variance_histogram),
        ]
        for text, command in buttons:
            ctk.CTkButton(parent, text=text, width=280, command=command).pack(pady=6)
        ctk.CTkButton(parent, text="Salir", width=280, command=self.destroy).pack(pady=(18, 12))
        ctk.CTkLabel(parent, text="").pack(fill="both", expand=True)

    def build_result_panel(self, figure_parent):
        ctk.CTkLabel(figure_parent, text="Gráfica", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(12, 10), anchor="w", padx=12)
        self.figure_container = ctk.CTkFrame(figure_parent, height=400)
        self.figure_container.pack(fill="x", padx=12, pady=(0, 12))
        self.interpretation_textbox = ctk.CTkTextbox(figure_parent, height=150, corner_radius=10)
        self.interpretation_textbox.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.interpretation_textbox.configure(state="normal")
        self.interpretation_textbox.insert("0.0", "Presione 'Interpretación' para ver el análisis aquí.\n")
        self.interpretation_textbox.configure(state="disabled")

    def clear_result_area(self):
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None
        if self.current_figure_frame:
            self.current_figure_frame.destroy()
            self.current_figure_frame = None
        self.interpretation_textbox.configure(state="normal")
        self.interpretation_textbox.delete("0.0", tk.END)
        self.interpretation_textbox.insert("0.0", "Presione 'Interpretación' para ver el análisis aquí.\n")
        self.interpretation_textbox.configure(state="disabled")
        self.current_index = None

    def show_summary(self, df: pd.DataFrame, index: int, stats: str = ""):
        self.current_title = f"Consulta {index+1}"
        self.current_index = index
        self.show_details()

    def show_details(self):
        if self.current_index is None:
            messagebox.showinfo("Interpretación", "Seleccione primero una consulta para ver la interpretación de la gráfica.")
            return
        interpretation = self.generate_interpretation(self.current_index)
        self.interpretation_textbox.configure(state="normal")
        self.interpretation_textbox.delete("0.0", tk.END)
        self.interpretation_textbox.insert("0.0", interpretation)
        self.interpretation_textbox.configure(state="disabled")



    def generate_interpretation(self, index: int) -> str:
        interpretations = [
            "Esta gráfica circular muestra cómo se distribuyen los tipos de vino en nuestro dataset. Si uno de los tipos, como el vino tinto o blanco, ocupa una porción mucho mayor del pastel, significa que tenemos más muestras de ese tipo en los datos. Esto podría influir en análisis posteriores, ya que el tipo más representado podría sesgar las conclusiones generales sobre la calidad o composición del vino.",
            "El histograma del contenido de alcohol revela la frecuencia de diferentes niveles de alcohol en los vinos. Las líneas verticales indican la media (promedio) y la mediana (valor central). Si la media está a la derecha de la mediana, la distribución está sesgada hacia vinos con más alcohol, lo que podría indicar una tendencia en la producción o preferencias de mercado. La varianza mide cuánto varían los niveles de alcohol alrededor de la media.",
            "El diagrama de cajas compara la calidad percibida entre tipos de vino. Cada caja representa el rango intercuartílico (del 25% al 75% de los datos), con la línea media dentro. Los puntos fuera de las cajas son valores atípicos. Si un tipo tiene una caja más alta o más ancha, significa mayor variabilidad en la calidad. Esto ayuda a entender si ciertos tipos de vino son más consistentes en su calidad.",
            "Este gráfico de dispersión muestra la relación entre el azúcar residual y el alcohol, con colores representando la calidad. Una correlación positiva (puntos subiendo a la derecha) sugeriría que vinos con más azúcar tienden a tener más alcohol. Los colores más oscuros (calidad alta) podrían agruparse en ciertas áreas, indicando patrones en cómo se combinan estos atributos para lograr mejores calificaciones.",
            "Las barras muestran la fuerza de correlación absoluta entre el alcohol y otras variables numéricas del vino. Barras más altas indican relaciones más fuertes. Por ejemplo, si la densidad tiene una barra alta, significa que el alcohol y la densidad cambian juntos de manera predecible. Esto es útil para identificar qué factores están más ligados al contenido de alcohol en la producción de vino.",
            "Las barras representan el promedio de sulfatos para cada nivel de calidad. Sulfatos son aditivos que afectan el sabor y preservación. Si las barras aumentan con la calidad, podría indicar que vinos mejores usan más sulfatos. La varianza alrededor de cada barra muestra cuánto varían los sulfatos dentro de cada grupo de calidad, ayudando a entender la consistencia en el uso de este compuesto.",
            "El histograma simple del pH muestra la acidez de los vinos. Un pH bajo indica mayor acidez. La distribución podría ser normal o sesgada, revelando tendencias en la acidez general del dataset. Estadísticas como media y desviación estándar en la tabla resumen ayudan a cuantificar qué tan ácidos son los vinos en promedio y cuánto varían.",
            "Los puntos muestran la relación entre dióxido de azufre libre y total, coloreados por calidad. Una relación lineal ascendente es esperada ya que el total incluye el libre. Vinos de mayor calidad (colores más intensos) podrían tener patrones distintos, quizás más dióxido de azufre para mejor preservación. La varianza en las medias indica dispersión en el uso de este conservante.",
            "Las barras con líneas de error muestran la acidez volátil promedio por calidad, con las líneas indicando la desviación estándar. Acidez volátil alta puede causar sabores indeseados. Si las barras disminuyen con la calidad, significa que vinos mejores controlan mejor esta acidez. La varianza mide la consistencia en el control de acidez dentro de cada nivel de calidad.",
            "El histograma de densidad incluye líneas para media y mediana. Densidad relaciona con azúcar y alcohol. Una distribución sesgada podría indicar predominio de ciertos estilos de vino. La varianza cuantifica la diversidad en densidad, y comparar media vs mediana revela asimetría en la composición física de los vinos."
        ]
        return interpretations[index] if 0 <= index < len(interpretations) else "Interpretación no disponible."
    def append_text(self, text: str):
        self.result_text.configure(state="normal")
        self.result_text.delete("0.0", tk.END)
        self.result_text.insert("0.0", text)
        self.result_text.configure(state="disabled")

    def plot_figure(self, figure):
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None
        if self.current_figure_frame:
            self.current_figure_frame.destroy()
        self.current_figure_frame = ctk.CTkFrame(self.figure_container)
        self.current_figure_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.current_canvas = FigureCanvasTkAgg(figure, master=self.current_figure_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True)

    def query_type_distribution_pie(self):
        counts = self.dataset["type"].value_counts().reset_index()
        counts.columns = ["type", "count"]
        self.clear_result_area()
        self.show_summary(counts, 0, "Conteo total por tipo de vino.")
        figure = plt.Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        ax.pie(counts["count"], labels=counts["type"], autopct="%1.1f%%", startangle=140)
        ax.set_title("Proporción de vinos por tipo")
        self.plot_figure(figure)

    def query_alcohol_histogram(self):
        alcohol = self.dataset["alcohol"]
        mean_val, median_val, std_val, var_val = alcohol.mean(), alcohol.median(), alcohol.std(), alcohol.var()
        stats = f"Media de alcohol: {mean_val:.3f}\nMediana de alcohol: {median_val:.3f}\nDesviación estándar: {std_val:.3f}\nVarianza: {var_val:.4f}\n"
        self.clear_result_area()
        self.show_summary(self.dataset[["alcohol", "quality", "type"]].sample(n=min(200, len(self.dataset))), 1, stats)
        figure = plt.Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        ax.hist(alcohol, bins=15, color="#4c72b0", alpha=0.85)
        ax.axvline(mean_val, color="red", linestyle="--", label=f"Media {mean_val:.2f}")
        ax.axvline(median_val, color="green", linestyle=":", label=f"Mediana {median_val:.2f}")
        ax.set_title("Distribución de alcohol")
        ax.set_xlabel("Alcohol")
        ax.set_ylabel("Frecuencia")
        ax.legend()
        self.plot_figure(figure)

    def query_quality_boxplot_by_type(self):
        grouped = [self.dataset[self.dataset["type"] == t]["quality"] for t in self.dataset["type"].unique()]
        labels = list(self.dataset["type"].unique())
        by_type = self.dataset.groupby("type")["quality"].agg(["mean", "median", "std", "var"]).round(3).reset_index()
        self.clear_result_area()
        self.show_summary(by_type, 2, by_type.to_string(index=False))
        figure = plt.Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        ax.boxplot(grouped, labels=labels, patch_artist=True, medianprops={"color": "black"})
        ax.set_title("Calidad por tipo de vino")
        ax.set_ylabel("Quality")
        self.plot_figure(figure)

    def query_sugar_alcohol_scatter(self):
        corr = self.dataset[["residual sugar", "alcohol"]].corr().iloc[0, 1]
        stats = f"Correlación entre azúcar residual y alcohol: {corr:.3f}\nPromedio de alcohol: {self.dataset['alcohol'].mean():.3f}\nPromedio de azúcar residual: {self.dataset['residual sugar'].mean():.3f}\n"
        self.clear_result_area()
        self.show_summary(self.dataset[["residual sugar", "alcohol", "quality"]].sample(n=min(200, len(self.dataset))), 3, stats)
        figure = plt.Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        scatter = ax.scatter(self.dataset["residual sugar"], self.dataset["alcohol"], c=self.dataset["quality"], cmap="viridis", alpha=0.7, s=45)
        ax.set_title("Azúcar residual vs Alcohol")
        ax.set_xlabel("Residual sugar")
        ax.set_ylabel("Alcohol")
        figure.colorbar(scatter, ax=ax).set_label("Quality")
        self.plot_figure(figure)

    def query_correlation_heatmap(self):
        corr = self.dataset.select_dtypes(include=[np.number]).corr()["alcohol"].abs().sort_values(ascending=False).drop("alcohol").reset_index()
        corr.columns = ["variable", "correlation"]
        self.clear_result_area()
        self.show_summary(corr, 4, "Correlación absoluta con alcohol.")
        figure = plt.Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        ax.bar(corr["variable"], corr["correlation"], color="skyblue")
        ax.set_title("Correlación con alcohol")
        ax.set_ylabel("Correlación absoluta")
        ax.tick_params(axis='x', rotation=45)
        self.plot_figure(figure)

    def query_sulphates_line_quality(self):
        df = self.dataset.groupby("quality")["sulphates"].agg(["mean", "std", "var"]).round(3).reset_index()
        self.clear_result_area()
        self.show_summary(df, 5, df.to_string(index=False))
        figure = plt.Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        ax.bar(df["quality"].astype(str), df["mean"], color="#d9534f", alpha=0.8)
        ax.set_title("Sulfatos promedio según calidad")
        ax.set_xlabel("Quality")
        ax.set_ylabel("Average sulphates")
        self.plot_figure(figure)

    def query_ph_area_by_type(self):
        df = self.dataset.copy()
        summary_df = df["pH"].describe().round(3).reset_index()
        summary_df.columns = ["stat", "value"]
        self.clear_result_area()
        self.show_summary(summary_df, 6, "Estadísticas descriptivas de pH.")
        figure = plt.Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        ax.hist(df["pH"], bins=20, color="lightgreen", alpha=0.8)
        ax.set_title("Distribución de pH")
        ax.set_xlabel("pH")
        ax.set_ylabel("Frecuencia")
        self.plot_figure(figure)

    def query_sulfur_bubble(self):
        df = self.dataset.copy()
        free_mean, total_mean = df["free sulfur dioxide"].mean(), df["total sulfur dioxide"].mean()
        free_var, total_var = df["free sulfur dioxide"].var(), df["total sulfur dioxide"].var()
        stats = f"Media de sulfuro libre: {free_mean:.2f}\nMedia de sulfuro total: {total_mean:.2f}\nVarianza libre: {free_var:.2f}\nVarianza total: {total_var:.2f}\n"
        self.clear_result_area()
        self.show_summary(df[["free sulfur dioxide", "total sulfur dioxide", "quality"]].sample(n=min(200, len(df))), 7, stats)
        figure = plt.Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        ax.scatter(df["free sulfur dioxide"], df["total sulfur dioxide"], c=df["quality"], cmap="plasma", alpha=0.6)
        ax.set_title("Relación entre sulfuro libre y total")
        ax.set_xlabel("Free sulfur dioxide")
        ax.set_ylabel("Total sulfur dioxide")
        figure.colorbar(ax.collections[0], ax=ax).set_label("Quality")
        self.plot_figure(figure)

    def query_acidity_bar_quality(self):
        df = self.dataset.groupby("quality")["volatile acidity"].agg(["mean", "std", "var"]).round(3).reset_index()
        self.clear_result_area()
        self.show_summary(df, 8, df.to_string(index=False))
        figure = plt.Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        ax.bar(df["quality"].astype(str), df["mean"], color="#5cb85c", alpha=0.8)
        ax.errorbar(df["quality"].astype(str), df["mean"], yerr=df["std"], fmt="none", ecolor="black", capsize=4)
        ax.set_title("Acidez volátil por calidad")
        ax.set_xlabel("Quality")
        ax.set_ylabel("Average volatile acidity")
        self.plot_figure(figure)

    def query_density_variance_histogram(self):
        density = self.dataset["density"]
        mean_val, median_val, std_val, var_val = density.mean(), density.median(), density.std(), density.var()
        stats = f"Media de densidad: {mean_val:.5f}\nMediana de densidad: {median_val:.5f}\nDesviación estándar: {std_val:.5f}\nVarianza de densidad: {var_val:.8f}\n"
        self.clear_result_area()
        self.show_summary(self.dataset[["density", "alcohol", "quality"]], 9, stats)
        figure = plt.Figure(figsize=(8, 5), dpi=100)
        ax = figure.add_subplot(111)
        ax.hist(density, bins=20, color="#8c564b", alpha=0.9)
        ax.axvline(mean_val, color="red", linestyle="--", label=f"Media {mean_val:.5f}")
        ax.axvline(median_val, color="green", linestyle=":", label=f"Mediana {median_val:.5f}")
        ax.set_title("Histograma de densidad del vino")
        ax.set_xlabel("Density")
        ax.set_ylabel("Frecuencia")
        ax.legend()
        self.plot_figure(figure)


if __name__ == "__main__":
    app = WineDashboard()
    app.mainloop()
