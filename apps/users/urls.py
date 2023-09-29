from django.urls import path

from apps.users.views import SignUpApiView, VerifyCodeApiView, UserFillingDataApiView

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpApiView.as_view(), name='sign_up'),
    path('verify-code/', VerifyCodeApiView.as_view(), name='verify_code'),
    path('fill-data/', UserFillingDataApiView.as_view(), name='filling_data'),
]
