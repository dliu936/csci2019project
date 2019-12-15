#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `csci_2019_project` package."""

import os
import pytest

from tempfile import TemporaryDirectory
from django.test import TestCase as DJTest, Client, RequestFactory
from unittest import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from luigi import build

from src.oandareports.reports.exposure import ExposureReport
from src.oandareports.reports.correlation import CorrelationReport
from src.oandareports.reports.financing import FinancingReport
from src.oandareports.reports.netasset import NetAssetReport
from src.oandareports.reports.opentrades import OpenTradesReport
from src.oandareports.reports.tradedistribution import TradeDistributionReport

from csci_2019_project.reports.views import ReportExposureView, ReportCorrelation, \
                                            ReportDashView, ReportFinancingView, ReportNavView, \
                                            ReportCorrelation, ReportOpenTradeView, ReportVolatilityView, \
                                            ReportPricingDistribution, ReportTradeDistribution, ReportMainView

# Allow DB access
pytestmark = pytest.mark.django_db


class FakeFileFailure(IOError):
    pass



class TestWebSite(DJTest):
    '''
    Test each of web pages
    '''
    c = Client()

    def setUp(self):
        # No set up needed
        pass

    def test_responses(self):
        # Verify each of the endpoints are responding
        response = self.client.get('/reports/correlation/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/reports/exposure/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/reports/financing/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/reports/nav/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/reports/opentrade/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/reports/pricingdist/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/reports/tradedist/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/reports/volatility/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/reports/scenario/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/reports/spread/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/reports/')
        self.assertEqual(response.status_code, 200)


    def testBuild(self, rpt, MultFigs=False, **kwargs):
        '''
        Reusable test for checking if the report builds successfully.
        Pass in any parameters in kwargs.
        '''
        t = rpt(**kwargs)
        # Check if the task succeeds
        task = build([t], local_scheduler=True)
        self.assertTrue(task, msg=f"Could not build report {t.__class__}")
        if task:
            # Check if the graph is drawn
            if MultFigs:
                figs = t.figs
                self.assertTrue(len(figs) > 0)
            else:
                fig = t.fig
                self.assertIsNotNone(fig, msg="Figure was not generated")


    def test_correlation(self):
        '''
        correlation report
        '''
        c = Client()
        c.open('reports/correlation')
        # Build the report to get the output file
        r=CorrelationReport()
        self.testBuild(r)
        view = ReportCorrelation.as_view(actions={'get': 'retrieve'})


    def test_exposure(self):
        '''
        Exposure report
        '''
        c = Client()
        c.open('reports/exposure')
        # Build the report to get the output file
        r = ExposureReport()
        self.testBuild(r)
        view = ReportExposureView.as_view(actions={'get': 'retrieve'})


    def test_financing(self):
        '''
        Financing report
        '''
        c = Client()
        c.open('reports/financing')
        # Build the report to get the output file
        r = FinancingReport()
        self.testBuild(r, True)
        view = ReportFinancingView.as_view(actions={'get': 'retrieve'})


    def test_nav(self):
        '''
        Net Asset Value report
        '''
        c = Client()
        c.open('reports/nav')
        # Build the report to get the output file
        r = NetAssetReport()
        self.testBuild(r)
        view = ReportNavView.as_view(actions={'get': 'retrieve'})

    def test_opentrades(self):
        '''
        Open Trades report
        '''
        c = Client()
        c.open('reports/opentrades')
        # Build the report to get the output file
        r = OpenTradesReport()
        self.testBuild(r, True)
        view = ReportOpenTradeView.as_view(actions={'get': 'retrieve'})


    def test_tradedistrib(self):
        '''
        Trade Distribution report
        '''
        c = Client()
        c.open('reports/tradedist')
        # Build the report to get the output file
        r = ReportTradeDistribution()
        self.testBuild(r)
        view = ReportTradeDistribution.as_view(actions={'get': 'retrieve'})
