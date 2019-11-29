from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReportsConfig(AppConfig):
    name = "csci_2019_project.reports"
    verbose_name = _("Reports")

    def ready(self):
        try:
            import csci_2019_project.reports.signals  # noqa F401
        except ImportError:
            pass
