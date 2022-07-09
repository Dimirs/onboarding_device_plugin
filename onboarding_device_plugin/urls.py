"""Django urlpatterns declaration for netbox_onboarding plugin."""


from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from .models import OnboardingTask
from .views import (
    OnboardingTaskView,
    OnboardingTaskListView,
    OnboardingTaskCreateView,
    OnboardingTaskBulkDeleteView,
    OnboardingTaskFeedBulkImportView,
)

urlpatterns = [
    path("", OnboardingTaskListView.as_view(), name="onboardingtask_list"),
    path("<int:pk>/", OnboardingTaskView.as_view(), name="onboardingtask"),
    path("add/", OnboardingTaskCreateView.as_view(), name="onboardingtask_add"),
    path("delete/", OnboardingTaskBulkDeleteView.as_view(), name="onboardingtask_bulk_delete"),
    path("import/", OnboardingTaskFeedBulkImportView.as_view(), name="onboardingtask_import"),
    path(
        "<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="onboardingtask_changelog",
        kwargs={"model": OnboardingTask},
    ),
]
