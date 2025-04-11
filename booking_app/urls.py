# booking_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('conferences/', views.conferences_view, name='conferences'),
    path('conferences/<slug:slug>/', views.conference_detail_view, name='conference_detail'),
    path('conferences/<slug:slug>/book/', views.booking_view, name='book_conference'),
    path('conferences/<slug:slug>/feedback/', views.feedback_view, name='feedback'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('my-bookings/<int:booking_id>/cancel/', views.cancel_booking_view, name='cancel_booking'),
    path('receipt/<int:booking_id>/', views.receipt_view, name='receipt'),
    path('receipt/<int:booking_id>/download/', views.download_receipt_view, name='download_receipt'),
]
