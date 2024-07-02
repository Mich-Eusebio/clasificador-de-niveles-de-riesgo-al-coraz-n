import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

API_KEY = 'AIzaSyB9xdKYyGMjMgtf5-5-yTM76dcJvF9Bolc'

def main():
    
    
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox("Selecciona una página", ["Formulario", "Predicción"])

    if page == "Formulario":
        datos = mostrar_formulario()
        A = int(1)
        st.session_state.datos = datos
    elif page == "Predicción":
        if "datos" not in st.session_state:
            st.error("Por favor, completa el formulario primero.")
        else:
            ver_prediccion(st.session_state.datos)

def mostrar_formulario():
    st.title("Formulario de Datos Personales")

    st.write("Por favor, completa los siguientes campos con la información solicitada. Si no sabes la respuesta para algún campo, escribe 'no sé'.")
    edad = st.text_input("Edad")
    genero = st.selectbox("Género", ["", "Mujer", "Hombre"])
    altura_cm = st.text_input("Altura (en centímetros)")
    peso_kg = st.text_input("Peso (en kilogramos)")
    presion_sistolica = st.text_input("Presión Sistólica")
    presion_diastolica = st.text_input("Presión Diastólica")
    colesterol = st.selectbox("Nivel de Colesterol", ["", "Normal", "Sobre lo normal", "Muy sobre lo normal"])
    glucosa = st.selectbox("Nivel de Glucosa", ["", "Normal", "Sobre lo normal", "Muy sobre lo normal"])
    fuma = st.selectbox("¿Fuma?", ["No", "Sí"])
    alcohol = st.selectbox("¿Consume alcohol?", ["No", "Sí"])
    ejercicio = st.selectbox("¿Realiza ejercicio regularmente?", ["No", "Sí"])

    datos = {
        "Edad": edad,
        "Género": genero,
        "Altura": altura_cm,
        "Peso": peso_kg,
        "Presión Sistólica": presion_sistolica,
        "Presión Diastólica": presion_diastolica,
        "Nivel de Colesterol": colesterol,
        "Nivel de Glucosa": glucosa,
        "Fuma": fuma,
        "Consume alcohol": alcohol,
        "Ejercicio regular": ejercicio
    }
    A = None
    def send(datos):
        st.session_state.datos = datos
        A = int(1)
        return datos
    if st.button("Enviar"):
        for key, value in datos.items():
            if not value:
                st.error(f"Por favor, completa el campo '{key}'.")
                return datos
        with st.expander("Revisar Datos"):
            st.write("Por favor, revisa tus datos antes de enviarlos:")
            for key, value in datos.items():
                st.write(f"{key}: {value}")
            ##botón de confirmar verde
            if st.button("Confirmar"):
                A = send(datos)
        
        if datos != None and A == 1:
            st.success("Datos enviados correctamente.")
            return datos
    
            
            
            
        
        
        
    
    
    
    
    return datos

def consumir_api_prediccion(datos):
    print("Datos enviados a la API:", datos)
    #llamar a la api de gemini con prompt en español
    
    prompt = (f"Tomando en cuenta los datos ingresados {datos}, "
              f"Dame 3 sugerencias para mejorar mi salud cardiovascular.")
    
    load_dotenv()
    
   
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(prompt) 
    
    if response:
        return response.text
    elif response.status_code == 401:
        return "Error: API Key inválida. Por favor, revisa tu API Key."

def ver_prediccion(datos):
    st.title("Predicción Cardiaca")
    st.write("A continuación, se muestra la predicción de enfermedad cardiaca basada en los datos ingresados.")
    st.write("Por favor, ten en cuenta que esta predicción es solo una estimación y no reemplaza el diagnóstico de un profesional de la salud.")

    prediccion = consumir_api_prediccion(datos)
    st.write(prediccion)

if __name__ == "__main__":
    main()
