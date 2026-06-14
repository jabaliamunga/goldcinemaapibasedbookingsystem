from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


urlpatterns = [
    # other URLs...
    path('api/token/', views.EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.front, name='front'),
    path('api/register_customer/', views.register_customer),
    path('api/fetch_productions/', views.fetch_productions, name='apifetch_productions'),
    path('productions_page/', views.account, name='account'), # view to display the booking page
    path("login/", views.loginapiconsumer), #url that consumes API
    path("api/booking/", views.booking, name='api/booking' ),
    path("register_customerapi_consumption/", views.register_customerapi_consumption, name="register_customerapi_consumption"),
    path("booking_api_consumption/", views.booking_api_consumption, name='booking_api_consumption'),
    path("api/fetch_seats/", views.fetch_seats, name='fetch_seats'),
    path("test/", views.checkseats, name="test"),
    path("board/", views.board, name="board")
]