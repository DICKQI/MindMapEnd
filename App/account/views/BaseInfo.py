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
        # 内容检测
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
            }, status=401)
        hash_password = make_password(jsonParams.get('password'))
        newPassword = UserPassword.objects.create(password=hash_password)
        newAccount = UserInfo.objects.create(
            email=jsonParams.get('email'),
            nickname=jsonParams.get('nickname'),
            password=newPassword,
            head=self.defaultHead
        )
        return JsonResponse({
            'status': True,
            'id': newAccount.id,
            'email': newAccount.email,
            'nickname': newAccount.nickname
        })

    defaultHead = 'data:image/png;base64,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'
