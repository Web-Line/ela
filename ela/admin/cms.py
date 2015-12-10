from ela.sites import main_admin_site
from cms.models import Page, UserSettings
from cms.admin.pageadmin import PageAdmin
from cms.admin.settingsadmin import SettingsAdmin


# cms.admin.pageadmin
main_admin_site.register(Page, PageAdmin)

# cms.admin.permissionadmin

# we should work on these later. when we want to setup permissions for cms.
# it's not the right time now.

# if get_cms_setting('PERMISSION'):
#     main_admin_site.site.register(
#         GlobalPagePermission,
#         GlobalPagePermissionAdmin)
#     PERMISSION_ADMIN_INLINES.extend([
#         ViewRestrictionInlineAdmin,
#         PagePermissionInlineAdmin,
#     ])

# cms.admin.placeholderadmin
# there is no ModelAdmin registered there.

# cms.admin.settingsadmin
main_admin_site.register(UserSettings, SettingsAdmin)

