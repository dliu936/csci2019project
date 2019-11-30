from django.urls import path

from .views import ReportMainView, ReportExposureView, ReportDashView

#app_name = "reports"

urlpatterns = [
    path("", ReportMainView.as_view(), name="reports"),
    path("dash", ReportDashView.as_view(), name="reports_dash"),
    path("exposure", ReportExposureView.as_view(), name="reports_exposure"),
]
