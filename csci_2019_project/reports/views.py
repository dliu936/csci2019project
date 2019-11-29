from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView, TemplateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class ReportMainView(TemplateView):
    template_name = 'templates/reports/reports.html'


class ReportExposureView(TemplateView):
    template_name = 'templates/reports/exposure.html'

class ReportDashView(TemplateView):
    template_name = 'templates/reports/reports_dash.html'
