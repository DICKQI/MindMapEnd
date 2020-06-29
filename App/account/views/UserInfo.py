from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from App.account.models import UserPassword
from common.dictInfo import model_to_dict
from common.userAuthCheck import check_login, getUser
import json


class UserInfoView(APIView):
    FIELDS = [
        'email', 'nickname', 'join_date', 'sex', 'signature'
    ]

    @check_login
    def get(self, request):
        """
        获取个人信息
        :param request:
        :return:
        """
        user = getUser(email=request.session.get('login'))
        userDict = model_to_dict(user, fields=self.FIELDS)
        return JsonResponse({
            'status': True,
            'user': userDict
        })

    @check_login
    def put(self, request):
        user = getUser(email=request.session.get('login'))
        params = request.body
        jsonParams = json.loads(params.decode('utf-8'))
        if jsonParams.get('nickname') is not None:
            user.nickname = jsonParams.get('nickname')
        if jsonParams.get('sex') is not None:
            user.sex = jsonParams.get('sex')
        if jsonParams.get('signature') is not None:
            user.signature = jsonParams.get('signature')
        user.save()
        userDict = model_to_dict(user, fields=self.FIELDS)
        return JsonResponse({
            'status': True,
            'user': userDict
        })

    @check_login
    def post(self, request):
        user = getUser(email=request.session.get('login'))
        params = request.body
        jsonParams = json.loads(params.decode('utf-8'))
        if jsonParams.get('oldPassword') is None:
            return JsonResponse({
                'status': False,
                'errMsg': '旧密码不能为空'
            }, status=401)
        if jsonParams.get('newPassword') is None:
            return JsonResponse({
                'status': False,
                'errMsg': '新密码不能为空'
            }, status=401)
        if not check_password(jsonParams.get('oldPassword'), user.password.password):
            return JsonResponse({
                'status': False,
                'errMsg': '旧密码不匹配'
            }, status=401)
        newPassword = make_password(jsonParams.get('newPassword'))
        user.password.password = newPassword
        user.password.save()
        return JsonResponse({
            'status': True,
            'user': {
                'id': user.id,
                'nickname': user.nickname
            }
        })


class UserHeadInfoView(APIView):

    @check_login
    def get(self, request):
        """
        获取头像base64
        :param request:
        :return:
        """

    @check_login
    def put(self, request):
        """
        修改头像
        :param request:
        :return:
        """
