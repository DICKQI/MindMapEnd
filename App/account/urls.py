from django.urls import path
from .views import AccountRegisterView, AccountBaseView

app_name = 'Account'
urlpatterns = [
    path('', AccountBaseView.as_view(), name='login_logout_checkLogin'),  # 登录登出检查登录
    path('register/', AccountRegisterView.as_view(), name='register'),  # 注册账号
]
