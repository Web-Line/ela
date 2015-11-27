from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^confirm-email/user(?P<user_id>[0-9]+)/(?P<key>[0-9]+)$',
        views.confirm_email, name='confirm-email'),
    
]