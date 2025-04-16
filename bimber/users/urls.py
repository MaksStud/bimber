from django.urls import path

from users import views

urlpatterns = [
    path('auth/', views.ApiAuthorizationView.as_view(), name='user-auth'),
]