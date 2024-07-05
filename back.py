#!/usr/bin/env python
# coding: utf-8

# In[ ]:






# In[ ]:


# cargar el modelo

import joblib

clf = joblib.load("random_forest.pkl")


# In[ ]:


# función parausar el promedio en caso de que el paciente no sepa su presión arterial

# realizé una investigación para agrupar por edades:
#si la edad es menor que 40, es jovén
#entre 41 y 60, es adulto medio
#mayor a 60 es viejo

# Este script es para cuando el usario no sabe de cuanto es el nivel de su presión arterial
# # se calcula el promedio de la presión en el dataset, basado en estas variables

import pandas as pd

df = pd.read_csv("cardio_train_normalizado.csv")
# extraer las edades, género y los tipos de presión arterial
df = df.filter(items=["age", "gender", "ap_hi", "ap_lo"])

def get_blod_pressure(gender, age):
  global df
  df = df[(df["gender"] == gender)]
  if 40 > age:
    df = df[(df["age"] < 40)]
    mean_ap_hi = round(df["ap_hi"].mean())
    mean_ap_lo = round(df["ap_lo"].mean())
    return [mean_ap_hi, mean_ap_lo]
  elif 40 < age < 61:
    df = df[(df["age"] > 40) & (df["age"] < 61)]
    mean_ap_hi = round(df["ap_hi"].mean())
    mean_ap_lo = round(df["ap_lo"].mean())
    return [mean_ap_hi, mean_ap_lo]
  else:
    df = df[(df["age"] >= 61)]
    mean_ap_hi = round(df["ap_hi"].mean())
    mean_ap_lo = round(df["ap_lo"].mean())
    return [mean_ap_hi, mean_ap_lo]


# In[ ]:


# función para tomar la data del usuario y devolver la predicción
#Nota la data del usuario debe estar  en una lista

def user_predict(data):
  prediccion = clf.predict(data)
  if prediccion[0] == 0:
    return "¡Felicidades, usted No tiene riesgo de un ataque al corazón!"
  else:
    return "¡Tiene riesgo de un ataque cardíaco, visite su médico!"



