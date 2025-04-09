# booking_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('conferences/', views.conferences_view, name='conferences'),
    path('conferences/<int:conference_id>/', views.conference_detail_view, name='conference_detail'),
    path('conferences/<int:conference_id>/book/', views.booking_view, name='book_conference'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('my-bookings/<int:booking_id>/cancel/', views.cancel_booking_view, name='cancel_booking'),
    path('conferences/<int:conference_id>/feedback/', views.feedback_view, name='feedback'),
]
