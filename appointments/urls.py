from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book_appointment, name='book'),
    path('my/', views.my_appointments, name='my_appointments'),
    path('success/<int:appointment_id>/', views.appointment_success, name='success'),
    path('update/<int:appointment_id>/', views.update_appointment, name='update'),
]
