from django.http import JsonResponse
from django.db.models import Q
from django.utils.timezone import now
from App.MindMap.models import MindMap, MindNode, MindMapCoMember
from rest_framework.views import APIView
from common.userAuthCheck import check_login, getUser
from common.dictInfo import model_to_dict
from datetime import datetime
import json


class MindMapView(APIView):
    FIELDS = [
        'nodeId', 'content', 'parent_node'
    ]

    @check_login
    def post(self, request):
        """
        创建在线导图/本地首次开启共享
        :param request:
        :return:
        """
        try:
            params = request.body
            print(params.decode('utf8', 'ignore'))
            jsonParams = json.loads(params.decode('utf8', 'ignore'))
            user = getUser(email=request.session.get('login'))
            mapId = self.newShareID()
            newMindMap = MindMap.objects.create(
                mapId=mapId,
                mapName=jsonParams.get('name'),
                roomMaster=user,
                roomPassword=jsonParams.get('password')
            )
            node_list = jsonParams.get('node')
            for node in node_list:
                if node['parent_node'] == 0:
                    MindNode.objects.create(
                        nodeId=node['nodeId'],
                        content=node['content'],
                        type='root',
                        parent_node=0,
                        belong_Map=newMindMap  # 导图id可以作为唯一
                    )
                else:
                    MindNode.objects.create(
                        nodeId=node['nodeId'],
                        content=node['content'],
                        type='seed',
                        parent_node=node['parent_node'],
                        belong_Map=newMindMap
                    )
            return JsonResponse({
                'status': True,
                'shareID': newMindMap.mapId,
                'roomMaster': {
                    'name': user.nickname,
                    'id': user.id
                }
            })
        except Exception as e:
            print(e)

    @check_login
    def get(self, request, shareID):
        """
        获取在线导图详细
        :param request:
        :param shareID:
        :return:
        """
        mindmap = MindMap.objects.filter(mapId=shareID)
        if not mindmap.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '导图不存在'
            }, status=404)
        mindmap = mindmap[0]
        mind_node_obj = MindNode.objects.filter(belong_Map=mindmap)
        # 获取在线导图节点信息
        mind_node_dict = [model_to_dict(obj, fields=self.FIELDS) for obj in mind_node_obj]
        # 获取权限信息
        user = getUser(request.session.get('login'))
        if user == mindmap.roomMaster:  # 导图创建者
            auth = 'rw'
        else:
            coMember = MindMapCoMember.objects.filter(
                Q(map=mindmap) &
                Q(user=user)
            )
            if not coMember.exists():
                # 对导图没有权限
                return JsonResponse({
                    'status': True,
                    'errMsg': '你对该导图没有权限'
                }, status=401)
            auth = coMember.auth
        return JsonResponse({
            'status': True,
            'shareId': shareID,
            'name': mindmap.mapName,
            'roomMaster': {
                'name': mindmap.roomMaster.nickname,
                'id': mindmap.roomMaster.id
            },
            'auth': auth,
            'node': mind_node_dict
        })

    @check_login
    def put(self, request, shareID):
        """
        再次开启共享
        :param request:
        :param shareID:
        :return:
        """
        mindmap = MindMap.objects.filter(mapId=shareID)
        if not mindmap.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '导图不存在'
            }, status=404)
        mindmap = mindmap[0]
        user = getUser(email=request.session.get('login'))
        if mindmap.roomMaster != user:
            return JsonResponse({
                'status': False,
                'errMsg': '你不是导图所有者，不能进行操作'
            }, status=401)
        params = request.body
        jsonParams = json.loads(params.decode('utf-8'))
        # 删除原来所有的node
        MindNode.objects.filter(belong_Map=mindmap).delete()
        # 修改导图信息
        mindmap.mapName = jsonParams.get('mapName')
        if jsonParams.get('password') is not None:
            mindmap.roomPassword = jsonParams.get('password')
        mindmap.last_mod_date = now()
        mindmap.shareStatus = True
        # 处理更新的node
        nodeList = jsonParams.get('node')
        for node in nodeList:
            MindNode.objects.create(
                nodeId=node['nodeId'],
                content=node['content'],
                type='seed',
                parent_node=node['parent_node'],
                belong_Map=mindmap
            )
        mindmap.save()
        return JsonResponse({
            'status': True,
            'shareID': mindmap.mapId,
            'roomMaster': {
                'name': user.nickname,
                'id': user.id
            }
        })

    @check_login
    def delete(self, request, shareID):
        """
        删除在线导图
        :param request:
        :param shareID:
        :return:
        """
        mindmap = MindMap.objects.filter(mapId=shareID)
        if not mindmap.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '导图不存在'
            }, status=404)
        mindmap = mindmap[0]
        user = getUser(email=request.session.get('login'))
        if mindmap.roomMaster != user:
            return JsonResponse({
                'status': False,
                'errMsg': '你不是导图所有者，不能进行操作'
            }, status=401)
        MindNode.objects.filter(belong_Map=mindmap).delete()
        mindmap.delete()
        return JsonResponse({
            'status': True,
            'shareID': shareID,
            'mapName': mindmap.mapName,
            'roomMaster': {
                'name': user.nickname,
                'id': user.id
            }
        })

    def newShareID(self):
        now = datetime.now()
        shareId = int(str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second))
        return shareId
