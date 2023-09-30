from django.urls import path

from appaframe import views

app_name = 'appaframe'

urlpatterns = [
    path('aframe/', views.AframeView.as_view(), name="aframe"),
]