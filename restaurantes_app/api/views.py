from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Restaurante


# Aquí crearemos la vista:

class RestaurantView(View):

    def get(self, request):
        restaurantes = list(Restaurante.objects.values())
        if len(restaurantes)>0:
            datos={'message': "Success", 'restaurantes': restaurantes}
        else:
            datos={'message': "Restaurants not found :( ..."}
        return JsonResponse(datos)

    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass
