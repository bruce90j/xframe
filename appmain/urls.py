from django.urls import path, include

from appmain import views

app_name = 'appmain'

urlpatterns = [
    path('', views.IndexView.as_view(), name="home"),
    path('aframe/', views.AframeView.as_view(), name="aframe"),
    path('connect-wallet', views.ConnectWalletView.as_view(), name="connect_wallet"),
    path('connect-xumm-wallet', views.ConnectXummWalletView.as_view(), name="connect_xumm_wallet"),
    path('logout/', views.logout_view, name='logout'),
]