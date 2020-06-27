from rest_framework.views import APIView
from App.account.models import UserInfo, UserPassword
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from common.userAuthCheck import getUser
import json


class AccountBaseView(APIView):

    def get(self, request):
        """
        检查是否登录
        :param request:
        :return:
        """
        if request.session.get('login', None):
            return JsonResponse({
                'status': True,
                'id': getUser(request.session.get('login')).id
            })
        else:
            return JsonResponse({
                'status': False,
                'errMsg': '你还未登录'
            }, status=401)

    def post(self, request):
        """
        登录
        :param request:
        :return:
        """
        params = request.body
        jsonParams = json.loads(params.decode('utf-8'))
        user = UserInfo.objects.filter(email=jsonParams.get('email'))
        if not user.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '邮箱不存在'
            }, status=404)
        user = user[0]
        db_password = user.password.password
        if check_password(jsonParams.get('password'), db_password):
            request.session['login'] = user.email
            return JsonResponse({
                'status': True,
                'id': user.id,
                'nickname': user.nickname,
                'email': user.email
            })
        else:
            return JsonResponse({
                'status': False,
                'errMsg': '密码错误'
            }, status=401)


class AccountRegisterView(APIView):

    def post(self, request):
        """
        注册账号
        :param request:
        :return:
        """
        params = request.body
        jsonParams = json.loads(params.decode('utf-8'))
        user = UserInfo.objects.filter(email__exact=jsonParams.get('email'))
        if user.exists():
            return JsonResponse({
                'status': True,
                'errMsg': '邮箱已存在'
            }, status=401)
        hash_password = make_password(jsonParams.get('password'))
        newPassword = UserPassword.objects.create(password=hash_password)
        newAccount = UserInfo.objects.create(
            email=jsonParams.get('email'),
            nickname=jsonParams.get('nickname'),
            password=newPassword
        )
        return JsonResponse({
            'status': True,
            'id': newAccount.id,
            'email': newAccount.email,
            'nickname': newAccount.nickname
        })
