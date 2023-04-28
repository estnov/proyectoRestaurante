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
            comentario = int(request.POST.get('COMENTARIO'))
            print(comentario)
            #Consumo de la lógica para predecir si se aprueba o no el crédito
            resul=modeloSNN.modeloSNN.predict(comentario)
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
        body = json.loads(request.body.decode('utf-8'))
        #Formato de datos de entrada
        comentario = str(body.get("COMENTARIO"))
        print(comentario)
        resul=modeloSNN.modeloSNN.predict(comentario)
        data = {'result': resul}
        resp=JsonResponse(data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp