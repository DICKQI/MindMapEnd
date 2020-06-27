from rest_framework.views import APIView
from App.MindMap.models import MindMap, MindMapCoMember
from django.http import JsonResponse
from common.userAuthCheck import check_login, getUser
from common.dictInfo import model_to_dict
from django.db.models import Q


class MindMapListView(APIView):
    FIELDS = [
        'mapId', 'mapName', 'roomMaster__nickname', 'create_date', 'last_mod_date'
    ]

    @check_login
    def get(self, request):
        """
        获取在线导图列表
        :param request:
        :return:
        """
        user = getUser(request.session.get('login'))
        coMap = MindMapCoMember.objects.filter(user=user)
        coMapList = [co.map_id for co in coMap]
        masterMap = MindMap.objects.filter(roomMaster=user)
        coMap = MindMap.objects.filter(mapId__in=coMapList)
        dict1 = [model_to_dict(mapobj, fields=self.FIELDS) for mapobj in masterMap]
        for di in dict1:
            di['auth'] = 'rw'
        dict2 = [model_to_dict(mapobj, fields=self.FIELDS) for mapobj in coMap]
        for di in dict2:
            di['auth'] = MindMapCoMember.objects.get(
                Q(map_id=di['mapId']) &
                Q(user=user)
            ).auth
        mapDict = dict1 + dict2
        return JsonResponse({
            'status': True,
            'mapList': mapDict
        })
