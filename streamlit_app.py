import streamlit as st
import json
from postgrest import PostgrestClient # ¡CORRECCIÓN!
import os

# --- CARGA DE SECRETOS (Simplificado) ---
@st.cache_resource
def cargar_secretos():
    url_publica = "https://lgtihtfyndnfkbuwfbxo.supabase.co"
    key_publica = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxndGlodGZ5bmRuZmtidXdmYnhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU5OTg4MjIsImV4cCI6MjA3MTU3NDgyMn0.K4igC3AgVkrmO6EDJDY9L_T-etecDTEXpmKfPimUE-g"
    try:
        # Usamos Postgrest para leer la configuración
        with PostgrestClient(base_url=url_publica, headers={"apikey": key_publica}) as client: # ¡CORRECCIÓN!
            response = client.from_("configuracion").select("nombre_clave, valor_clave").execute()
        secretos = {item['nombre_clave']: item['valor_clave'] for item in response.data}
        return secretos
    except Exception as e:
        st.error(f"Error crítico al cargar configuración: {e}")
        return None

SECRETS = cargar_secretos()

# --- INTERFAZ DE USUARIO ---
st.title("🤖 Panel de Control - Prospectador IA")

if SECRETS:
    st.success("¡Configuración secreta cargada!")
    
    with st.form(key="campaign_form"):
        que_vendes = st.text_input("1. ¿Qué producto o servicio vendes?")
        cliente_ideal = st.text_input("2. ¿Cuál es tu cliente ideal?")
        ciudad_pais = st.text_input("3. ¿En qué ciudad y país quieres buscar?")
        cantidad_prospectos = st.number_input("4. ¿Cuántos prospectos?", 10, 500, 50)
        submit_button = st.form_submit_button("✅ Lanzar Campaña")

    if submit_button:
        try:
            # Usamos Postgrest para escribir la campaña
            with PostgrestClient(base_url=SECRETS['SUPABASE_URL'], headers={"apikey": SECRETS['SUPABASE_KEY']}) as client: # ¡CORRECCIÓN!
                nueva_campana = {
                    'cliente_id': 1, 'nombre_campana': f"Campaña: {cliente_ideal}",
                    'criterio_busqueda': json.dumps({
                        "que_vendes": que_vendes, "cliente_ideal": cliente_ideal,
                        "ubicacion": ciudad_pais, "cantidad": cantidad_prospectos
                    }), 'estado_campana': 'pendiente'
                }
                client.from_("campanas").insert(nueva_campana).execute()
            
            st.success("¡Campaña creada con éxito!")
            st.balloons()
        except Exception as e:
            st.error(f"Hubo un error al crear la campaña: {e}")
else:
    st.error("Error crítico: La aplicación no puede funcionar.")
