from django.http import JsonResponse
from App.account.models import UserInfo


def check_login(func):
    """
    用于检查是否登录的修饰器
    :param func:
    :return:
    """
    def wrapper(self, request, *args, **kwargs):
        if request.session.get('login') is not None:
            user = getUser(request.session.get('login'))
            '''检测是否为黑名单用户，黑名单用户限制一切功能'''
            if user.user_role == '6':
                return JsonResponse({
                    'errMsg': '账号已被封禁，请联系管理员',
                    'status': False
                }, status=401)
            return func(self, request, *args, **kwargs)
        else:
            return JsonResponse({
                'status': False,
                'errMsg': '你还未登录'
            }, status=401)

    return wrapper


def getUser(email):
    """
    通过获取request的session中email来获取用户对象
    :param email:
    :return:
    """
    return UserInfo.objects.get(email=email)
