from django.urls import path
from .views import (Index, SuicideByCountry)

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('chart/<str:name>/', SuicideByCountry.as_view(), name='chart'),

]