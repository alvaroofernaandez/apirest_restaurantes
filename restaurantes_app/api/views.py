from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurante
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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

# LOGIN, USUARIOS, ETC

class UserManagementView(View):

    def get(self, request, id=0):
        if id:
            user = User.objects.filter(id=id).first()
            if user:
                user_data = {'id': user.id, 'username': user.username, 'email': user.email}
                datos = {'message': "Usuario encontrado!", 'user': user_data}
            else:
                datos = {'message': "Usuario no encontrado."}
        else:
            users = list(User.objects.values('id', 'username', 'email'))
            datos = {'message': "Usuarios encontrados!", 'users': users}
        return JsonResponse(datos)

    def post(self, request):
        jd=json.loads(request.body)
        try:
            user = User.objects.create_user(username=jd['username'], password=jd['password'], email=jd['email'])
            datos = {'message': 'Usuario creado con éxito.'}
        except Exception as e:
            datos = {'message': str(e)}
        return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        user = User.objects.filter(id=id).first()
        if user:
            user.username = jd.get('username', user.username)
            user.email = jd.get('email', user.email)
            if 'password' in jd:
                user.set_password(jd['password'])
            user.save()
            datos = {'message': "Usuario editado con éxito."}
            return JsonResponse(datos)
        else:
            datos = {'message': "Usuario no encontrado."}
        return JsonResponse(datos)


    def delete(self, request, id):
        user = User.objects.filter(id=id).first()
        if user:
            user.delete()
            datos = {'message': 'Usuario eliminado con éxito'}
        else:
            datos = {'message': 'Usuario no encontrado.'}
        return JsonResponse(datos)

class UserLoginView(View):

    def post(self, request):
        jd = json.loads(request.body)
        username = jd['username']
        password = jd['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            datos = {'message': 'Log in realizado con éxito.'}
            return JsonResponse(datos)
        else:
            datos = {'message': 'Credenciales inválidas.'}
        return JsonResponse(datos)

class UserLogoutView(View):

    def post(self, request):
        logout(request)
        datos = {'message': 'Log out realizado con éxito, hasta pronto.'}
        return JsonResponse(datos)


