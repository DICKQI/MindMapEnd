from rest_framework.views import APIView
from App.account.models import UserInfo, UserPassword
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from common.userAuthCheck import getUser, check_login
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

    @check_login
    def delete(self, request):
        """
        登出
        :param request:
        :return:
        """
        user = getUser(email=request.session.get('login'))
        request.session['login'] = None
        return JsonResponse({
            'status': True,
            'id': user.id
        })


class AccountRegisterView(APIView):

    def post(self, request):
        """
        注册账号
        :param request:
        :return:
        """
        params = request.body
        jsonParams = json.loads(params.decode('utf-8'))
        if jsonParams.get('email') is None:
            return JsonResponse({
                'status': False,
                'errMsg': "邮箱不能为空"
            }, status=401)
        if UserInfo.objects.filter(email__exact=jsonParams.get('email')).exists():
            return JsonResponse({
                'status': False,
                'errMsg': '邮箱已存在'
            }, status=401)
        if jsonParams.get('nickname') is None:
            return JsonResponse({
                'status': False,
                'errMsg': "昵称不能为空"
            }, status=401)
        if UserInfo.objects.filter(nickname=jsonParams.get('nickname')).exists():
            return JsonResponse({
                'status': False,
                'errMsg': '昵称已存在'
            }, status=401)
        if jsonParams.get('password') is None:
            return JsonResponse({
                'status': False,
                'errMsg': '密码不能为空'
            })
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
