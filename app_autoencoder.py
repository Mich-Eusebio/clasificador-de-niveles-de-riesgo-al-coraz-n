import streamlit as st
from pandas import DataFrame
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import back #modulo con algunas funciones necesarias
import back_encoder


#Esta es una función creada por Axel la cual hace que La IA de google genere sugerencias de salud de acuerdo a los datos del usuario
# Michael retocó el prompt

# Importar la librería de gemini, (inteligencia generativa de google)
import google.generativeai as genai

# obtener la clave api, (es gratuita).
API_KEY = 'AIzaSyB9xdKYyGMjMgtf5-5-yTM76dcJvF9Bolc'

# función para obtener su respuesta
def consumir_api_prediccion(datos):
    print("Datos enviados a la API:", datos)
    #llamar a la api de gemini con prompt en español
    
    prompt = (f"Tomando en cuenta los datos ingresados {datos}, "
              f"Dame 3 sugerencias para mejorar mi salud cardiovascular."
              f"Nota la data está tratada, o sea que para el género 1 es mujer, 2 es hombre; el colesterol va del 1 al 3, y esto representa normal, sobre lo normal y extremadamente sobre lo normal; lo mismo del colesterol se aplica para la glucosa; y finalmente para las variables de fumar, alcohol y ejercicio, 0 significa no, y 1 representa sí")

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(prompt) 
    
    if response:
        return response.text
    elif response.status_code == 401:
        return "Error: No sé pudieron geneerar las sugerencias de Gemini"



# traer el modelo Randon Forest
autoencoder = back_encoder.autoencoder



# traer el dataframe reducido con solo edad, genero y tipos de presión
df = back.df

# procesar la data del usuario
def process_data(data_user):
    promedio_presiones = back.get_blod_pressure(data_user[1], data_user[0])
    while "No sé" in data_user:
        if data_user[4] == "No sé":
            data_user[4] = promedio_presiones[0]
        elif data_user[5] == "No sé":
            data_user[5] = promedio_presiones[1]
    
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data_user)
    scaled_data = scaled_data.T
    return scaled_data

def user_prediction(data_user):
    umbral = back_encoder.umbral
    prediction = back_encoder.predecir(autoencoder, data_user, umbral)
    prediction = prediction.np()
    return prediction




def main():
    st.sidebar.title("Navegación")
    page = st.sidebar.selectbox("Selecciona una página", ["Formulario", "Predicción", "Conversor de unidades"])

    if page == "Formulario":
        mostrar_formulario()
    elif page == "Predicción":
        ver_prediccion()
    elif page == "Conversor de unidades":
        conversor()

def mostrar_formulario():
    st.title("¡Clarc tiene un par de preguntas para tí!")

    st.write("""
Por favor, completa los siguientes campos con la información solicitada y así Clarc hará su predicción 🔮.\n
• Si no sabes la respuesta para las unidades de conversión, puedes usar nuestro conversor 📏, solo expande la barra lateral.\n
• En caso de que no conozcas tu presión sistólica o diastólica, solo escribe “No sé” 🤷.

❕Vamos, Clarc se muere por saber tu salud 💓❕
""")


    edad = st.number_input("Edad", min_value=1, max_value=120, step=1)
    
    genero = st.selectbox("Género", ["", "Mujer", "Hombre"])
    if genero == "Mujer":
        genero_val = 2
    elif genero == "Hombre":
        genero_val = 1
    else:
        genero_val = None
    
    altura_cm = st.number_input("Altura (en centímetros)", value=160)
    peso_kg = st.number_input("Peso (en kilogramos)", value=75)

    presion_sistolica = st.text_input("Presión Sistólica")
    presion_diastolica = st.text_input("Presión Diastólica")
    try:
        presion_sistolica = int(presion_sistolica)
        presion_diastolica = int(presion_diastolica)
    except ValueError:
        presion_sistolica, presion_diastolica = "No sé", "No sé"

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

    datos = {
        "age": edad,
        "gender": genero_val,
        "height": altura_cm,
        "weight": peso_kg,
        "ap_hi": presion_sistolica,
        "ap_lo": presion_diastolica,
        "cholesterol": colesterol_val,
        "gluc": glucosa_val,
        "smoke": fuma_val,
        "alco": alcohol_val,
        "active": ejercicio_val
        }
    if st.button("enviar"):
        st.session_state["datos"] = datos
        st.write("Datos enviados correctamente")
        st.write("Expanda la barra lateral y haga clic en \"Predicción\" para que vea su resultado")
        






def ver_prediccion():
    if "datos" in st.session_state:
        st.title("Resultados de la Predicción")
        st.write("Clarck dice que...🤞")
        
        datos = st.session_state.datos
        datos = list(datos.values())
        normalized_data = process_data(datos)
        st.write(str(type(normalized_data)))
        resultado = user_prediction(normalized_data)
        
        st.write("\n", resultado)

# implementar la función de Axel al front
        st.header("Sugerencias de Gemini")
        st.write(consumir_api_prediccion(st.session_state.datos))

#poner una advertencia sobre nuestro modelo Clarc
        st.header("¡Atensión!")
        st.write("Hasta ahora, 5/7/2024, Clarc cuenta con una presición de un 73.62%. No recomendamos tomar el resultado como verdad absoluta. Sin embargo, estamos trabajando en robustecer nuestro modelo. \n\n ¡GRACIAS POR PROBAR CLARC!")

# Mostrar mensaje si el usuario no llena el formulario
    else:
        st.write("No se han enviado datos aún, por favor, completa el formulario.")

def conversor():
# Encabezado principal
    st.title("Conversor de Unidades")

    # Convertidor de pies a centímetros
    st.header("Convertidor de Pies a Centímetros")
    feet = st.number_input("Ingrese la cantidad en pies:", min_value=0.0, format="%.2f")
    cm = feet * 30.48
    st.write(f"{feet} pies son {cm:.2f} centímetros")

    # Convertidor de libras a kilogramos
    st.header("Convertidor de Libras a Kilogramos")
    lbs = st.number_input("Ingrese la cantidad en libras:", min_value=0.0, format="%.2f")
    kg = lbs * 0.453592
    st.write(f"{lbs} libras son {kg:.2f} kilogramos")


if __name__ == "__main__":
    main()

