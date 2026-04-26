from django.urls import path
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # other URLs...
    #path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.front, name='homepage'),
    path('api/register_customer/', views.register_customer),
    path('api/login/', views.login, name='apilogin'),
    path('api/fetch_production/', views.fetch_productions, name='apifetch_productions'),
    path('productions_page/', views.account, name='account'),
    path("login/", views.loginapiconsumer)
]