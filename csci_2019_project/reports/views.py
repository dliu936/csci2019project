from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView, TemplateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render


class ReportDashView(TemplateView):
    template_name = 'reports/dash.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ReportMainView(TemplateView):
    template_name = 'reports/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportExposureView(TemplateView):
    template_name = 'reports/exposure.html'


    def index(request):
        ccydict = {"Unites States Dollar" : "USD", "United Kingdom Pounds" : "GBP"}
        context = {'currencylist': ccydict}
        return render(request, ReportDashView.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportVolatilityView(TemplateView):
    template_name = 'reports/volatility.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportFinancingView(TemplateView):
    template_name = 'reports/financing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportNavView(TemplateView):
    template_name = 'reports/nav.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
