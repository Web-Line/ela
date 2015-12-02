from account.views import SignupView as AccountSignupView
from .models import UserProfile
from .forms import SignupForm


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
        super(AccountSignupView, self).after_signup(form)