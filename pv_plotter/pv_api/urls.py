from django.urls import path
from .views import LoginUserView, LogoutUserView


app_name = 'api'

urlpatterns = [
    path(
        'login/',
        LoginUserView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        LogoutUserView.as_view(),
        name='logout'
    ),
]