# -*- coding: utf-8 -*-
"""redes-neuronales-bayesianas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cLLgQVTNdQwbPmIwyYsetH7zft4s_o1D

# Redes Neuronales Bayesianas
A partir del artículo encontrado se buscará implementar y capacitar una red neuronal bayesiana con la ayuda de la herramienta Keras después del cálculo de la incertidumbre de peso en las redes neuronales.
Para lograr tal objetivo se utilizará también la herramienta Tensor Flow.  

Como toda red neuronal bayesiana, se caracteriza por asignar una distribución de probabilidad en lugar de un solo valor o estimación. Por tal motivo estas distribuciones de probabilidad se encargan de describir la incertidumbre de los pesos y se utiliza para estimar la incertidumbre en las predicciones.

#### Fuente de la replicación:
- https://www.sciencedirect.com/science/article/abs/pii/S0893608021000356  
- https://nbviewer.org/github/krasserm/bayesian-machine-learning/blob/dev/bayesian-neural-networks/bayesian_neural_networks.ipynb

## Implementación

La inferencia variacional de los parámetros de la red neuronal ahora se demuestra en un problema de regresión simple. Por lo tanto se hará uso de una distribución Gaussiana.
El conjunto de datos de entrenamiento en este ejemplo consta de 32 muestras.
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import streamlit as st
import warnings
import matplotlib.pyplot as plt

# to ignore
warnings.filterwarnings("ignore")

# %matplotlib inline

# Streamlit
st.set_page_config(page_title="RNB")
st.markdown("# RNB")
st.sidebar.header("RNB")
st.markdown(
    """
    #Redes Neuronales Bayesianas
    A partir del artículo encontrado se buscará implementar y capacitar una red neuronal bayesiana con la ayuda de la herramienta Keras después del cálculo de la incertidumbre de peso en las redes neuronales.  
    Para lograr tal objetivo se utilizará también la herramienta Tensor Flow.
    """
)

st.markdown(
    """
    Como toda red neuronal bayesiana, se caracteriza por asignar una distribución de probabilidad en lugar de un solo valor o estimación. Por tal motivo estas distribuciones de probabilidad se encargan de describir la incertidumbre de los pesos y se utiliza para estimar la incertidumbre en las predicciones.
    ###Fuente de la replicación:
    - https://www.sciencedirect.com/science/article/abs/pii/S0893608021000356  
    - https://nbviewer.org/github/krasserm/bayesian-machine-learning/blob/dev/bayesian-neural-networks/bayesian_neural_networks.ipynb
    """
)

st.markdown(
    """
    ## Implementación
    La inferencia variacional de los parámetros de la red neuronal ahora se demuestra en un problema de regresión simple. Por lo tanto se hará uso de una distribución Gaussiana.  
    El conjunto de datos de entrenamiento en este ejemplo consta de 32 muestras.
    """
)

def f(x, sigma):
    epsilon = np.random.randn(*x.shape) * sigma
    return 10 * np.sin(2 * np.pi * (x)) + epsilon
#data = pd.read_csv('Google_train_data.csv')


train_size = 32
noise = 1.0

X = np.linspace(-0.5, 0.5, train_size).reshape(-1, 1)
y = f(X, sigma=noise)
y_true = f(X, sigma=0.0)

plt.scatter(X, y, marker='+', label='Training data')
plt.plot(X, y_true, label='Truth')
plt.title('Noisy training data and ground truth')
plt.legend();

st.write
(
    "
    El ruido en los datos de entrenamiento da lugar a una incertidumbre aleatoria. Para cubrir esta incertidumbre epistémica, se implementa la lógica de inferencia variacional en una capa DenseVariational.
    "
)

from keras import backend as K
from keras import activations, initializers
from keras.layers import Layer

import tensorflow as tf
import tensorflow_probability as tfp


class DenseVariational(Layer):
    def __init__(self,
                 units,
                 kl_weight,
                 activation=None,
                 prior_sigma_1=1.5,
                 prior_sigma_2=0.1,
                 prior_pi=0.5, **kwargs):
        self.units = units
        self.kl_weight = kl_weight
        self.activation = activations.get(activation)
        self.prior_sigma_1 = prior_sigma_1
        self.prior_sigma_2 = prior_sigma_2
        self.prior_pi_1 = prior_pi
        self.prior_pi_2 = 1.0 - prior_pi
        self.init_sigma = np.sqrt(self.prior_pi_1 * self.prior_sigma_1 ** 2 +
                                  self.prior_pi_2 * self.prior_sigma_2 ** 2)

        super().__init__(**kwargs)

    def compute_output_shape(self, input_shape):
        return input_shape[0], self.units

    def build(self, input_shape):
        self.kernel_mu = self.add_weight(name='kernel_mu',
                                         shape=(input_shape[1], self.units),
                                         initializer=initializers.normal(stddev=self.init_sigma),
                                         trainable=True)
        self.bias_mu = self.add_weight(name='bias_mu',
                                       shape=(self.units,),
                                       initializer=initializers.normal(stddev=self.init_sigma),
                                       trainable=True)
        self.kernel_rho = self.add_weight(name='kernel_rho',
                                          shape=(input_shape[1], self.units),
                                          initializer=initializers.constant(0.0),
                                          trainable=True)
        self.bias_rho = self.add_weight(name='bias_rho',
                                        shape=(self.units,),
                                        initializer=initializers.constant(0.0),
                                        trainable=True)
        super().build(input_shape)

    def call(self, inputs, **kwargs):
        kernel_sigma = tf.math.softplus(self.kernel_rho)
        kernel = self.kernel_mu + kernel_sigma * tf.random.normal(self.kernel_mu.shape)

        bias_sigma = tf.math.softplus(self.bias_rho)
        bias = self.bias_mu + bias_sigma * tf.random.normal(self.bias_mu.shape)

        self.add_loss(self.kl_loss(kernel, self.kernel_mu, kernel_sigma) +
                      self.kl_loss(bias, self.bias_mu, bias_sigma))

        return self.activation(K.dot(inputs, kernel) + bias)

    def kl_loss(self, w, mu, sigma):
        variational_dist = tfp.distributions.Normal(mu, sigma)
        return self.kl_weight * K.sum(variational_dist.log_prob(w) - self.log_prior_prob(w))

    def log_prior_prob(self, w):
        comp_1_dist = tfp.distributions.Normal(0.0, self.prior_sigma_1)
        comp_2_dist = tfp.distributions.Normal(0.0, self.prior_sigma_2)
        return K.log(self.prior_pi_1 * comp_1_dist.prob(w) +
                     self.prior_pi_2 * comp_2_dist.prob(w))

st.write
(
    "
    El modelo implementado es una red neuronal con dos capas ocultas DenseVariational, cada una con 20 unidades, y una capa de salida DenseVariational con una unidad. En lugar de modelar una distribución de probabilidad completa como salida, la red simplemente genera la media de la distribución gaussiana correspondiente.
    "
)

import warnings
warnings.filterwarnings('ignore')

from keras.layers import Input
from keras.models import Model

batch_size = train_size
num_batches = train_size / batch_size

kl_weight = 1.0 / num_batches
prior_params = {
    'prior_sigma_1': 1.5, 
    'prior_sigma_2': 0.1, 
    'prior_pi': 0.5 
}

x_in = Input(shape=(1,))
x = DenseVariational(20, kl_weight, **prior_params, activation='relu')(x_in)
x = DenseVariational(20, kl_weight, **prior_params, activation='relu')(x)
x = DenseVariational(1, kl_weight, **prior_params)(x)

model = Model(x_in, x)

st.write
(
    "
    La red ahora se puede entrenar con una función de probabilidad logarítmica negativa gaussiana (neg_log_likelihood) como función de pérdida suponiendo una desviación estándar fija (ruido).
    "
)

from keras import callbacks, optimizers

def neg_log_likelihood(y_obs, y_pred, sigma=noise):
    dist = tfp.distributions.Normal(loc=y_pred, scale=sigma)
    return K.sum(-dist.log_prob(y_obs))

model.compile(loss=neg_log_likelihood, optimizer=optimizers.Adam(lr=0.08), metrics=['mse'])
model.fit(X, y, batch_size=batch_size, epochs=1500, verbose=0);

st.write
(
    "
    En la implementación al llamar a model.predict extraemos una muestra aleatoria de la distribución posterior variacional y la usamos para calcular el valor de salida de la red. A partir de estas predicciones podemos calcular estadísticas como la media y la desviación estándar.
    "
)

import tqdm

X_test = np.linspace(-1.5, 1.5, 1000).reshape(-1, 1)
y_pred_list = []

for i in tqdm.tqdm(range(500)):
    y_pred = model.predict(X_test)
    y_pred_list.append(y_pred)
    
y_preds = np.concatenate(y_pred_list, axis=1)

y_mean = np.mean(y_preds, axis=1)
y_sigma = np.std(y_preds, axis=1)

plt.plot(X_test, y_mean, 'r-', label='Predictive mean');
plt.scatter(X, y, marker='+', label='Training data')
plt.fill_between(X_test.ravel(), 
                 y_mean + 2 * y_sigma, 
                 y_mean - 2 * y_sigma, 
                 alpha=0.5, label='Epistemic uncertainty')
plt.title('Prediction')
plt.legend();

st.write
(
    "
    Podemos ver claramente en el gráfico anterior que la incertidumbre epistémica es mucho mayor en regiones sin datos de entrenamiento que en regiones con datos de entrenamiento existentes.
    "
)
