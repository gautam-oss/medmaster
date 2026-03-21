from django.urls import path
from . import views

app_name = 'insurance'

urlpatterns = [
    path('predict/', views.predict_insurance, name='predict'),
    path('result/<int:prediction_id>/', views.prediction_result, name='result'),
    path('guest-result/', views.guest_result, name='guest_result'),
    path('history/', views.prediction_history, name='history'),
    path('about/', views.about_model, name='about'),
]
