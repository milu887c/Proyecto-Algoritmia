from tkinter import *
from tkinter import messagebox, ttk

# ============================================================
# PRECIOS BASE (pueden modificarse desde la interfaz)
# ============================================================
PRECIOS_BASE = {
    "Baño": 20000,
    "Corte de pelo": 30000,
    "Servicio completo": 45000
}

# Ajuste por tamaño de mascota (multiplicador)
AJUSTE_TAMANO = {
    "Pequeño": 1.0,
    "Mediano": 1.3,
    "Grande": 1.6
}

# Ajuste por tipo de mascota (multiplicador)
AJUSTE_TIPO = {
    "Perro": 1.0,
    "Gato": 1.1,
    "Otro": 1.2
}

# Lista global que almacenará los servicios registrados (diccionarios)
servicios_registrados = []


# ============================================================
# FUNCIONES DE LÓGICA
# ============================================================
def calcular_costo(servicio, tamano, tipo, precios):
    """Calcula el costo total aplicando ajustes por tamaño y tipo."""
    precio_base = precios[servicio]
    multiplicador = AJUSTE_TAMANO[tamano] * AJUSTE_TIPO[tipo]
    return round(precio_base * multiplicador, 2)


def validar_campos(nombre_mascota, nombre_propietario, servicio, tamano, tipo):
    """Valida que todos los campos obligatorios estén completos."""
    if not nombre_mascota.strip():
        return "Debe ingresar el nombre de la mascota."
    if not nombre_propietario.strip():
        return "Debe ingresar el nombre del propietario."
    if not servicio:
        return "Debe seleccionar un servicio."
    if not tamano:
        return "Debe seleccionar el tamaño de la mascota."
    if not tipo:
        return "Debe seleccionar el tipo de mascota."
    return None


def obtener_precios_actuales():
    """Lee los precios que el usuario haya configurado en la interfaz."""
    try:
        precios = {
            "Baño": float(entry_precio_bano.get()),
            "Corte de pelo": float(entry_precio_corte.get()),
            "Servicio completo": float(entry_precio_completo.get())
        }
        for k, v in precios.items():
            if v <= 0:
                raise ValueError
        return precios
    except ValueError:
        raise ValueError("Los precios deben ser números positivos.")


# ============================================================
# FUNCIÓN: REGISTRAR SERVICIO
# ============================================================
def registrar_servicio():
    nombre_mascota = entry_mascota.get()
    nombre_propietario = entry_propietario.get()
    servicio = combo_servicio.get()
    tamano = combo_tamano.get()
    tipo = combo_tipo.get()

    # Validación de campos obligatorios
    error = validar_campos(nombre_mascota, nombre_propietario, servicio, tamano, tipo)
    if error:
        messagebox.showwarning("Validación", error)
        return

    # Validación de precios con try-except
    try:
        precios = obtener_precios_actuales()
    except ValueError as e:
        messagebox.showerror("Error en precios", str(e))
        return

    # Cálculo del costo
    costo = calcular_costo(servicio, tamano, tipo, precios)

    # Guardar registro como diccionario
    registro = {
        "mascota": nombre_mascota.strip(),
        "propietario": nombre_propietario.strip(),
        "tipo": tipo,
        "tamano": tamano,
        "servicio": servicio,
        "costo": costo
    }
    servicios_registrados.append(registro)

    # Mostrar detalle del cobro
    detalle = (
        "✅ Servicio registrado\n\n"
        "Mascota: " + registro["mascota"] + "\n"
        "Propietario: " + registro["propietario"] + "\n"
        "Tipo: " + registro["tipo"] + "  |  Tamaño: " + registro["tamano"] + "\n"
        "Servicio: " + registro["servicio"] + "\n"
        "Costo total: $" + format(costo, ",.2f")
    )
    messagebox.showinfo("Detalle del cobro", detalle)

    # Actualizar tabla y resumen
    actualizar_tabla()
    actualizar_resumen()

    # Limpiar campos (excepto precios)
    entry_mascota.delete(0, END)
    entry_propietario.delete(0, END)
    combo_servicio.set("")
    combo_tamano.set("")
    combo_tipo.set("")
    entry_mascota.focus()


# ============================================================
# FUNCIÓN: ACTUALIZAR TABLA
# ============================================================
def actualizar_tabla():
    # Limpiar tabla
    for fila in tabla.get_children():
        tabla.delete(fila)

    # Recorrer con ciclo for y llenar
    for i, r in enumerate(servicios_registrados, start=1):
        tabla.insert("", END, values=(
            i, r["mascota"], r["propietario"], r["tipo"],
            r["tamano"], r["servicio"], "$" + format(r["costo"], ",.2f")
        ))


# ============================================================
# FUNCIÓN: ACTUALIZAR RESUMEN (contadores y acumuladores)
# ============================================================
def actualizar_resumen():
    total_mascotas = len(servicios_registrados)
    ingresos_totales = 0
    conteo_servicios = {"Baño": 0, "Corte de pelo": 0, "Servicio completo": 0}

    # Ciclo for: acumuladores y contadores
    for r in servicios_registrados:
        ingresos_totales += r["costo"]
        conteo_servicios[r["servicio"]] += 1

    # Determinar servicio más solicitado con condicionales
    mas_solicitado = "—"
    if total_mascotas > 0:
        max_cant = max(conteo_servicios.values())
        # Ciclo para encontrar todos los empatados
        empatados = [s for s, c in conteo_servicios.items() if c == max_cant]
        mas_solicitado = ", ".join(empatados) + " (" + str(max_cant) + ")"

    promedio = ingresos_totales / total_mascotas if total_mascotas > 0 else 0

    lbl_resumen.config(
        text=(
            "Mascotas atendidas: " + str(total_mascotas) + "    |    "
            "Ingresos totales: $" + format(ingresos_totales, ",.2f") + "    |    "
            "Promedio por servicio: $" + format(promedio, ",.2f") + "\n"
            "Servicio más solicitado: " + mas_solicitado
        )
    )


# ============================================================
# FUNCIÓN: LIMPIAR REGISTROS
# ============================================================
def limpiar_registros():
    if not servicios_registrados:
        messagebox.showinfo("Información", "No hay registros para eliminar.")
        return
    if messagebox.askyesno("Confirmar", "¿Desea eliminar todos los registros?"):
        servicios_registrados.clear()
        actualizar_tabla()
        actualizar_resumen()
        messagebox.showinfo("Listo", "Registros eliminados correctamente.")


# ============================================================
# INTERFAZ GRÁFICA
# ============================================================
ventana = Tk()
ventana.title("🐾 Peluquería de Mascotas - Sistema de Servicios")
ventana.geometry("980x720")
ventana.configure(bg="#f4f6fb")

# -------- TÍTULO --------
Label(ventana, text="🐶 Sistema de Servicios - Peluquería de Mascotas 🐱",
      font=("Segoe UI", 16, "bold"), bg="#f4f6fb", fg="#2a3b70").pack(pady=10)

# -------- MARCO: DATOS DE LA MASCOTA --------
frame_datos = LabelFrame(ventana, text=" Datos de la mascota ",
                         font=("Segoe UI", 11, "bold"), bg="#f4f6fb", padx=10, pady=10)
frame_datos.pack(fill="x", padx=15, pady=5)

Label(frame_datos, text="Nombre mascota:", bg="#f4f6fb").grid(row=0, column=0, sticky="w", padx=5, pady=3)
entry_mascota = Entry(frame_datos, width=25)
entry_mascota.grid(row=0, column=1, padx=5, pady=3)

Label(frame_datos, text="Propietario:", bg="#f4f6fb").grid(row=0, column=2, sticky="w", padx=5, pady=3)
entry_propietario = Entry(frame_datos, width=25)
entry_propietario.grid(row=0, column=3, padx=5, pady=3)

Label(frame_datos, text="Tipo:", bg="#f4f6fb").grid(row=1, column=0, sticky="w", padx=5, pady=3)
combo_tipo = ttk.Combobox(frame_datos, values=["Perro", "Gato", "Otro"], state="readonly", width=22)
combo_tipo.grid(row=1, column=1, padx=5, pady=3)

Label(frame_datos, text="Tamaño:", bg="#f4f6fb").grid(row=1, column=2, sticky="w", padx=5, pady=3)
combo_tamano = ttk.Combobox(frame_datos, values=["Pequeño", "Mediano", "Grande"], state="readonly", width=22)
combo_tamano.grid(row=1, column=3, padx=5, pady=3)

Label(frame_datos, text="Servicio:", bg="#f4f6fb").grid(row=2, column=0, sticky="w", padx=5, pady=3)
combo_servicio = ttk.Combobox(frame_datos, values=["Baño", "Corte de pelo", "Servicio completo"],
                              state="readonly", width=22)
combo_servicio.grid(row=2, column=1, padx=5, pady=3)

# -------- MARCO: PRECIOS --------
frame_precios = LabelFrame(ventana, text=" Precios base por servicio (editables) ",
                           font=("Segoe UI", 11, "bold"), bg="#f4f6fb", padx=10, pady=10)
frame_precios.pack(fill="x", padx=15, pady=5)

Label(frame_precios, text="Baño $:", bg="#f4f6fb").grid(row=0, column=0, padx=5)
entry_precio_bano = Entry(frame_precios, width=10)
entry_precio_bano.insert(0, str(PRECIOS_BASE["Baño"]))
entry_precio_bano.grid(row=0, column=1, padx=5)

Label(frame_precios, text="Corte de pelo $:", bg="#f4f6fb").grid(row=0, column=2, padx=5)
entry_precio_corte = Entry(frame_precios, width=10)
entry_precio_corte.insert(0, str(PRECIOS_BASE["Corte de pelo"]))
entry_precio_corte.grid(row=0, column=3, padx=5)

Label(frame_precios, text="Servicio completo $:", bg="#f4f6fb").grid(row=0, column=4, padx=5)
entry_precio_completo = Entry(frame_precios, width=10)
entry_precio_completo.insert(0, str(PRECIOS_BASE["Servicio completo"]))
entry_precio_completo.grid(row=0, column=5, padx=5)

# -------- BOTONES --------
frame_botones = Frame(ventana, bg="#f4f6fb")
frame_botones.pack(pady=10)

btn_registrar = Button(frame_botones, text="➕ Registrar servicio", command=registrar_servicio,
                       bg="#2a9d8f", fg="white", font=("Segoe UI", 10, "bold"),
                       padx=15, pady=6, cursor="hand2")
btn_registrar.grid(row=0, column=0, padx=10)

btn_limpiar = Button(frame_botones, text="🗑️ Limpiar registros", command=limpiar_registros,
                     bg="#e76f51", fg="white", font=("Segoe UI", 10, "bold"),
                     padx=15, pady=6, cursor="hand2")
btn_limpiar.grid(row=0, column=1, padx=10)

# -------- TABLA DE REGISTROS --------
frame_tabla = LabelFrame(ventana, text=" Servicios realizados ",
                         font=("Segoe UI", 11, "bold"), bg="#f4f6fb", padx=10, pady=10)
frame_tabla.pack(fill="both", expand=True, padx=15, pady=5)

columnas = ("#", "Mascota", "Propietario", "Tipo", "Tamaño", "Servicio", "Costo")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=110, anchor="center")
tabla.column("#", width=40)
tabla.pack(fill="both", expand=True)

# -------- RESUMEN --------
frame_resumen = LabelFrame(ventana, text=" Resumen del establecimiento ",
                           font=("Segoe UI", 11, "bold"), bg="#f4f6fb", padx=10, pady=10)
frame_resumen.pack(fill="x", padx=15, pady=10)

lbl_resumen = Label(frame_resumen,
                    text="Mascotas atendidas: 0    |    Ingresos totales: $0.00    |    "
                         "Promedio por servicio: $0.00\nServicio más solicitado: —",
                    font=("Segoe UI", 10), bg="#f4f6fb", fg="#2a3b70", justify="left")
lbl_resumen.pack(anchor="w")

# -------- INICIALIZAR --------
actualizar_resumen()
ventana.mainloop()