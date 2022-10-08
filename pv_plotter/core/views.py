from django.views.generic import TemplateView
from .utils import PVPlotly


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginView(TemplateView):
    template_name = 'core/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AuthView(TemplateView):  # TODO RedirectView
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RegisterView(TemplateView):
    template_name = 'core/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ForgotPasswordView(TemplateView):
    template_name = 'core/forgot_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RestorePasswordView(TemplateView):
    template_name = 'core/restore_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PVPlotView(TemplateView):
    template_name = 'core/pv_analysis.html'

    def get_context_data(self, **kwargs):
        plt = PVPlotly()
        context = super().get_context_data(**kwargs)
        context['figure'] = plt.render_layout()
        return context
