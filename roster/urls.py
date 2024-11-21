from django.urls import path
from . import views


urlpatterns = [
    path('', views.import_availability, name='import_availability'),
    path('generate-roster/<int:month>/<int:year>/', views.generate_roster_for_month, name='generate_roster'),
]