from django.urls import path
from .views import LoginUserView, LogoutUserView, \
                    RegisterUserView, PVView, PVPlotView


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
    path(
        'register/',
        RegisterUserView.as_view(),
        name='register'
    ),
    path(
        'pv-analysis/',
        PVView.as_view(),
        name='pv_analysis'
    ),
    path(
        'pv-analysis/plot/',
        PVPlotView.as_view(),
        name='plot_data'
    ),
]
