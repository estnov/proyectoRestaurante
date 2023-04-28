from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse
from appRestaurante.Logica import modeloSNN

print("Librerias importadas")

class Clasificacion():
    def determinarCategoria(request):
        return render(request, "comentarioRestaurante.html")
    @api_view(['GET','POST'])
    def predecir(request):
        try:
            print("Ingresa a predecir")
            #Formato de datos de entrada
            print("")
            print(request.POST)
            print(request.POST.get('COMENTARIO'))
            comentario = str(request.POST.get('COMENTARIO'))
            print(comentario)
            #Consumo de la lógica para predecir si se aprueba o no el crédito
            resul=modeloSNN.modeloSNN.predict(modeloSNN.modeloSNN,comentario)
        except:
            resul='Datos inválidos'
        return render(request, "informe.html",{"e":resul})
    @csrf_exempt
    @api_view(['GET','POST'])
    def predecirIOJson(request):
        print(request)
        print('***')
        print(request.body)
        print('***')
        print('Leer comentario')
        print(request.POST.get('COMENTARIO'))
        #body = json.loads(request.body.decode('utf-8'))
        #print('Leer body')        
        #print(body)
        #Formato de datos de entrada
        #comentario = str(body.get("COMENTARIO"))
        print('***')
        #print(comentario)   
        resul=modeloSNN.modeloSNN.predict(modeloSNN.modeloSNN,request.POST.get('COMENTARIO'))
        data = {'result': resul}
        resp=JsonResponse(data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp