"""Tables for device onboarding tasks."""


import django_tables2 as tables
from .models import OnboardingTask
from netbox.tables import NetBoxTable
from netbox.tables.columns import ChoiceFieldColumn, TagColumn

class OnboardingTaskTable(NetBoxTable):
    """Table for displaying OnboardingTask instances."""

    pk = ChoiceFieldColumn(default=AVAILABLE_LABEL)
    id = tables.LinkColumn()
    site = tables.LinkColumn()
    platform = tables.LinkColumn()
    created_device = tables.LinkColumn()

    class Meta(NetBoxTable.Meta):  # noqa: D106 "Missing docstring in public nested class"
        model = OnboardingTask
        fields = (
            "pk",
            "id",
            "created",
            "ip_address",
            "site",
            "platform",
            "created_device",
            "status",
            "failed_reason",
            "message",
        )


class OnboardingTaskFeedBulkTable(NetBoxTable):
    """TODO document me."""

    site = tables.LinkColumn()

    class Meta(NetBoxTable.Meta):  # noqa: D106 "Missing docstring in public nested class"
        model = OnboardingTask
        fields = (
            "id",
            "created",
            "site",
            "platform",
            "ip_address",
            "port",
            "timeout",
        )




