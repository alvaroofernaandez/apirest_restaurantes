from django.urls import path
from .views import RestaurantView, UserManagementView, UserLoginView, UserLogoutView

urlpatterns=  [
    path('restaurantes/', RestaurantView.as_view(),name='lista_restaurantes'),
    path('restaurantes/<int:id>', RestaurantView.as_view(), name='process_restaurantes'),
    path('users/', UserManagementView.as_view(), name='user_crud_api'),
    path('users/<int:id>/', UserManagementView.as_view(), name='user_detail'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout')
]