# from django.shortcuts import render
# from wuser.models import User
# from django.shortcuts import get_object_or_404
# from django.core.exceptions import PermissionDenied
# from django.utils.translation import ugettext_lazy as _
#
#
# # Create your views here.
# def confirm_email(request, user_id, key):
#     """
#      get user and confirmed_key to confirm and activate user (is_active)
#     """
#     user = get_object_or_404(User, pk=user_id)
#     if user.is_confirmed:
#         return render(request, template_name='admin/base_site.html', context={
#             'messages': [_("Your email: {} has been already confirmed!"
#                            .format(user.email))], 'is_popup': True})
#     else:
#         try:
#             user.confirm_email(key, save=False)
#         except:
#             raise PermissionDenied
#         user.is_active = True
#         user.save()

from account.views import SignupView as AccountSignupView
from wuser.forms import SignupForm
from wuser.models import UserProfile


class SignupView(AccountSignupView):
    form_class = SignupForm

    def update_profile(self, form):
        UserProfile.objects.create(
            user=self.created_user,
            birthdate=form.cleaned_data["birthdate"],
            fathers_name=form.cleaned_data["fathers_name"],
        )

    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)