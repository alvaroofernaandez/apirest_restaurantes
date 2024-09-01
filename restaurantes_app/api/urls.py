from django.urls import path
from .views import RestaurantView


urlpatterns=  [
    path('restaurantes/', RestaurantView.as_view(),name='lista_restaurantes'),
    path('restaurantes/<int:id>', RestaurantView.as_view(), name='process_restaurantes'),

]