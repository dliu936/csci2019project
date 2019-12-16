#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `csci_2019_project` package.


The web site will call the report generator and dynamically create the report.
The result will be displayed to the user.

The test scenarios were difficult to come up with. The views were all self-contained.
At a minimum, consideration was given to verify the report generator could be called and the resulting
output was expected.

As noted on the Django website, the testing of content is better suited to tools such as Selenium.


"""

import os
import pytest

from tempfile import TemporaryDirectory
from django.test import TestCase as DJTest, Client, RequestFactory
from unittest import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from luigi import build

# TODO: rename these once it is in the master branch
from oandareports.reports.exposure import ExposureReport
from oandareports.reports.correlation import CorrelationReport
from oandareports.reports.financing import FinancingReport
from oandareports.reports.netasset import NetAssetReport
from oandareports.reports.opentrades import OpenTradesReport
from oandareports.reports.tradedistribution import TradeDistributionReport

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
    client = Client()

    def setUp(self):
        # No set up needed
        pass


    def test_correlation(self):
        '''
        correlation report
        '''
        c = Client()
        c.get('reports/correlation')
        # Build the report to get the output file
        r=CorrelationReport(granularity='M5')
        # Check if the task succeeds
        task = build([r], local_scheduler=True)
        self.assertTrue(task, msg=f"Could not build report {r.__class__}")
        if task:
            fig = r.fig
            self.assertIsNotNone(fig, msg="Figure was not generated")


    def test_exposure(self):
        '''
        Exposure report
        '''
        c = Client()
        c.get('reports/exposure')
        # Build the report to get the output file
        r = ExposureReport()
        # Check if the task succeeds
        task = build([r], local_scheduler=True)
        self.assertTrue(task, msg=f"Could not build report {r.__class__}")
        if task:
            fig = r.fig
            self.assertIsNotNone(fig, msg="Figure was not generated")


    def test_financing(self):
        '''
        Financing report
        '''
        c = Client()
        c.get('reports/financing')
        # Build the report to get the output file
        r = FinancingReport()
        task = build([r], local_scheduler=True)
        self.assertTrue(task, msg=f"Could not build report {r.__class__}")
        if task:
            figs = r.figs
            self.assertTrue(len(figs) > 0)


    def test_nav(self):
        '''
        Net Asset Value report
        '''
        c = Client()
        c.get('reports/nav')
        # Build the report to get the output file
        r = NetAssetReport()
        task = build([r], local_scheduler=True)
        self.assertTrue(task, msg=f"Could not build report {r.__class__}")
        if task:
            fig = r.fig
            self.assertIsNotNone(fig, msg="Figure was not generated")


    def test_opentrades(self):
        '''
        Open Trades report
        '''
        c = Client()
        c.get('reports/opentrades')
        # Build the report to get the output file
        r = OpenTradesReport()
        task = build([r], local_scheduler=True)
        self.assertTrue(task, msg=f"Could not build report {r.__class__}")
        if task:
            figs = r.figs
            self.assertTrue(len(figs) > 0)



    def test_tradedistrib(self):
        '''
        Trade Distribution report
        '''
        c = Client()
        c.get('reports/tradedist')
        # Build the report to get the output file
        r = TradeDistributionReport()
        task = build([r], local_scheduler=True)
        self.assertTrue(task, msg=f"Could not build report {r.__class__}")
        if task:
            fig = r.fig
            self.assertIsNotNone(fig, msg="Figure was not generated")

