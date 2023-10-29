from django.urls import path

from apps.users.views import SignUpApiView, VerifyCodeApiView, UserFillingDataApiView, LoginAPIView, \
    LoginRefreshApiView, LogOutAPIView, VerifyAgainApiView

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpApiView.as_view(), name='sign_up'),
    path('verify-code/', VerifyCodeApiView.as_view(), name='verify_code'),
    path('new-verify-code/', VerifyAgainApiView.as_view(), name='new_verify_code'),
    path('fill-data/', UserFillingDataApiView.as_view(), name='filling_data'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login-refresh/', LoginRefreshApiView.as_view(), name='login-refresh'),
    path('logout/', LogOutAPIView.as_view(), name='logout'),
]
