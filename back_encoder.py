# -*- coding: utf-8 -*-
"""back_encoder.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ub191RJTuidI7e0IRXTHuhJflTVhNm_e
"""




# cargar el modelo
import tensorflow as tf
autoencoder = tf.keras.models.load_model("autoencoder.h5")


## crear una función de predicción
def predecir(modelo, datos, umbral):
  reconstrucciones = modelo(datos)
  perdida = tf.keras.losses.mae(reconstrucciones, datos)
  return tf.math.less(perdida, umbral)

umbral= 0.1558244534054211