import numpy as np
import numpy as np
import re
from sklearn.pipeline import Pipeline
import pickle
import seaborn as sns
import copy
import nltk
nltk.download('stopwords')
nltk.download('wordnet') 
nltk.download('omw-1.4')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from string import punctuation
from keras.models import load_model

from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from nltk.stem.wordnet import WordNetLemmatizer
from django.urls import reverse

import pandas as pd

print('Librerias importadas')

class modeloSNN():
    def cargarPipeline(self,nombreArchivo):
        with open(nombreArchivo+'.pickle', 'rb') as handle:
            pipeline = pickle.load(handle)
        print('Picke cargado correctamente')
        return pipeline

    def cargarRNN(self,nombreArchivo):
        print('Intentando leer la red neuronal desde el archivo')
        model = load_model(nombreArchivo+'.h5')    
        print("Red Neuronal Cargada desde Archivo") 
        return model
   
    
    def predict(self,datos_entrada):
        df = pd.DataFrame(columns=['text'])
        df.loc[0] = datos_entrada
        
        print("Prediciendo con los datos de entrada")
        model = load_model("C:/Users/esteb/OneDrive - Universidad Politecnica Salesiana/7mo ciclo/Aprendizaje automatico/Practica 1/Libros/Django/proyectoRestaurante/proyectoRestauranteNN/Recursos/redNN65.h5")
        print("RNN cargada")
        with open('C:/Users/esteb/OneDrive - Universidad Politecnica Salesiana/7mo ciclo/Aprendizaje automatico/Practica 1/Libros/Django/proyectoRestaurante/proyectoRestauranteNN/Recursos/tokenizer.pickle', 'rb') as handle:
            pipeline = pickle.load(handle)
        print('Picke cargado correctamente')
        tokenizer = pipeline
        print("Tokenizer cargado")
        print('Creado el dataframe de entrada')
        #df['text'] = df['text'].apply(preprocessor)
        
        max_features = 100
        X2 = tokenizer.texts_to_sequences(df['text'].values)
        X2 = pad_sequences(X2,maxlen=80)
        
        print(X2.shape)
        output = model.predict(X2)
        
        # Print the predicted output
        max_values = np.argmax(output, axis=1)
        
        out = []
        j=0
        
        for i in max_values:
            if(i==0):
                out.append(f'Malo con una precisión del {output[j][i]}%')
            elif(i==1):
                out.append(f'Bueno con una precisión del {output[j][i]}%')
            else:
                out.append(f'Excelente con una precisión del {output[j][i]}%')
            j+=1
        
        return out
