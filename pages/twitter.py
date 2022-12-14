import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud, STOPWORDS
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import snscrape.modules.twitter as sntwitter
import nltk
import warnings
import streamlit as st

st.set_page_config(page_title="Twitter")

st.markdown("# Análisis de sentimiento (Twitter)")
st.sidebar.header("Twitter")
st.write(
    """En esta sección podras realizar un análisis de sentimientos de la cuenta de Twitter de tu preferencia, se seleccionarán 300 tweets para la evaluación."""
)

ticker = st.text_input('Usuario en inglés a buscar:', 'PopBase')
st.write('El usuario actual es:', ticker)

# Creamos una lista donde guardaremos atributos de c/tweet (datos)
attributes_container = []

# Usamos TwitterSearchScraper para realizar scrapping y obtener los tweets, estamos seleccionando los útlimos 300 tweets
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:'+ticker).get_items()):
    if i>300:
        break
    attributes_container.append([tweet.date, tweet.likeCount, tweet.sourceLabel, tweet.content])
    
# Creamos un dataframe para la lista de tweets obtenidos en el paso anterior
tweets_df = pd.DataFrame(attributes_container, columns=["Date Created", "Number of Likes", "Source of Tweet", "Tweets"])
st.write("Observamos el dataframe creado")
tweets_df

# Creamos una función que limpie el texto de cada tweet
def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9]+', '', text) #Remueve @menciones
    text = re.sub('#', '', text) # Remueve '#' hash tag
    text = re.sub('RT[\s]+', '', text) # Remueve RT (retuiteado)
    text = re.sub('https?:\/\/\S+', '', text) # Remueve hipervínculos
    return text

#Aplicamos esta función a la columna "Tweets" de nuestro dataframe
tweets_df["Tweets"] = tweets_df["Tweets"].apply(cleanTxt)

st.write("Dataframe luego de la limpieza de datos")
#Veamos nuevamente el dataframe
tweets_df

#Verifiquemos que tengamos la misma cantidad de info en todas las columnas
tweets_df.info()

#Obtenemos solo los tweets
only_tweets = tweets_df.iloc[:, 3].values

st.write("Visualizamos solo los tweets")
#Asignamos esa lista de tweets a un dataframe
tweets_t = pd.DataFrame({'Tweets': only_tweets})
tweets_t

nltk.download('vader_lexicon')
# Iniciamos el SentimentIntensityAnalyzer.
vader = SentimentIntensityAnalyzer()

st.write("Análisis de sentimiento")
# Apply lambda function to get compound scores. Aplicamos una función lambda para obtener el puntaje compuesto
function = lambda texto: vader.polarity_scores(texto)['compound']
tweets_t['compound'] = tweets_t['Tweets'].apply(function)
tweets_t

# Realizamos su visualización en un WordCloud
import seaborn as sns

allWords = ' '.join([twts for twts in tweets_t['Tweets']])
wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
st.write("Visualización en un WordCloud")
fig1 = plt.figure()
plt.imshow(wordCloud, interpolation="bilinear")
plt.axis('off')
st.pyplot(fig1)

def getAnalysis(score):
 if score < 0:
    return 'Negative'
 elif score == 0:
    return 'Neutral'
 else:
    return 'Positive'

tweets_t['sentiment'] = tweets_t['compound'].apply(getAnalysis)
st.write("Puntaje de análisis de sentimiento y visualización si el tweet es positivo, neutral o negativo")
tweets_t

st.write("Entre un grupo de 300 tweets tenemos: ")
st.write(tweets_t['sentiment'].value_counts())

st.write("Visualización de resultados: Gráfico de barras")
fig2 = plt.figure()
plt.title('Análisis de sentimiento')
plt.xlabel('Sentimiento')
plt.ylabel('Conteo')
tweets_t['sentiment'].value_counts().plot(kind = 'bar')
st.pyplot(fig2)

st.write("Visualización de resultados: Gráfico de pastel")
fig3 = plt.figure()
tweets_t.sentiment.value_counts().plot(kind='pie', autopct='%1.0f%%',  fontsize=12, figsize=(9,6), colors=["blue", "red", "yellow"])
plt.ylabel("Análisis de sentimiento en los últimos 300 tweets de la cuenta @PopBase", size=14)
st.pyplot(fig3)

st.write("Haz llegado hasta el final de esta sección. Gracias")

