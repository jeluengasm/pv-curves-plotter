from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name='home'
    ),
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'login/auth',
        views.AuthView.as_view(),
        name='auth'
    ),
    path(
        'logout/',
        views.HomeView.as_view(),  # TODO: change view
        name='logout'
    ),
    path(
        'register/',
        views.RegisterView.as_view(),
        name='register'
    ),
    path(
        'register/done/',
        TemplateView.as_view(template_name='core/register_done.html'),
        name='register_done'
    ),
    path(
        'user/password-recovery/',
        views.ForgotPasswordView.as_view(),
        name='recovery'
    ),
    path(
        'user/restore-password/',
        views.RestorePasswordView.as_view(),
        name='restore'
    ),
    path(
        'pv-analysis/',
        views.PVPlotView.as_view(),
        name='pv_analysis'
    ),
    path(
        'about-us/',
        TemplateView.as_view(template_name='core/about-us.html'),
        name='about_us'
    ),
    path(
        'contact-us/',
        TemplateView.as_view(template_name='core/contact-us.html'),
        name='contact_us'
    ),
    path(
        'faq/',
        TemplateView.as_view(template_name='core/faq.html'),
        name='faq'
    ),
    path(
        'install/',
        TemplateView.as_view(template_name='core/installation.html'),
        name='installation'
    ),
    path(
        'the-app/',
        TemplateView.as_view(template_name='core/the_app.html'),
        name='the_app'
    ),
]
