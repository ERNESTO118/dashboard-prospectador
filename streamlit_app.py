import streamlit as st
import json
from supabase import create_client

# --- CARGA DE SECRETOS ---
@st.cache_resource
def cargar_secretos():
    url_publica = "https://lgtihtfyndnfkbuwfbxo.supabase.co"
    key_publica = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxndGlodGZ5bmRuZmtidXdmYnhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU5OTg4MjIsImV4cCI6MjA3MTU3NDgyMn0.K4igC3AgVkrmO6EDJDY9L_T-etecDTEXpmKfPimUE-g"
    try:
        supabase_para_secretos = create_client(url_publica, key_publica)
        response = supabase_para_secretos.table('configuracion').select('nombre_clave, valor_clave').execute()
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
            # Usamos la librería 'supabase' original
            supabase = create_client(SECRETS['SUPABASE_URL'], SECRETS['SUPABASE_KEY'])
            
            nueva_campana = {
                'cliente_id': 1, 'nombre_campana': f"Campaña: {cliente_ideal}",
                'criterio_busqueda': json.dumps({
                    "que_vendes": que_vendes, "cliente_ideal": cliente_ideal,
                    "ubicacion": ciudad_pais, "cantidad": cantidad_prospectos
                }), 'estado_campana': 'pendiente'
            }
            
            supabase.table('campanas').insert(nueva_campana).execute()
            
            st.success("¡Campaña creada con éxito!")
            st.balloons()
        except Exception as e:
            st.error(f"Hubo un error al crear la campaña: {e}")
else:
    st.error("Error crítico: La aplicación no puede funcionar.")
