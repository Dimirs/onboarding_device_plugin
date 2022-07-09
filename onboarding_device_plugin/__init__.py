"""Plugin declaration for netbox_onboarding."""


__version__ = '0.1.0'


from extras.plugins import PluginConfig


class OnboardingConfig(PluginConfig):
    """Plugin configuration for the netbox_onboarding plugin."""

    name = "onboarding_device_plugin"
    verbose_name = "Device Onboarding"
    version = __version__
    author = "Aslanov D.M."
    description = "A plugin for NetBox to easily onboard new devices."
    base_url = "onboarding"
    required_settings = []
    default_settings = {
        "create_platform_if_missing": True,
        "create_manufacturer_if_missing": True,
        "create_device_type_if_missing": True,
        "create_device_role_if_missing": True,
        "default_device_role": "network",
        "default_device_role_color": "FF0000",
        "default_management_interface": "PLACEHOLDER",
        "default_management_prefix_length": 0,
        "default_device_status": "active",
        "create_management_interface_if_missing": True,
        "skip_device_type_on_update": False,
        "skip_manufacturer_on_update": False,
        "platform_map": {},
        "onboarding_extensions_map": {"ios": "netbox_onboarding.onboarding_extensions.ios",},
        "object_match_strategy": "loose",
    }


config = OnboardingConfig




