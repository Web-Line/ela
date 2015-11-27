from django.shortcuts import render
from models import User
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _


# Create your views here.
def confirm_email(request, id, key):
    user = get_object_or_404(User, pk=id)
    if user.is_confirmed:
        return render(request, template_name='admin/base_site.html', context={
            'messages': [_("Your email: {} has been already confirmed!"
                           .format(user.email))], 'is_popup': True})
    else:
        try:
            user.confirm_email(key, save=False)
        except:
            raise PermissionDenied
        user.is_active = True
        user.save()