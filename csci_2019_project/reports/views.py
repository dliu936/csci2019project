import os
import plotly.graph_objects as go
import plotly.offline as opy
import plotly.tools as tls
import pandas as pd
import luigi
from luigi import build
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import oandareports as rp

#from oandareports.reports.exposure import ExposureReport as E

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView, TemplateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.core.management import BaseCommand, call_command

from src.oandareports.reports.exposure import ExposureReport
from src.oandareports.reports.correlation import CorrelationReport
from src.oandareports.reports.financing import FinancingReport
from src.oandareports.reports.netasset import NetAssetReport
from src.oandareports.reports.opentrades import OpenTradesReport
from src.oandareports.reports.tradedistribution import TradeDistributionReport

#from oandareports.reports.exposure import ExposureReport as exrpt
# from oandareports.reports.correlation import CorrelationReport
# from oandareports.reports.financing import FinancingReport
# from oandareports.reports.netasset import NetAssetReport
# from oandareports.reports.opentrades import OpenTradesReport



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
    '''
    Use this class to invoke luigi and be notified  when it completes successfully.
    '''
    template_name = 'reports/exposure.html'

    def index(request):
        return render(request, ReportDashView.template_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t = ExposureReport()
        task = build([t], local_scheduler=True)
        if task:
            plotly_fig = tls.mpl_to_plotly(t.fig)
            div = opy.plot(plotly_fig, auto_open=False, output_type='div')
            context['graph'] = div
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
        # t = FinancingReport()
        # task = build([t], local_scheduler=True)
        # if task:
        #     plotly_fig = tls.mpl_to_plotly(FigureCanvas(t.fig[0]))
        #     div = opy.plot(plotly_fig, auto_open=False, output_type='div')
        #     context['graph'] = div
        return context



class ReportNavView(TemplateView):
    template_name = 'reports/nav.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t = NetAssetReport()
        task = build([t], local_scheduler=True)
        if task:
            plotly_fig = tls.mpl_to_plotly(t.fig)
            div = opy.plot(plotly_fig, auto_open=False, output_type='div')
            context['graph'] = div
        return context


class ReportOpenTradeView(TemplateView):
    template_name = 'reports/opentrade.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # t = OpenTradesReport()
        # task = build([t], local_scheduler=True)
        # if task:
        #     plotly_fig = tls.mpl_to_plotly(FigureCanvas(t.fig[0]))
        #     div = opy.plot(plotly_fig, auto_open=False, output_type='div')
        #     context['graph'] = div
        return context


class ReportCorrelation(TemplateView):
    template_name = 'reports/correlation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # # TODO: get the selection
        # #if request.POST.getlist('cp3')
        # t = CorrelationReport(granularity='M5')
        # task = build([t], local_scheduler=True)
        # if task:
        #     plotly_fig = tls.mpl_to_plotly(t.fig)
        #     div = opy.plot(plotly_fig, auto_open=False, output_type='div')
        #     context['graph'] = div
        return context


class ReportTradeDistribution(TemplateView):
    template_name = 'reports/tradedist.html'

    def get_context_data(self, **kwargs):
        context = super(ReportTradeDistribution, self).get_context_data(**kwargs)
        # TODO: get the selection
        #if request.POST.getlist('cp3')
        t = TradeDistributionReport()
        task = build([t], local_scheduler=True)
        if task:
            plotly_fig = t.fig
            div = opy.plot(plotly_fig, auto_open=False, output_type='div')
            context['graph'] = div
        return context


class ReportPricingDistribution(TemplateView):
    template_name = 'reports/pricingdist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ReportScenarioView(TemplateView):
    template_name = 'reports/scenario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReportSpread(TemplateView):
    template_name = 'reports/spread.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DemoCandleStick(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(DemoCandleStick, self).get_context_data(**kwargs)

        df = pd.read_csv(os.path.join('data','stocks','sample.csv'))

        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                             open=df['USD_EUR.Open'], high=df['USD_EUR.High'],
                                             low=df['USD_EUR.Low'], close=df['USD_EUR.Close'])
                              ])

        fig.update_layout(
            title='Trade Distribution',
            yaxis_title='USD/EUR',
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
