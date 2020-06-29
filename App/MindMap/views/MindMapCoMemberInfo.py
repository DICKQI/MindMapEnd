from rest_framework.views import APIView
from App.MindMap.models import MindMap, MindMapCoMember
from django.http import JsonResponse
from common.userAuthCheck import check_login, getUser
from django.db.models import Q
import json


class MindMapCoInfoView(APIView):

    @check_login
    def post(self, request, shareID):
        """
        加入导图协作
        :param request:
        :param shareID:
        :return:
        """
        params = request.body
        jsonParams = json.loads(params.decode('utf-8'))
        mindMap = MindMap.objects.filter(mapId=shareID)
        if not mindMap.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '导图不存在'
            }, status=404)
        mindMap = mindMap[0]
        user = getUser(email=request.session.get("login"))
        if mindMap.roomMaster == user:
            return JsonResponse({
                'status': False,
                'errMsg': '你是导图所有者'
            }, status=401)
        if MindMapCoMember.objects.filter(
                Q(map=mindMap) &
                Q(user=user)
        ).exists():
            return JsonResponse({
                'status': False,
                'errMsg': '你已经是导图协作成员了'
            }, status=401)
        if not mindMap.roomPassword == jsonParams.get('password', ''):
            return JsonResponse({
                'status': False,
                'errMsg': '密码错误'
            }, status=401)
        MindMapCoMember.objects.create(
            map=mindMap,
            user=user,
            auth='rw'
        )
        return JsonResponse({
            'status': False,
            'shareID': shareID,
            'user': {
                'name': user.nickname,
                'id': user.id
            },
            'mapName': mindMap.mapName,
            'roomMaster': {
                'name': mindMap.roomMaster.nickname,
                'id': mindMap.roomMaster.id
            }
        })

    @check_login
    def delete(self, request, shareID):
        """
        退出导图协作
        :param request:
        :param shareID:
        :return:
        """
        mindMap = MindMap.objects.filter(mapId=shareID)
        if not mindMap.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '导图不存在'
            }, status=404)
        mindMap = mindMap[0]
        user = getUser(email=request.session.get("login"))
        if mindMap.roomMaster == user:
            return JsonResponse({
                'status': False,
                'errMsg': '你是导图所有者'
            }, status=401)
        coMember = MindMapCoMember.objects.filter(
            Q(map=mindMap) &
            Q(user=user)
        )
        if not coMember.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '你还不是导图的协作成员'
            }, status=401)
        coMember = coMember[0]
        coMember.delete()
        return JsonResponse({
            'status': False,
            'shareID': shareID,
            'mapName': mindMap.mapName
        })
