"""Forms for network device onboarding."""

from django import forms
from django.db import transaction
from django_rq import get_queue


from dcim.models import Site, Platform, DeviceRole, DeviceType

from .models import OnboardingTask
from .choices import OnboardingStatusChoices, OnboardingFailChoices
from .utils.credentials import Credentials
from utilities.forms import (
    DynamicModelChoiceField,
    CSVModelChoiceField,
)
from netbox.forms import NetBoxModelForm, NetBoxModelCSVForm, NetBoxModelFilterSetForm



BLANK_CHOICE = (("", "---------"),)

class OnboardingTaskForm(NetBoxModelForm, forms.ModelForm):
    """Form for creating a new OnboardingTask instance."""

    ip_address = forms.CharField(
        required=True, label="IP address", help_text="IP Address/DNS Name of the device to onboard"
    )

    site = DynamicModelChoiceField(required=True, queryset=Site.objects.all())

    username = forms.CharField(required=False, help_text="Device username (will not be stored in database)")
    password = forms.CharField(
        required=False, widget=forms.PasswordInput, help_text="Device password (will not be stored in database)"
    )
    secret = forms.CharField(
        required=False, widget=forms.PasswordInput, help_text="Device secret (will not be stored in database)"
    )

    platform = DynamicModelChoiceField(
        queryset=Platform.objects.all(),
        required=False,
        to_field_name="slug",
        help_text="Device platform. Define ONLY to override auto-recognition of platform.",
    )
    role = DynamicModelChoiceField(
        queryset=DeviceRole.objects.all(),
        required=False,
        to_field_name="slug",
        help_text="Device role. Define ONLY to override auto-recognition of role.",
    )
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        to_field_name="slug",
        help_text="Device type. Define ONLY to override auto-recognition of type.",
    )

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        model = OnboardingTask
        fields = [
            "site",
            "ip_address",
            "port",
            "timeout",
            "username",
            "password",
            "secret",
            "platform",
            "role",
            "device_type",
        ]

    def save(self, commit=True, **kwargs):
        """Save the model, and add it and the associated credentials to the onboarding worker queue."""
        model = super().save(commit=commit, **kwargs)
        if commit:
            credentials = Credentials(self.data.get("username"), self.data.get("password"), self.data.get("secret"))
            get_queue("default").enqueue("onboarding_device_plugin.worker.onboard_device", model.pk, credentials)
        return model




class OnboardingTaskFilterForm(NetBoxModelFilterSetForm, forms.ModelForm):
    """Form for filtering OnboardingTask instances."""

    site = DynamicModelChoiceField(queryset=Site.objects.all(), required=False, to_field_name="slug")

    platform = DynamicModelChoiceField(queryset=Platform.objects.all(), required=False, to_field_name="slug")

    status = forms.ChoiceField(choices=BLANK_CHOICE + OnboardingStatusChoices.CHOICES, required=False)

    failed_reason = forms.ChoiceField(
        choices=BLANK_CHOICE + OnboardingFailChoices.CHOICES, required=False, label="Failed Reason"
    )

    q = forms.CharField(required=False, label="Search")

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        model = OnboardingTask
        fields = ["q", "site", "platform", "status", "failed_reason"]


class OnboardingTaskFeedCSVForm(NetBoxModelCSVForm):
    """Form for entering CSV to bulk-import OnboardingTask entries."""

    site = CSVModelChoiceField(
        queryset=Site.objects.all(),
        required=True,
        to_field_name="slug",
        help_text="Slug of parent site",
        error_messages={"invalid_choice": "Site not found",},
    )
    ip_address = forms.CharField(required=True, help_text="IP Address of the onboarded device")
    username = forms.CharField(required=False, help_text="Username, will not be stored in database")
    password = forms.CharField(required=False, help_text="Password, will not be stored in database")
    secret = forms.CharField(required=False, help_text="Secret password, will not be stored in database")
    platform = CSVModelChoiceField(
        queryset=Platform.objects.all(),
        required=False,
        to_field_name="slug",
        help_text="Slug of device platform. Define ONLY to override auto-recognition of platform.",
        error_messages={"invalid_choice": "Platform not found.",},
    )
    port = forms.IntegerField(required=False, help_text="Device PORT (def: 22)",)

    timeout = forms.IntegerField(required=False, help_text="Device Timeout (sec) (def: 30)",)

    role = CSVModelChoiceField(
        queryset=DeviceRole.objects.all(),
        required=False,
        to_field_name="slug",
        help_text="Slug of device role. Define ONLY to override auto-recognition of role.",
        error_messages={"invalid_choice": "DeviceRole not found",},
    )

    device_type = CSVModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        to_field_name="slug",
        help_text="Slug of device type. Define ONLY to override auto-recognition of type.",
        error_messages={"invalid_choice": "DeviceType not found",},
    )

    class Meta:  # noqa: D106 "Missing docstring in public nested class"
        model = OnboardingTask
        fields = [
            "site",
            "ip_address",
            "port",
            "timeout",
            "platform",
            "role",
        ]

    def save(self, commit=True, **kwargs):
        """Save the model, and add it and the associated credentials to the onboarding worker queue."""
        model = super().save(commit=commit, **kwargs)
        if commit:
            credentials = Credentials(self.data.get("username"), self.data.get("password"), self.data.get("secret"))
            transaction.on_commit(
                lambda: get_queue("default").enqueue("onboarding_device_plugin.worker.onboard_device", model.pk, credentials)
            )
        return model
