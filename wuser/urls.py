from django.conf.urls import url
from wuser import views

#
# urlpatterns = [
#     url(r'^confirm-email/user(?P<user_id>[0-9]+)/(?P<key>[0-9]+)$',
#         views.confirm_email, name='confirm-email'),
#
# ]

from django.conf.urls import url
from wuser.views import (SignupView, LoginView)


urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name="account_signup"),
    url(r'^login/$', LoginView.as_view(), name="account_login"),
]