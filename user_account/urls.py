from django.conf.urls import url
from.views import AcountSignupView


urlpatterns = [
    url(r'^signup/$', AcountSignupView.as_view(), name="account_signup"),
]