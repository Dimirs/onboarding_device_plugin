import logging

from django.shortcuts import get_object_or_404, render



from .filters import OnboardingTaskFilter
from .forms import OnboardingTaskForm, OnboardingTaskFilterForm, OnboardingTaskFeedCSVForm
from .models import OnboardingTask
from .tables import OnboardingTaskTable, OnboardingTaskFeedBulkTable
from netbox.views import generic


logger = logging.getLogger("rq.worker")

# pylint: disable=ungrouped-imports,no-name-in-module

 # ObjectView, BulkDeleteView, BulkImportView, ObjectEditView, ObjectListView

class ReleaseMixinOnboardingTaskView(generic.ObjectView):
        """Release Mixin View for presenting a single OnboardingTask."""

class ReleaseMixinOnboardingTaskListView(generic.ObjectListView):
        """Release Mixin View for listing all extant OnboardingTasks."""

class ReleaseMixinOnboardingTaskCreateView(generic.ObjectEditView):
        """Release Mixin View for creating a new OnboardingTask."""

class ReleaseMixinOnboardingTaskBulkDeleteView(generic.BulkDeleteView):
        """Release Mixin View for deleting one or more OnboardingTasks."""

class ReleaseMixinOnboardingTaskFeedBulkImportView(generic.BulkImportView):
        """Release Mixin View for bulk-importing a CSV file to create OnboardingTasks."""



class OnboardingTaskView(ReleaseMixinOnboardingTaskView):
    """View for presenting a single OnboardingTask."""

    queryset = OnboardingTask.objects.all()

    def get(self, request, pk):  # pylint: disable=invalid-name, missing-function-docstring
        """Get request."""
        instance = get_object_or_404(self.queryset, pk=pk)

        return render(
            request, "onboarding_device_plugin/onboardingtask.html", {"object": instance, "onboardingtask": instance}
        )


class OnboardingTaskListView(ReleaseMixinOnboardingTaskListView):
    """View for listing all extant OnboardingTasks."""

    queryset = OnboardingTask.objects.all().order_by("-id")
    filterset = OnboardingTaskFilter
    filterset_form = OnboardingTaskFilterForm
    table = OnboardingTaskTable
    template_name = "onboarding_device_plugin/onboarding_tasks_list.html"



class OnboardingTaskCreateView(ReleaseMixinOnboardingTaskCreateView):
    """View for creating a new OnboardingTask."""

    model = OnboardingTask
    queryset = OnboardingTask.objects.all()
    model_form = OnboardingTaskForm
    template_name = "onboarding_device_plugin/onboarding_task_edit.html"
    default_return_url = "plugins:onboarding_device_plugin:onboardingtask_list"


class OnboardingTaskBulkDeleteView(ReleaseMixinOnboardingTaskBulkDeleteView):
    """View for deleting one or more OnboardingTasks."""

    queryset = OnboardingTask.objects.filter()  # TODO: can we exclude currently-running tasks?
    table = OnboardingTaskTable
    default_return_url = "plugins:onboarding_device_plugin:onboardingtask_list"


class OnboardingTaskFeedBulkImportView(ReleaseMixinOnboardingTaskFeedBulkImportView):
    """View for bulk-importing a CSV file to create OnboardingTasks."""

    queryset = OnboardingTask.objects.all()
    model_form = OnboardingTaskFeedCSVForm
    table = OnboardingTaskFeedBulkTable
    default_return_url = "plugins:onboarding_device_plugin:onboardingtask_list"
