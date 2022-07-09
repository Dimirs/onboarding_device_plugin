"""Plugin additions to the NetBox navigation menu."""

from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link="plugins:onboarding_device_plugin:onboardingtask_list",
        link_text="Onboarding Tasks",
        buttons=(
            PluginMenuButton(
                link="plugins:onboarding_device_plugin:onboardingtask_add",
                title="Onboard",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
            ),
            PluginMenuButton(
                link="plugins:onboarding_device_plugin:onboardingtask_import",
                title="Bulk Onboard",
                icon_class="mdi mdi-database-import-outline",
		color=ButtonColorChoices.BLUE,
            ),
        ),
    ),
)
