from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.register, name="register"),
    path('home', views.home, name="home"),
    path('logout', views.logout, name="logout"),
    path('sell', views.sell, name="sell"),
    path('buy', views.buy, name="buy"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('wallet', views.wallet, name="wallet"),
    path('transactions', views.transactions, name="transactions"),
    path('setting', views.setting, name="setting"),
    path("verify_payment/<str:ref>", views.verify_payment, name="verify-payment"),
]
