from django.urls import path

from apps.users.views import SignUpApiView

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpApiView.as_view(), name='sign_up'),
]
