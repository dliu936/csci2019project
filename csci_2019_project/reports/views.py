import plotly.graph_objects as go
import plotly.offline as opy
import pandas as pd

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView, TemplateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from src.oandareports.reports import exposure, correlation

exposure.
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


class ReportOpenTradeView(TemplateView):
    template_name = 'reports/opentrade.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportCorrelation(TemplateView):
    template_name = 'reports/correlation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportTradeDistribution(TemplateView):
    template_name = 'reports/tradedist.html'

    def get_context_data(self, **kwargs):
        context = super(ReportTradeDistribution, self).get_context_data(**kwargs)

        df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                             open=df['AAPL.Open'], high=df['AAPL.High'],
                                             low=df['AAPL.Low'], close=df['AAPL.Close'])
                              ])

        fig.update_layout(
            title='The Great Recession',
            yaxis_title='AAPL Stock',
            shapes=[dict(
                x0='2016-12-09', x1='2016-12-09', y0=0, y1=1, xref='x', yref='paper',
                line_width=2)],
            annotations=[dict(
                x='2016-12-09', y=0.05, xref='x', yref='paper',
                showarrow=False, xanchor='left', text='Increase Period Begins')]
        )
        div = opy.plot(fig, auto_open=False, output_type='div')
        context['graph'] = div
        return context


class ReportPricingDistribution(TemplateView):
    template_name = 'reports/pricingdist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
