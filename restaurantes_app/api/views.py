from functools import wraps
import jwt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Restaurante
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User, Group
from .jwt_utils import create_jwt
import json


def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth = request.META.get('HTTP_AUTHORIZATION', None)
        if auth is None:
            return JsonResponse({'message': "No se proporcionó el token."})
        try:
            token = auth.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': "El token ha expirado."})
        except jwt.InvalidTokenError:
            return JsonResponse({'message': "El token es inválido."})
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = User.objects.get(id=request.user_id)
            if not user.groups.filter(name=role).exists():
                return JsonResponse({'message': "No tienes permiso para realizar esta acción."}, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


class RestaurantView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(jwt_required)
    def get(self, request, id=0):
        if id > 0:
            restaurantes = list(Restaurante.objects.filter(id=id).values())
            if restaurantes:
                return JsonResponse({'message': "Restaurantes encontrados!", 'restaurantes': restaurantes})
            else:
                return JsonResponse({'message': "Restaurants not found..."})
        else:
            restaurantes = list(Restaurante.objects.values())
            return JsonResponse({'message': "Restaurantes encontrados!",
                                 'restaurantes': restaurantes}) if restaurantes else JsonResponse(
                {'message': "Restaurants not found."})

    @method_decorator(jwt_required)
    @method_decorator(role_required('admins'))
    def post(self, request):
        jd = json.loads(request.body)
        Restaurante.objects.create(name=jd['name'], web=jd['web'], yearFoundation=jd['yearFoundation'])
        return JsonResponse({'message': "Restaurante añadido con éxito."})

    @method_decorator(jwt_required)
    @method_decorator(role_required('admins'))
    def put(self, request, id):
        jd = json.loads(request.body)
        restaurante = Restaurante.objects.filter(id=id).first()
        if restaurante:
            restaurante.name = jd['name']
            restaurante.web = jd['web']
            restaurante.yearFoundation = jd['yearFoundation']
            restaurante.save()
            return JsonResponse({'message': "Restaurante editado con éxito."})
        else:
            return JsonResponse({'message': "Restaurants not found..."})

    @method_decorator(jwt_required)
    @method_decorator(role_required('admins'))
    def delete(self, request, id):
        restaurante = Restaurante.objects.filter(id=id).first()
        if restaurante:
            restaurante.delete()
            return JsonResponse({'message': "Restaurante eliminado."})
        else:
            return JsonResponse({'message': "Restaurants not found..."})


class UserManagementView(View):

    @method_decorator(jwt_required)
    @method_decorator(role_required('admins'))
    def get(self, request, id=0):
        if id:
            user = User.objects.filter(id=id).first()
            if user:
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': list(user.groups.values_list('name', flat=True)),
                }
                return JsonResponse({'message': "Usuario encontrado!", 'user': user_data})
            else:
                return JsonResponse({'message': "Usuario no encontrado."})
        else:
            users = list(User.objects.values('id', 'username', 'email'))
            return JsonResponse({'message': "Usuarios encontrados!", 'users': users})

    def post(self, request):
        jd = json.loads(request.body)
        try:
            user = User.objects.create_user(username=jd['username'], password=jd['password'], email=jd['email'])

            role = jd.get('role', 'user')
            if role == 'admin':
                group, created = Group.objects.get_or_create(name='admins')
                user.groups.add(group)
            else:
                group, created = Group.objects.get_or_create(name='users')
                user.groups.add(group)

            return JsonResponse({'message': 'Usuario creado con éxito.'})
        except Exception as e:
            return JsonResponse({'message': str(e)})

    @method_decorator(jwt_required)
    @method_decorator(role_required('admins'))
    def put(self, request, id):
        jd = json.loads(request.body)
        user = User.objects.filter(id=id).first()
        if user:
            user.username = jd.get('username', user.username)
            user.email = jd.get('email', user.email)
            if 'password' in jd:
                user.set_password(jd['password'])
            user.save()
            return JsonResponse({'message': "Usuario editado con éxito."})
        else:
            return JsonResponse({'message': "Usuario no encontrado."})

    @method_decorator(jwt_required)
    @method_decorator(role_required('admins'))
    def delete(self, request, id):
        user = User.objects.filter(id=id).first()
        if user:
            user.delete()
            return JsonResponse({'message': 'Usuario eliminado con éxito'})
        else:
            return JsonResponse({'message': 'Usuario no encontrado.'})


class UserLoginView(View):

    def post(self, request):
        jd = json.loads(request.body)
        username = jd['username']
        password = jd['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token = create_jwt(user)
            return JsonResponse({'token': token})
        else:
            return JsonResponse({'message': 'Credenciales inválidas.'})


class UserLogoutView(View):

    def post(self, request):
        logout(request)
        return JsonResponse({'message': 'Log out realizado con éxito, hasta pronto.'})


class UserProfileView(View):

    @method_decorator(jwt_required)
    def get(self, request):
        try:
            user_id = request.user_id
            user = User.objects.filter(id=user_id).first()

            if user is None:
                return JsonResponse({'message': "Usuario no encontrado."})
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            return JsonResponse({'message': "Datos del usuario.", 'user': user_data})
        except Exception as e:
            return JsonResponse({'error': str(e)})
