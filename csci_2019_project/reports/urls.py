from django.urls import path


from .views import * # ReportExposureView, ReportDashView, ReportNavView, R

#app_name = "reports"

urlpatterns = [
    path("", ReportDashView.as_view(), name="reports_dash"),
    path("dash", ReportDashView.as_view(), name="reports_dash"),
    path("exposure", ReportExposureView.as_view(), name="reports_exposure"),
    path("volatility", ReportVolatilityView.as_view(), name="reports_volatility"),
    path("financing", ReportFinancingView.as_view(), name="reports_financing"),
    path("netassetvalue", ReportNavView.as_view(), name="reports_nav"),
]
