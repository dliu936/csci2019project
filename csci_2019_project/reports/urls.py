from django.urls import path

from .views import ReportMainView, ReportExposureView, ReportDashView

app_name = "reports"

urlpatterns = [
    path("report/", view=ReportMainView, name="reports"),
    path("report/dash", view=ReportDashView, name="reports_dash"),
    path("report/exposure", view=ReportExposureView, name="report_exposure"),
]
