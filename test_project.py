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
    Test the models for correctness, check the foreign key relationships.
    '''
    client = Client()

    def setUp(self):
        # Create user account
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
        response = self.client.get('/reports/')
        self.assertEqual(response.status_code, 200)


    def test_views(self):
        '''
        Test the views
        '''

        c = Client()
        c.open('reports/exposure')
        # Test the dates endpoint
        view = ReportExposureView.as_view(actions={'get': 'retrieve'})


