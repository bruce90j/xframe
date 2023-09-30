from django.urls import path

from appmain import views

app_name = 'appmain'

urlpatterns = [
    path('', views.IndexView.as_view(), name="home"),
    path('account/', views.AccountView.as_view(), name="account"),
    path('nft/<str:xid>/', views.NFTMetadataView.as_view(), name="nft-metadata"),
    path('account/nft-create/', views.NFTCreateView.as_view(), name="nft-create"),
    path('account/sign-payload/', views.SignPayloadView.as_view(), name="sign-payload"),
    path('connect-wallet', views.ConnectWalletView.as_view(), name="connect_wallet"),
    path('connect-xumm-wallet', views.ConnectXummWalletView.as_view(), name="connect_xumm_wallet"),
    path('logout/', views.logout_view, name='logout'),
]