import streamlit as st
from supabase import create_client, Client
from apify_client import ApifyClient
import time

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Prospectador IA", page_icon="🤖", layout="centered")

# --- CARGA DE SECRETOS (Nuestra caja fuerte personalizada) ---
@st.cache_resource
def cargar_secretos():
    url_publica = "TU_URL_DE_SUPABASE"  # Reemplaza con tu URL
    key_publica = "TU_LLAVE_ANON_DE_SUPABASE" # Reemplaza con tu llave anon
    try:
        supabase_para_secretos = create_client(url_publica, key_publica)
        response = supabase_para_secretos.table('configuracion').select('nombre_clave, valor_clave').execute()
        secretos = {item['nombre_clave']: item['valor_clave'] for item in response.data}
        return secretos
    except Exception as e:
        st.error(f"Error crítico: No se pudo cargar la configuración desde Supabase. {e}")
        return None

SECRETS = cargar_secretos()

# --- FUNCIONES DEL TRABAJADOR CAZADOR (La lógica que trajimos de Replit) ---
def ejecutar_mision_apify(apify_client, busqueda, ubicacion, limite):
    busqueda_completa = f"{busqueda} en {ubicacion}"
    run_input = {
        "searchStringsArray": [busqueda_completa],
        "maxCrawledPlacesPerSearch": limite,
        "language": "es"
    }
    try:
        run = apify_client.actor("compass/crawler-google-places").call(run_input=run_input)
        items = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
        return items
    except Exception as e:
        st.error(f"Error al contactar a Apify: {e}")
        return []

def guardar_prospectos(supabase_client, prospectos, id_campana):
    contador_guardados = 0
    st.write("💾 Guardando prospectos en la base de datos...")
    progress_bar = st.progress(0)
    
    for i, lugar in enumerate(prospectos):
        nuevo_prospecto = {
            'campana_id': id_campana, 'nombre_negocio': lugar.get('title'),
            'url_google_maps': lugar.get('url'), 'url_sitio_web': lugar.get('website'),
            'telefono': lugar.get('phone'), 'email_contacto': lugar.get('email'),
            'estado_prospecto': 'cazado'
        }
        try:
            supabase_client.table('prospectos').insert(nuevo_prospecto).execute()
            st.write(f"  -> ✅ Guardado: {nuevo_prospecto['nombre_negocio']}")
            contador_guardados += 1
        except Exception:
            st.write(f"  -> 🟡 Omitido (duplicado): {nuevo_prospecto['nombre_negocio']}")
        
        progress_bar.progress((i + 1) / len(prospectos))
    
    return contador_guardados

# --- INTERFAZ DE USUARIO (El Dashboard) ---
st.title("🤖 Panel de Control - Prospectador IA")
st.markdown("---")

if SECRETS:
    st.success("¡Configuración secreta cargada desde Supabase!")
    
    st.header("🚀 Crear Nueva Campaña en Google Maps")
    with st.form(key="campaign_form"):
        tipo_negocio = st.text_input("¿Qué tipo de negocio buscas?", placeholder="Ej: Abogados de familia")
        ciudad_pais = st.text_input("¿En qué ciudad y país?", placeholder="Ej: Bogotá, Colombia")
        cantidad_prospectos = st.number_input("¿Cuántos prospectos?", 10, 100, 20) # Limitamos a 100 para no agotar el plan gratuito
        submit_button = st.form_submit_button("🔎 Iniciar Búsqueda Real")

    if submit_button:
        if tipo_negocio and ciudad_pais:
            # ¡AQUÍ CONECTAMOS LOS CABLES!
            ID_CAMPANA_PRUEBA = 1
            
            with st.spinner(f"El Cazador está buscando '{tipo_negocio}' en '{ciudad_pais}'. Esto puede tardar varios minutos..."):
                # Inicializamos los clientes con las llaves cargadas
                supabase = create_client(SECRETS['SUPABASE_URL'], SECRETS['SUPABASE_KEY'])
                apify = ApifyClient(SECRETS['APIFY_KEY'])
                
                # Ejecutamos la misión
                resultados = ejecutar_mision_apify(apify, tipo_negocio, ciudad_pais, cantidad_prospectos)

            if resultados:
                # Si hay resultados, los guardamos
                total_guardados = guardar_prospectos(supabase, resultados, ID_CAMPANA_PRUEBA)
                st.success(f"¡Misión completada! Se han guardado {total_guardados} nuevos prospectos.")
                st.balloons()
            else:
                st.warning("La búsqueda no arrojó nuevos resultados.")
        else:
            st.error("Por favor, rellena todos los campos.")
else:
    st.error("Error crítico: La aplicación no puede funcionar sin la configuración de Supabase.")
