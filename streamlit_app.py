import streamlit as st
from supabase import create_client, Client
from apify_client import ApifyClient

# --- FUNCIÓN PARA CARGAR LAS LLAVES DESDE SUPABASE ---
# Esta es nuestra propia versión de los "Secrets".
@st.cache_resource
def cargar_secretos():
    # Estas dos llaves las ponemos aquí porque son necesarias para leer las demás.
    # Son las credenciales de "solo lectura", de bajo riesgo.
    url_publica = "https://lgtihtfyndnfkbuwfbxo.supabase.co"
    key_publica = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxndGlodGZ5bmRuZmtidXdmYnhvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU5OTg4MjIsImV4cCI6MjA3MTU3NDgyMn0.K4igC3AgVkrmO6EDJDY9L_T-etecDTEXpmKfPimUE-g"
    
    try:
        supabase_para_secretos = create_client(url_publica, key_publica)
        response = supabase_para_secretos.table('configuracion').select('nombre_clave, valor_clave').execute()
        
        secretos = {item['nombre_clave']: item['valor_clave'] for item in response.data}
        st.success("¡Configuración secreta cargada desde Supabase!")
        return secretos
    except Exception as e:
        st.error(f"No se pudo cargar la configuración desde Supabase: {e}")
        return None

# --- CARGAMOS LOS SECRETOS AL INICIAR LA APP ---
SECRETS = cargar_secretos()

# --- CUERPO PRINCIPAL DE LA APLICACIÓN ---
st.title("🤖 Panel de Control - Prospectador IA (v2)")

if SECRETS: # Solo mostramos el formulario si los secretos se cargaron bien
    with st.form(key="campaign_form"):
        tipo_negocio = st.text_input("¿Qué tipo de negocio buscas?")
        ciudad_pais = st.text_input("¿En qué ciudad y país?")
        cantidad_prospectos = st.number_input("¿Cuántos prospectos?", 10, 500, 50)
        submit_button = st.form_submit_button("🔎 Iniciar Búsqueda")

    if submit_button:
        if tipo_negocio and ciudad_pais:
            st.info("Orden recibida. Misión en curso...")
            
            # --- Aquí irá la lógica para llamar al Cazador ---
            # Por ahora, solo mostramos que hemos recibido la orden y los secretos.
            st.write(f"Misión: Buscar {cantidad_prospectos} '{tipo_negocio}' en '{ciudad_pais}'.")
            
            # Verificamos que hemos leído la API_KEY correctamente
            if 'APIFY_KEY' in SECRETS:
                st.success("La llave de Apify se ha cargado correctamente.")
            else:
                st.error("No se encontró la llave de Apify en la configuración.")
                
        else:
            st.error("Por favor, rellena el tipo de negocio y la ciudad.")
else:
    st.error("La aplicación no puede funcionar sin cargar la configuración.")
