import streamlit as st
import json
from supabase import create_client

# --- FUNCIÓN DE CARGA DE SECRETOS CON "LOGS" DETALLADOS ---
@st.cache_resource
def cargar_secretos():
    st.info("Iniciando la carga de secretos...")
    try:
        # Estas son las llaves públicas para LEER la tabla de configuración
        url_publica = "https://lgtihtfyndnfkbuwfbxo.supabase.co"
        key_publica = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxndGlodGZ5bmRuZmtidXdmYnhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU5OTg4MjIsImV4cCI6MjA3MTU3NDgyMn0.K4igC3AgVkrmO6EDJDY9L_T-etecDTEXpmKfPimUE-g"
        
        st.write(f"1. URL pública para leer secretos: {url_publica}")
        st.write(f"2. Key pública para leer secretos: ...{key_publica[-5:]}") # Mostramos solo los últimos 5 caracteres
        
        supabase_para_secretos = create_client(url_publica, key_publica)
        st.write("3. Cliente de Supabase para leer secretos CREADO.")
        
        response = supabase_para_secretos.table('configuracion').select('nombre_clave, valor_clave').execute()
        st.write("4. Se ejecutó la consulta a la tabla 'configuracion'.")
        
        secretos = {item['nombre_clave']: item['valor_clave'] for item in response.data}
        st.success("¡Configuración secreta cargada desde Supabase!")
        st.write("Secretos cargados:", secretos.keys()) # Mostramos qué llaves se cargaron
        return secretos
    except Exception as e:
        st.error(f"Error crítico durante la carga de secretos: {e}")
        return None

SECRETS = cargar_secretos()

# --- INTERFAZ DE USUARIO ---
st.title("🤖 Panel de Control - Modo Depuración")

if SECRETS:
    with st.form(key="campaign_form"):
        # ... (campos del formulario como antes) ...
        que_vendes = st.text_input("1. ¿Qué producto o servicio vendes?")
        cliente_ideal = st.text_input("2. ¿Cuál es tu cliente ideal?")
        ciudad_pais = st.text_input("3. ¿En qué ciudad y país quieres buscar?")
        cantidad_prospectos = st.number_input("4. ¿Cuántos prospectos quieres encontrar?", 10, 500, 50)
        submit_button = st.form_submit_button("✅ Lanzar Campaña")

    if submit_button:
        try:
            st.info("Botón presionado. Intentando escribir en la base de datos...")
            
            url_escritura = SECRETS['SUPABASE_URL']
            key_escritura = SECRETS['SUPABASE_KEY']
            
            st.write(f"5. URL para escribir leída de la config: {url_escritura}")
            st.write(f"6. Key para escribir leída de la config: ...{key_escritura[-5:]}")
            
            supabase_escritura = create_client(url_escritura, key_escritura)
            st.write("7. Cliente de Supabase para escribir CREADO.")
            
            nueva_campana = {
                'cliente_id': 1, 'nombre_campana': "Prueba de Depuración",
                'criterio_busqueda': json.dumps({"test": "data"}),
                'estado_campana': 'pendiente'
            }
            
            supabase_escritura.table('campanas').insert(nueva_campana).execute()
            st.success("¡ÉXITO! La campaña se escribió en la base de datos.")
            st.balloons()
            
        except Exception as e:
            st.error(f"Hubo un error al crear la campaña: {e}")
else:
    st.error("Error crítico: La aplicación no puede funcionar.")
