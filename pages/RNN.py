# -*- coding: utf-8 -*-
"""redes-neuronales-recurrentes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cLLgQVTNdQwbPmIwyYsetH7zft4s_o1D

# Redes Neuronales Recurrentes
 es un tipo de modelo de redes neuronales que procesa secuencias de datos. Las RNN tienen una estructura en la que las salidas de algunas neuronas
  se vuelven a utilizar como entradas en otras neuronas en la misma red, permitiendo que la red tenga una memoria temporal y procese secuencias de 
  datos de manera efectiva. Esto las hace adecuadas para tareas como el procesamiento del lenguaje natural, la predicción de series temporales y otras
   tareas que involucren secuencias de datos. Los modelos RNN se pueden implementar utilizando diferentes tipos de celdas recurrentes, como las celdas
    LSTM y GRU, que tienen una mayor capacidad de memoria y pueden mejorar la capacidad de la red para procesar secuencias de datos a largo plazo. 

#### Fuente de la replicación:
- https://www.sciencedirect.com/science/article/abs/pii/S0893608021000356  


## Implementación

La inferencia variacional de los parámetros de la red neuronal ahora se demuestra en un problema de regresión simple. Por lo tanto se hará uso de una distribución Gaussiana.
"""
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import warnings
import streamlit as st
from math import sqrt
# To plot
plt.style.use('seaborn-darkgrid')

# To ignore warnings
warnings.filterwarnings("ignore")


st.set_page_config(page_title="RNN", page_icon="📈",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("# PEN")
st.sidebar.header("PEN")
st.markdown(
    """
    # Redes Neuronales Recurrentes
    es un tipo de modelo de redes neuronales que procesa secuencias de datos. Las RNN tienen una estructura en la que las salidas de algunas neuronas
    se vuelven a utilizar como entradas en otras neuronas en la misma red, permitiendo que la red tenga una memoria temporal y procese secuencias de 
    datos de manera efectiva. Esto las hace adecuadas para tareas como el procesamiento del lenguaje natural, la predicción de series temporales y otras
    tareas que involucren secuencias de datos. Los modelos RNN se pueden implementar utilizando diferentes tipos de celdas recurrentes, como las celdas
    LSTM y GRU, que tienen una mayor capacidad de memoria y pueden mejorar la capacidad de la red para procesar secuencias de datos a largo plazo. 
    """
)

ticker = st.text_input('Etiqueta de cotización', 'PEN')
st.write('La etiqueta de cotización actual es', ticker)

tic = yf.Ticker(ticker)
hist = tic.history(period="max", auto_adjust=True)

st.write("date time")
testdf = yf.download("PEN", start="2022-03-31",
                     end=dt.datetime.now(), progress=False)
testdf

st.write("Realizar la preparación de datos de RNN model entrenamiento ")
training_set = hist.iloc[:, 1:2].values
training_set
