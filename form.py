import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Cargar el modelo
clf = joblib.load("random_forest.pkl")
#joblib.dump(clf, "random_forest.pkl", protocol=2)


# Cargar el dataset y calcular las estadísticas (medias y desviaciones estándar)
df = pd.read_csv("cardio_train_normalizado.csv")
mean = {
    'age': df['age'].mean(), 'gender': df['gender'].mean(), 'height': df['height'].mean(), 'weight': df['weight'].mean(),
    'ap_hi': df['ap_hi'].mean(), 'ap_lo': df['ap_lo'].mean(), 'cholesterol': df['cholesterol'].mean(), 'gluc': df['gluc'].mean(),
    'smoke': df['smoke'].mean(), 'alco': df['alco'].mean(), 'active': df['active'].mean()
}
std = {
    'age': df['age'].std(), 'gender': df['gender'].std(), 'height': df['height'].std(), 'weight': df['weight'].std(),
    'ap_hi': df['ap_hi'].std(), 'ap_lo': df['ap_lo'].std(), 'cholesterol': df['cholesterol'].std(), 'gluc': df['gluc'].std(),
    'smoke': df['smoke'].std(), 'alco': df['alco'].std(), 'active': df['active'].std()
}

# Función para obtener la presión arterial promedio
def get_blod_pressure(gender, age):
    filtered_df = df[(df["gender"] == gender)]
    if age < 40:
        filtered_df = filtered_df[(filtered_df["age"] < 40)]
    elif 40 <= age <= 60:
        filtered_df = filtered_df[(filtered_df["age"] >= 40) & (filtered_df["age"] <= 60)]
    else:
        filtered_df = filtered_df[(filtered_df["age"] > 60)]

    mean_ap_hi = round(filtered_df["ap_hi"].mean())
    mean_ap_lo = round(filtered_df["ap_lo"].mean())

    return [mean_ap_hi, mean_ap_lo]

# Función para normalizar los datos del usuario
def normalize_user_data(user_data):
    """
    Normaliza los datos del usuario basados en las medias y desviaciones estándar del conjunto de entrenamiento.
    
    Parameters:
    user_data (dict): Diccionario con los datos del usuario.

    Returns:
    list: Lista de datos normalizados.
    """
    normalized_data = []
    for key in mean.keys():
        if user_data[key] == 'nosé':
            if key in ['ap_hi', 'ap_lo']:
                gender = user_data['gender']
                age = user_data['age']
                user_data['ap_hi'], user_data['ap_lo'] = get_blod_pressure(gender, age)
            else:
                user_data[key] = mean[key]

        normalized_value = (user_data[key] - mean[key]) / std[key]
        normalized_data.append(normalized_value)

    return [normalized_data]

# Función para realizar la predicción
def user_predict(data):
    prediccion = clf.predict(data)
    if prediccion[0] == 0:
        return "¡Felicidades, usted No tiene riesgo de un ataque al corazón!"
    else:
        return "¡Tiene riesgo de un ataque cardíaco, visite su médico!"

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
        genero_val = 2
    elif genero == "Hombre":
        genero_val = 1
    else:
        genero_val = None
    
    altura_cm = st.text_input("Altura (en centímetros)")
    peso_kg = st.text_input("Peso (en kilogramos)")
    
    presion_sistolica = st.text_input("Presión Sistólica")
    presion_diastolica = st.text_input("Presión Diastólica")
    
    colesterol = st.selectbox("Nivel de Colesterol", ["", "Normal", "Sobre lo normal", "Muy sobre lo normal"])
    if colesterol == "Normal":
        colesterol_val = 1
    elif colesterol == "Sobre lo normal":
        colesterol_val = 2
    elif colesterol == "Muy sobre lo normal":
        colesterol_val = 3
    else:
        colesterol_val = None
    
    glucosa = st.selectbox("Nivel de Glucosa", ["", "Normal", "Sobre lo normal", "Muy sobre lo normal"])
    if glucosa == "Normal":
        glucosa_val = 1
    elif glucosa == "Sobre lo normal":
        glucosa_val = 2
    elif glucosa == "Muy sobre lo normal":
        glucosa_val = 3
    else:
        glucosa_val = None
    
    fuma = st.selectbox("¿Fuma?", ["No", "Sí"])
    fuma_val = 1 if fuma == "Sí" else 0
    
    alcohol = st.selectbox("¿Consume alcohol?", ["No", "Sí"])
    alcohol_val = 1 if alcohol == "Sí" else 0
    
    ejercicio = st.selectbox("¿Realiza ejercicio regularmente?", ["No", "Sí"])
    ejercicio_val = 1 if ejercicio == "Sí" else 0
    
    if st.button("Revisar Datos"):
        datos = {
            "age": edad,
            "gender": genero_val,
            "height": altura_cm if altura_cm.lower() != 'no sé' else 'nosé',
            "weight": peso_kg if peso_kg.lower() != 'no sé' else 'nosé',
            "ap_hi": presion_sistolica if presion_sistolica.lower() != 'no sé' else 'nosé',
            "ap_lo": presion_diastolica if presion_diastolica.lower() != 'no sé' else 'nosé',
            "cholesterol": colesterol_val,
            "gluc": glucosa_val,
            "smoke": fuma_val,
            "alco": alcohol_val,
            "active": ejercicio_val
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
        normalized_data = normalize_user_data(datos)
        resultado = user_predict(normalized_data)
        
        st.write("Resultado del modelo: ", resultado)
    else:
        st.write("No se han enviado datos aún, por favor, completa el formulario.")

if __name__ == "__main__":
    main()
