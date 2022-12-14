import streamlit as st

st.set_page_config(
    page_title="Tarea Semana 12",
    page_icon="馃憢",
)

st.write("# Despliegue web de modelos del Grupo G 馃")

st.sidebar.success("Seleccione un modelo del men煤")

st.markdown(
    """
    # Grupo G - Integrantes:
    | Nombre | Participaci贸n|
    |--|--|
    | Oscar Stalyn, Yanfer Laura | Regresi贸n l铆neal (RL) |
    | Diego Tharlez Montalvo Ortega | Support Vector Regression (SVR) |
    | Jorge Luis Quispe Alarcon | Twitter |
    | Wilker Edison,Atalaya Ramirez | M谩quinas de vectores de soporte (SVM) |
    | Anthony Elias,Ricse Perez | Red Neuronal Recurrente(RNN) |
    | Carlos Daniel Tarme帽o Noriega | K-Vecinos Cercanos(KNN) |
    | Nathaly Nicole Pichilingue Pimentel | M谩quinas de vectores de soporte(SVC) y Random Forest(RF) |
    | Jorge Luis, Marin Evangelista | Redes Neuronales Bayesianas (RNB) |

    ### Especificaciones:
    **Donde muestra las predicciones/los resultados:**
    - Gr谩ficamente. 
    - N煤mericamente los valores de las predicciones (print de dataframe con la predicci贸n o clasificaci贸n).
    
    **Donde se muestra el EDA:**
    - Ploteo de los precios reales.
    (Ploteo de media m贸vil los precios reales.)

    **Donde el usuario pueda indicar:**
    - El modelo ejecutar.
    - La acci贸n o instrumento financiero que quiera analizar.
"""
)
