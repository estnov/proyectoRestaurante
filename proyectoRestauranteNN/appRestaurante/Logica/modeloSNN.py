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
    def cargarPipeline(nombreArchivo):
        with open(nombreArchivo+'.pickle', 'rb') as handle:
            pipeline = pickle.load(handle)
        print('Picke cargado correctamente')
        return pipeline

    def cargarRNN(nombreArchivo):
        model = load_model(nombreArchivo+'.h5')    
        print("Red Neuronal Cargada desde Archivo") 
        return model
    
    def generarStopWords():
        ##Creating a list of stop words and adding custom stopwords
        stop_words = set(stopwords.words('spanish'))
        ##Creating a list of custom stopwords
        new_words = ['pastas','filo','amigas','amigos']
        stop_words = stop_words.union(new_words)
        return stop_words

    stop = generarStopWords()
    porter = PorterStemmer()

    def normalize(s):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
            ("à", "a"),
            ("è", "e"),
            ("ì", "i"),
            ("ò", "o"),
            ("ù", "u"),
            ("ñ", "n"),
        )
        for a, b in replacements:
            s = s.replace(a, b).replace(a.upper(), b.upper())
        return s

    def preprocessor(text):#tokenizer
        #text = re.sub('[^a-zA-z0-9ñ\s]','',text)
        text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text) #remove tags
        text = re.sub('<[^>]*>', '', text)
        emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
        text = re.sub('[\W]+', ' ', text.lower()) + ' '.join(emoticons).replace('-', '')
        
        text = normalize(text)
        
        text = ''.join([c if c not in punctuation else ' '+c+' ' \
                        for c in text]).lower()    
        #text=re.sub("(\\d|\\W)+"," ",text) # remove special characters and digits
        ##Stemming
        text = text.split()
        #ps=PorterStemmer()
        #Lemmatisation
        lem = WordNetLemmatizer()
        text = [lem.lemmatize(word) for word in text if not word in  
                stop]
        tokenized = " ".join(text)
        return tokenized
    
    
    model = cargarRNN("C:/Users/esteb/OneDrive - Universidad Politecnica Salesiana/7mo ciclo/Aprendizaje automatico/Practica 1/Libros/Django/proyectoRestaurante/proyectoRestauranteNN/Recursos/redNN65")
    tokenizer = cargarPipeline('C:/Users/esteb/OneDrive - Universidad Politecnica Salesiana/7mo ciclo/Aprendizaje automatico/Practica 1/Libros/Django/proyectoRestaurante/proyectoRestauranteNN/Recursos/tokenizer')
    
    
    def predict(datos_entrada):
        
        model = cargarRNN('C:/Users/esteb/OneDrive - Universidad Politecnica Salesiana/7mo ciclo/Aprendizaje automatico/Practica 1/Libros/Django/proyectoRestaurante/proyectoRestauranteNN/Recursos/redNN65')
        tokenizer = cargarPipeline('C:/Users/esteb/OneDrive - Universidad Politecnica Salesiana/7mo ciclo/Aprendizaje automatico/Practica 1/Libros/Django/proyectoRestaurante/proyectoRestauranteNN/Recursos/tokenizer')
    
        datos_entrada['text'] = datos_entrada['text'].apply(preprocessor)
        
        max_features = 100
        X2 = tokenizer.texts_to_sequences(datos_entrada['text'].values)
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
