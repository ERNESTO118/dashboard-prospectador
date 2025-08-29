import streamlit as st
import time

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Prospectador IA",
    page_icon="🤖",
    layout="centered"
)

# --- Título Principal ---
st.title("🤖 Panel de Control - Prospectador IA")
st.markdown("---")

# --- Formulario para Crear Campaña ---
st.header("🚀 Crear Nueva Campaña en Google Maps")
st.write("Rellena los siguientes campos para que nuestro Cazador se ponga a trabajar.")

# Usamos un formulario para agrupar los inputs y el botón
with st.form(key="campaign_form"):
    # Campo 1: ¿Qué negocio? (El cuestionario del cliente)
    tipo_negocio = st.text_input(
        label="¿Qué tipo de negocio buscas?",
        placeholder="Ej: Restaurantes veganos, talleres mecánicos..."
    )

    # Campo 2: ¿Dónde?
    ciudad_pais = st.text_input(
        label="¿En qué ciudad y país?",
        placeholder="Ej: Lima, Perú; Madrid, España..."
    )

    # Campo 3: ¿Cuántos?
    cantidad_prospectos = st.number_input(
        label="¿Cuántos prospectos quieres encontrar? (Máx. 500)",
        min_value=10,
        max_value=500,
        value=50, # Valor por defecto
        step=10
    )

    # Botón de envío del formulario
    submit_button = st.form_submit_button(label="🔎 Iniciar Búsqueda")

# --- Lógica que se ejecuta al presionar el botón ---
if submit_button:
    # Verificamos que los campos importantes estén llenos
    if tipo_negocio and ciudad_pais:
        st.success(f"¡Orden recibida! El Cazador ha sido enviado.")
        
        # Mostramos un resumen de la misión para el cliente
        with st.expander("Ver detalles de la misión"):
            st.write(f"**Objetivo:** {tipo_negocio}")
            st.write(f"**Ubicación:** {ciudad_pais}")
            st.write(f"**Límite:** {cantidad_prospectos} prospectos")

        # Simulamos que el sistema está trabajando (en el futuro, esto llamará al Orquestador)
        with st.spinner("El Orquestador está asignando la tarea al Cazador..."):
            time.sleep(3) # Simulamos una espera de 3 segundos
        
        st.info("¡El Cazador ya está en el campo! Te notificaremos cuando la misión haya finalizado.")
        st.balloons()

    else:
        # Si faltan datos, mostramos un error
        st.error("Por favor, rellena al menos el tipo de negocio y la ciudad.")
