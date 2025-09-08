import streamlit as st
import requests

URL_ORQUESTADOR = "https://orquestador-production.up.railway.app/crear-campana"

st.title("🤖 Panel de Control - Prospectador IA")
st.markdown("---")

with st.form(key="campaign_form"):
    que_vendes = st.text_input("1. ¿Qué producto o servicio vendes?")
    cliente_ideal = st.text_input("2. ¿Cuál es tu cliente ideal?")
    ciudad_pais = st.text_input("3. ¿En qué ciudad y país quieres buscar?")
    cantidad_prospectos = st.number_input("4. ¿Cuántos prospectos?", 10, 500, 50)
    submit_button = st.form_submit_button("✅ Lanzar Campaña")

if submit_button:
    if que_vendes and cliente_ideal and ciudad_pais:
        with st.spinner("Enviando orden al Orquestador..."):
            try:
                datos_para_orquestador = {
                    "que_vendes": que_vendes, "cliente_ideal": cliente_ideal,
                    "ubicacion": ciudad_pais, "cantidad": cantidad_prospectos
                }
                response = requests.post(URL_ORQUESTADOR, json=datos_para_orquestador)
                
                if response.status_code == 200:
                    st.success("¡Campaña Iniciada! El Orquestador ha recibido tu orden.")
                    st.balloons()
                else:
                    st.error(f"El Orquestador respondió con un error: {response.text}")
            except Exception as e:
                st.error(f"No se pudo conectar con el Orquestador: {e}")
    else:
        st.error("Por favor, rellena todos los campos.")
