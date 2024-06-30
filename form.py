import streamlit as st

def main():
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox("Selecciona una página", ["Formulario", "Predicción"])

    if page == "Formulario":
        mostrar_formulario()
    elif page == "Predicción":
        ver_prediccion()

def mostrar_formulario():
    st.title("Formulario de Datos Personales")

    st.write("Por favor, completa los siguientes campos con la información solicitada. Si no sabes la respuesta para algún campo, escribe 'no sé'.")

    edad = st.number_input("Edad", min_value=1, max_value=120, step=1)
    
    genero = st.selectbox("Género", ["", "Mujer", "Hombre"])
    if genero == "Mujer":
        genero_val = "Mujer"
    elif genero == "Hombre":
        genero_val = "Hombre"
    else:
        genero_val = None
    
    altura_cm = st.text_input("Altura (en centímetros)")
    peso_kg = st.text_input("Peso (en kilogramos)")
    
    presion_sistolica = st.text_input("Presión Sistólica")
    presion_diastolica = st.text_input("Presión Diastólica")
    
    colesterol = st.selectbox("Nivel de Colesterol", ["", "Normal", "Sobre lo normal", "Muy sobre lo normal"])
    if colesterol == "Normal":
        colesterol_val = "Normal"
    elif colesterol == "Sobre lo normal":
        colesterol_val = "Sobre lo normal"
    elif colesterol == "Muy sobre lo normal":
        colesterol_val = "Muy sobre lo normal"
    else:
        colesterol_val = None
    
    glucosa = st.selectbox("Nivel de Glucosa", ["", "Normal", "Sobre lo normal", "Muy sobre lo normal"])
    if glucosa == "Normal":
        glucosa_val = "Normal"
    elif glucosa == "Sobre lo normal":
        glucosa_val = "Sobre lo normal"
    elif glucosa == "Muy sobre lo normal":
        glucosa_val = "Muy sobre lo normal"
    else:
        glucosa_val = None
    
    fuma = st.selectbox("¿Fuma?", ["No", "Sí"])
    fuma_val = "Sí" if fuma == "Sí" else "No"
    
    alcohol = st.selectbox("¿Consume alcohol?", ["No", "Sí"])
    alcohol_val = "Sí" if alcohol == "Sí" else "No"
    
    ejercicio = st.selectbox("¿Realiza ejercicio regularmente?", ["No", "Sí"])
    ejercicio_val = "Sí" if ejercicio == "Sí" else "No"
    
    if st.button("Revisar Datos"):
        datos = {
            "Edad": edad,
            "Género": genero_val,
            "Altura": altura_cm,
            "Peso": peso_kg,
            "Presión Sistólica": presion_sistolica,
            "Presión Diastólica": presion_diastolica,
            "Nivel de Colesterol": colesterol_val,
            "Nivel de Glucosa": glucosa_val,
            "Fuma": fuma_val,
            "Consume alcohol": alcohol_val,
            "Ejercicio regular": ejercicio_val
        }
        
        with st.expander("Revisar Datos"):
            st.write("Por favor, revisa tus datos antes de enviarlos:")
            for key, value in datos.items():
                st.write(f"{key}: {value}")

            if st.button("Confirmar y Enviar", key="confirmar_enviar"):
                st.session_state.datos = datos
                st.write("Datos enviados con éxito.")
                st.sidebar.button("Ver Predicción", on_click=ver_prediccion)

def ver_prediccion():
    if "datos" in st.session_state:
        st.title("Resultados de la Predicción")
        st.write("Aquí se mostrarán los resultados del modelo de predicción basados en los datos ingresados.")
        
        datos = st.session_state.datos
        for key, value in datos.items():
            st.write(f"{key}: {value}")
            
        st.write("Resultado del modelo: [AQUÍ EL RESULTADO]")
    else:
        st.write("No se han enviado datos aún, Michael, actua...")

if __name__ == "__main__":
    main()