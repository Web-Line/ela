from suit.templatetags.suit_menu import Menu
from django.core.handlers.wsgi import WSGIRequest
from django import template
from django.core.urlresolvers import NoReverseMatch

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_menu_patch(context, request):
    """
    :type request: WSGIRequest
    """
    if not isinstance(request, WSGIRequest):
        return None

    # Try to get app list
    try:
        template_response = get_admin_site(context.current_app).index(request)
    except NoReverseMatch:
        # Django 1.8 uses request.current_app instead of context.current_app

        template_response = get_admin_site(request).index(request)

    try:
        app_list = template_response.context_data['app_list']
    except Exception:
        return

    return Menu(context, request, app_list).get_app_list()


def get_admin_site(current_app):
    """
    Method tries to get actual admin.site class, if any custom admin sites
    were used. Couldn't find any other references to actual class other than
    in func_closer dict in index() func returned by resolver.
    """
    """
    This is a bug in suit library. Here is a solve for that.
    suit can't find custom registered admin site properly, so we have to give it
    manually.
    """
    from ela.sites import main_admin_site
    return main_admin_site

#    resolver_match = resolve(reverse('%s:index' % current_app))
#    logger.debug("resolver_match={}".format(resolver_match.func().func_closure))
#    for func_closure in resolver_match.func.func_closure:
#        if isinstance(func_closure.cell_contents, AdminSite):
#            return func_closure.cell_contents
#    return admin.site
