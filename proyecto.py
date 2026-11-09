from tkinter import *
from tkinter import ttk, messagebox

# ============================================================
# PRECIOS BASE POR SERVICIO
# ============================================================
PRECIOS_BASE = {
    "Baño": 20000,
    "Corte de pelo": 30000,
    "Servicio completo": 45000
}

RECARGO_TAMANO = {
    "Pequeño": 1.0,
    "Mediano": 1.2,
    "Grande": 1.5
}

RECARGO_TIPO = {
    "Perro": 1.0,
    "Gato": 1.15,
    "Otro": 1.25
}

# ============================================================
# ESTRUCTURAS DE ALMACENAMIENTO EN MEMORIA
# ============================================================
servicios_registrados = []   # lo que se muestra / se va registrando en pantalla
historial_servicios = []     # histórico acumulado, NUNCA se borra al limpiar pantalla


# ============================================================
# FUNCIÓN AUXILIAR: Escribir en el área de resultados
# (habilita, escribe, deshabilita)
# ============================================================
def escribir_resultado(texto):
    area_resultados.config(state="normal")   # habilitar para escribir
    area_resultados.insert(END, texto)
    area_resultados.see(END)
    area_resultados.config(state="disabled") # volver a bloquear


# ============================================================
# FUNCIÓN: Calcular costo total del servicio
# ============================================================
def calcular_costo(tipo_mascota, tamano, servicio):
    try:
        precio_base = PRECIOS_BASE[servicio]
        factor_tipo = RECARGO_TIPO[tipo_mascota]
        factor_tamano = RECARGO_TAMANO[tamano]
        total = precio_base * factor_tipo * factor_tamano
        return round(total, 2)
    except KeyError:
        messagebox.showerror("Error de configuración",
                             "Los datos seleccionados no tienen precio asignado.")
        return None


# ============================================================
# FUNCIÓN: Validar campos obligatorios
# ============================================================
def validar_campos(nombre_mascota, nombre_dueno, tipo, tamano, servicio):
    if not nombre_mascota.strip():
        messagebox.showerror("Error", "Debe ingresar el nombre de la mascota.")
        return False
    if not nombre_dueno.strip():
        messagebox.showerror("Error", "Debe ingresar el nombre del propietario.")
        return False
    if not tipo:
        messagebox.showerror("Error", "Debe seleccionar el tipo de mascota.")
        return False
    if not tamano:
        messagebox.showerror("Error", "Debe seleccionar el tamaño de la mascota.")
        return False
    if not servicio:
        messagebox.showerror("Error", "Debe seleccionar el servicio.")
        return False
    return True


# ============================================================
# FUNCIÓN: Aplicar descuento opcional (valida con try-except)
# ============================================================
def aplicar_descuento(total):
    texto = entrada_descuento.get().strip()

    if texto == "":
        return total, 0

    try:
        descuento = float(texto)
    except ValueError:
        messagebox.showerror("Error de entrada",
                             "El descuento debe ser un número (ej: 10 o 12.5).")
        return None, None

    if descuento < 0 or descuento > 100:
        messagebox.showerror("Error",
                             "El descuento debe estar entre 0 y 100.")
        return None, None

    total_final = total - (total * descuento / 100)
    return round(total_final, 2), descuento


# ============================================================
# FUNCIÓN: Mostrar mensaje inicial
# ============================================================
def mostrar_mensaje_inicial():
    escribir_resultado(
        "Bienvenido al sistema de la peluquería de mascotas 🐾\n"
        "Complete los datos y presione 'Registrar servicio'.\n\n"
        "Precios base:\n"
        f"   • Baño: ${PRECIOS_BASE['Baño']:,.0f}\n"
        f"   • Corte de pelo: ${PRECIOS_BASE['Corte de pelo']:,.0f}\n"
        f"   • Servicio completo: ${PRECIOS_BASE['Servicio completo']:,.0f}\n\n"
        "Recargos por tamaño: Pequeño x1.0 | Mediano x1.2 | Grande x1.5\n"
        "Recargos por tipo: Perro x1.0 | Gato x1.15 | Otro x1.25\n"
        + "-"*55 + "\n"
    )


# ============================================================
# FUNCIÓN: Registrar un servicio
# ============================================================
def registrar_servicio():
    nombre_mascota = entrada_mascota.get()
    nombre_dueno = entrada_dueno.get()
    tipo = combo_tipo.get()
    tamano = combo_tamano.get()
    servicio = combo_servicio.get()

    if not validar_campos(nombre_mascota, nombre_dueno, tipo, tamano, servicio):
        return

    total_base = calcular_costo(tipo, tamano, servicio)
    if total_base is None:
        return

    total_final, descuento = aplicar_descuento(total_base)
    if total_final is None:
        return

    registro = {
        "mascota": nombre_mascota.strip(),
        "dueno": nombre_dueno.strip(),
        "tipo": tipo,
        "tamano": tamano,
        "servicio": servicio,
        "total_base": total_base,
        "descuento": descuento,
        "total": total_final
    }

    servicios_registrados.append(registro)
    historial_servicios.append(registro)   # ← también al historial

    detalle = (
        f"🐾 Mascota: {registro['mascota']} | Dueño: {registro['dueno']}\n"
        f"   Tipo: {tipo} | Tamaño: {tamano} | Servicio: {servicio}\n"
        f"   💰 Costo base: ${total_base:,.2f}\n"
    )
    if descuento > 0:
        detalle += f"   🎁 Descuento aplicado: {descuento:g}%\n"
    detalle += (
        f"   ✅ Total a pagar: ${total_final:,.2f}\n"
        f"{'-'*55}\n"
    )
    escribir_resultado(detalle)

    entrada_mascota.delete(0, END)
    entrada_dueno.delete(0, END)
    entrada_descuento.delete(0, END)
    combo_tipo.set("")
    combo_tamano.set("")
    combo_servicio.set("")

    messagebox.showinfo("Registro exitoso",
                        f"Servicio registrado para {registro['mascota']}.\n"
                        f"Total a pagar: ${total_final:,.2f}")


# ============================================================
# FUNCIÓN: Generar resumen (usa ciclo FOR) — sobre el HISTORIAL
# ============================================================
def generar_resumen():
    if not historial_servicios:
        messagebox.showwarning("Sin datos",
                               "No hay servicios registrados aún.")
        return

    total_mascotas = 0
    ingresos_totales = 0.0
    conteo_servicios = {"Baño": 0, "Corte de pelo": 0, "Servicio completo": 0}

    for reg in historial_servicios:
        total_mascotas += 1
        ingresos_totales += reg["total"]
        conteo_servicios[reg["servicio"]] += 1

    promedio = ingresos_totales / total_mascotas

    servicio_top = max(conteo_servicios, key=conteo_servicios.get)
    cantidad_top = conteo_servicios[servicio_top]

    resumen = (
        "\n" + "="*55 + "\n"
        "           📊 RESUMEN DE INGRESOS 📊\n"
        + "="*55 + "\n"
        f"🐶 Mascotas atendidas: {total_mascotas}\n"
        f"💵 Ingresos totales:  ${ingresos_totales:,.2f}\n"
        f"📈 Promedio por servicio: ${promedio:,.2f}\n\n"
        f"🏆 Servicio más solicitado: {servicio_top} ({cantidad_top} veces)\n\n"
        "Detalle por servicio:\n"
    )
    for serv, cant in conteo_servicios.items():
        resumen += f"   • {serv}: {cant} atención(es)\n"
    resumen += "="*55 + "\n"

    escribir_resultado(resumen)


# ============================================================
# FUNCIÓN: Mostrar listado (usa ciclo WHILE) — sobre el HISTORIAL
# ============================================================
def mostrar_listado():
    if not historial_servicios:
        messagebox.showwarning("Sin datos", "No hay servicios registrados.")
        return

    escribir_resultado(
        "\n📋 LISTADO DE SERVICIOS REGISTRADOS\n" + "-"*55 + "\n"
    )

    i = 0
    while i < len(historial_servicios):
        reg = historial_servicios[i]
        escribir_resultado(
            f"{i+1}. {reg['mascota']} ({reg['tipo']}/{reg['tamano']}) - "
            f"{reg['servicio']} - ${reg['total']:,.2f}\n"
        )
        i += 1

    escribir_resultado("-"*55 + "\n")


# ============================================================
# FUNCIÓN: Limpiar pantalla (conserva el historial → resumen y listado intactos)
# ============================================================
def limpiar_resultados():
    if messagebox.askyesno("Confirmar",
                           "¿Desea borrar la pantalla?\n"
                           "El historial acumulado se conservará y seguirá "
                           "apareciendo en 'Ver resumen' y 'Ver listado'."):
        servicios_registrados.clear()   # solo la vista actual
        # historial_servicios NO se toca

        # Borrar todo el contenido (hay que habilitar para poder borrar)
        area_resultados.config(state="normal")
        area_resultados.delete("1.0", END)
        area_resultados.config(state="disabled")

        mostrar_mensaje_inicial()

        entrada_mascota.delete(0, END)
        entrada_dueno.delete(0, END)
        entrada_descuento.delete(0, END)
        combo_tipo.set("")
        combo_tamano.set("")
        combo_servicio.set("")


# ============================================================
# FUNCIÓN NUEVA: Reiniciar TODO (borra historial → resumen y listado quedan vacíos)
# ============================================================
def reiniciar_todo():
    if messagebox.askyesno("Confirmar",
                           "¿Borrar TODO el historial? Esta acción no se puede deshacer.\n"
                           "Se perderán tanto el resumen como el listado."):
        servicios_registrados.clear()
        historial_servicios.clear()

        area_resultados.config(state="normal")
        area_resultados.delete("1.0", END)
        area_resultados.config(state="disabled")

        mostrar_mensaje_inicial()

        entrada_mascota.delete(0, END)
        entrada_dueno.delete(0, END)
        entrada_descuento.delete(0, END)
        combo_tipo.set("")
        combo_tamano.set("")
        combo_servicio.set("")


# ============================================================
# INTERFAZ GRÁFICA CON TKINTER
# ============================================================
ventana = Tk()
ventana.title("Peluquería de Mascotas - Registro de Servicios")
ventana.geometry("760x690")
ventana.configure(bg="#F4F1EA")
ventana.iconbitmap('icono.ico')

# Título
titulo = Label(ventana, text="🐾 Peluquería de Mascotas 🐾",
               font=("Arial", 18, "bold"), bg="#F4F1EA", fg="#4A3B2A")
titulo.pack(pady=10)

# Frame de formulario
frame_form = Frame(ventana, bg="#F4F1EA")
frame_form.pack(pady=10)

# Nombre de la mascota
Label(frame_form, text="Nombre de la mascota:", bg="#F4F1EA",
      font=("Arial", 11)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
entrada_mascota = Entry(frame_form, width=30, font=("Arial", 11))
entrada_mascota.grid(row=0, column=1, padx=5, pady=5)

# Nombre del propietario
Label(frame_form, text="Nombre del propietario:", bg="#F4F1EA",
      font=("Arial", 11)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
entrada_dueno = Entry(frame_form, width=30, font=("Arial", 11))
entrada_dueno.grid(row=1, column=1, padx=5, pady=5)

# Tipo de mascota
Label(frame_form, text="Tipo de mascota:", bg="#F4F1EA",
      font=("Arial", 11)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
combo_tipo = ttk.Combobox(frame_form, values=list(RECARGO_TIPO.keys()),
                          state="readonly", width=28)
combo_tipo.grid(row=2, column=1, padx=5, pady=5)

# Tamaño
Label(frame_form, text="Tamaño:", bg="#F4F1EA",
      font=("Arial", 11)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
combo_tamano = ttk.Combobox(frame_form, values=list(RECARGO_TAMANO.keys()),
                            state="readonly", width=28)
combo_tamano.grid(row=3, column=1, padx=5, pady=5)

# Servicio
Label(frame_form, text="Servicio:", bg="#F4F1EA",
      font=("Arial", 11)).grid(row=4, column=0, sticky="w", padx=5, pady=5)
combo_servicio = ttk.Combobox(frame_form, values=list(PRECIOS_BASE.keys()),
                              state="readonly", width=28)
combo_servicio.grid(row=4, column=1, padx=5, pady=5)

# Descuento (opcional, validado con try-except)
Label(frame_form, text="Descuento (%) [opcional]:", bg="#F4F1EA",
      font=("Arial", 11)).grid(row=5, column=0, sticky="w", padx=5, pady=5)
entrada_descuento = Entry(frame_form, width=30, font=("Arial", 11))
entrada_descuento.grid(row=5, column=1, padx=5, pady=5)

# Frame de botones
frame_botones = Frame(ventana, bg="#F4F1EA")
frame_botones.pack(pady=10)

btn_registrar = Button(frame_botones, text="Registrar servicio",
                       command=registrar_servicio,
                       bg="#8FBC8F", fg="white",
                       font=("Arial", 11, "bold"), width=18)
btn_registrar.grid(row=0, column=0, padx=5)

btn_resumen = Button(frame_botones, text="Ver resumen",
                     command=generar_resumen,
                     bg="#4682B4", fg="white",
                     font=("Arial", 11, "bold"), width=18)
btn_resumen.grid(row=0, column=1, padx=5)

btn_listado = Button(frame_botones, text="Ver listados",
                     command=mostrar_listado,
                     bg="#DAA520", fg="white",
                     font=("Arial", 11, "bold"), width=18)
btn_listado.grid(row=0, column=2, padx=5)

btn_limpiar = Button(frame_botones, text="Limpiar pantalla",
                     command=limpiar_resultados,
                     bg="#CD5C5C", fg="white",
                     font=("Arial", 11, "bold"), width=18)
btn_limpiar.grid(row=0, column=3, padx=5)

btn_reiniciar = Button(frame_botones, text="Borrar historial",
                       command=reiniciar_todo,
                       bg="#8B4513", fg="white",
                       font=("Arial", 11, "bold"), width=18)
btn_reiniciar.grid(row=1, column=0, columnspan=4, pady=6)

# Área de resultados (Text + Scrollbar)
frame_resultados = Frame(ventana)
frame_resultados.pack(pady=10, padx=20, fill="both", expand=True)

scroll = Scrollbar(frame_resultados)
scroll.pack(side=RIGHT, fill=Y)

area_resultados = Text(frame_resultados, height=15, width=80,
                       font=("Courier", 10), yscrollcommand=scroll.set,
                       bg="#FFFEF8", wrap="word",
                       state="disabled")   # ← SOLO LECTURA
area_resultados.pack(side=LEFT, fill="both", expand=True)
scroll.config(command=area_resultados.yview)

# Mensaje inicial
mostrar_mensaje_inicial()

ventana.mainloop()