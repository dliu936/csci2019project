from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView, TemplateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _



class ReportMainView(TemplateView):
    template_name = 'reports/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportExposureView(TemplateView):
    template_name = 'reports/exposure.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ReportDashView(TemplateView):
    template_name = 'reports/dash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
