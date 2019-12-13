from django.urls import path


from .views import *

#app_name = "reports"

urlpatterns = [
    path("", ReportDashView.as_view(), name="reports_dash"),
    path("dash", ReportDashView.as_view(), name="reports_dash"),
    path("exposure", ReportExposureView.as_view(), name="exposure"),
    path("volatility", ReportVolatilityView.as_view(), name="volatility"),
    path("financing", ReportFinancingView.as_view(), name="financing"),
    path("netassetvalue", ReportNavView.as_view(), name="nav"),
    path("opentrades", ReportOpenTradeView.as_view(), name="opentrades"),
    path("correlation", ReportCorrelation.as_view(), name="correlation"),
    path("tradedist", ReportTradeDistribution.as_view(), name="tradedist"),
    path("pricingdist", ReportPricingDistribution.as_view(), name="pricingdist"),
]
