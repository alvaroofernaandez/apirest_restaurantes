from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurante
import json


# Aquí crearemos la vista:

class RestaurantView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if (id>0):
            restaurantes = list(Restaurante.objects.filter(id=id).values())
            if len(restaurantes) > 0:
                restaurante = restaurantes[0]
                datos={'message': "Restaurantes encontrados!", 'restaurantes': restaurantes}
            else:
                datos = {'message': "Restaurants not found..."}
            return JsonResponse(datos)
        else:
            restaurantes = list(Restaurante.objects.values())
            if len(restaurantes)>0:
                datos={'message': "Restaurantes encontrados!", 'restaurantes': restaurantes}
            else:
                datos={'message': "Restaurants not found."}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body)
        Restaurante.objects.create(name=jd['name'],web=jd['web'],yearFoundation=jd['yearFoundation'])
        datos={'message': "Restaurante añadido con éxito."}
        return JsonResponse(datos)


    def put(self, request, id):
        jd = json.loads(request.body)
        restaurantes = list(Restaurante.objects.filter(id=id).values())
        if len(restaurantes) > 0:
            restaurante = Restaurante.objects.get(id=id)
            restaurante.name=jd['name']
            restaurante.web=jd['web']
            restaurante.yearFoundation=jd['yearFoundation']
            restaurante.save()
            datos = {'message': "Restaurante editado con éxito."}
        else:
            datos = {'message': "Restaurants not found..."}
        return JsonResponse(datos)

    def delete(self, request, id):
        restaurantes = list(Restaurante.objects.filter(id=id).values())
        if len(restaurantes) > 0:
            Restaurante.objects.filter(id=id).delete()
            datos = {'message': "Restaurante eliminado."}
        else:
            datos = {'message': "Restaurants not found..."}
        return JsonResponse(datos)