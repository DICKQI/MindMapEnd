from rest_framework.views import APIView
from App.MindMap.models import MindMap, MindMapCoMember, MindNode
from django.http import JsonResponse
from common.userAuthCheck import check_login, getUser
from django.db.models import Q
import json


class MindMapNodeInfoView(APIView):

    @check_login
    def post(self, request, mapID, parent_id):
        """
        新建节点
        :param request:
        :param mapID:
        :param parent_id:
        :return:
        """
        user = getUser(request.session.get('login'))
        mindMap = MindMap.objects.filter(mapId=mapID)
        if not mindMap.exists():
            return JsonResponse({
                'status': False,
                'errMsg': "导图不存在"
            }, status=404)
        mindMap = mindMap[0]
        if not mindMap.shareStatus:
            return JsonResponse({
                'status': False,
                'errMsg': '导图未开启共享功能'
            }, status=401)
        if not mindMap.roomMaster == user:
            coRelation = MindMapCoMember.objects.filter(
                Q(map=mindMap) &
                Q(user=user)
            )
            if not coRelation.exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '你对该导图没有权限'
                }, status=403)
            elif coRelation[0].auth == 'ro':
                return JsonResponse({
                    'status': False,
                    'errMsg': '你对改导图没有修改权限'
                }, status=403)
        if not MindNode.objects.filter(
            Q(nodeId=parent_id) &
            Q(belong_Map=mindMap)
        ).exists():
            return JsonResponse({
                'status': False,
                'errMsg': '父节点不存在'
            }, status=404)
        params = request.body
        jsonParams = json.loads(params.decode('utf-8'))
        newNode = MindNode.objects.create(
            content=jsonParams.get('content', ''),
            type='seed',
            parent_node=parent_id,
            belong_Map=mindMap,
            nodeId=self.newNodeID()
        )
        return JsonResponse({
            'status': True,
            'nodeId': newNode.nodeId,
            'parent_node': parent_id,
            'map': mindMap.mapId
        })

    @check_login
    def put(self, request, mapID, nodeID):
        """
        修改节点信息
        :param request:
        :param mapID:
        :param nodeID:
        :return:
        """
        user = getUser(request.session.get('login'))
        mindMap = MindMap.objects.filter(mapId=mapID)
        if not mindMap.exists():
            return JsonResponse({
                'status': False,
                'errMsg': "导图不存在"
            }, status=404)
        mindMap = mindMap[0]
        if not mindMap.shareStatus:
            return JsonResponse({
                'status': False,
                'errMsg': '导图未开启共享功能'
            }, status=401)
        if not mindMap.roomMaster == user:
            coRelation = MindMapCoMember.objects.filter(
                Q(map=mindMap) &
                Q(user=user)
            )
            if not coRelation.exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '你对该导图没有权限'
                }, status=403)
            elif coRelation[0].auth == 'ro':
                return JsonResponse({
                    'status': False,
                    'errMsg': '你对改导图没有修改权限'
                }, status=403)
        node = MindNode.objects.filter(
            Q(nodeId=nodeID) &
            Q(belong_Map=mindMap)
        )
        if not node.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '该节点不存在'
            }, status=404)
        node = node[0]
        params = request.body
        jsonParams = json.loads(params.decode('utf-8'))
        if jsonParams.get('content') is not None:
            node.content = jsonParams.get('content')
        node.save()
        return JsonResponse({
            'status': True,
            'nodeID': node.nodeId,
            'parent_node': node.parent_node,
            'content': node.content,
            'mapID': mindMap.mapId
        })

    def delete(self, request, mapID, nodeID):
        """
        删除节点及其子节点
        :param request:
        :param mapID:
        :param nodeID:
        :return:
        """
        user = getUser(request.session.get('login'))
        mindMap = MindMap.objects.filter(mapId=mapID)
        if not mindMap.exists():
            return JsonResponse({
                'status': False,
                'errMsg': "导图不存在"
            }, status=404)
        mindMap = mindMap[0]
        if not mindMap.shareStatus:
            return JsonResponse({
                'status': False,
                'errMsg': '导图未开启共享功能'
            }, status=401)
        if not mindMap.roomMaster == user:
            coRelation = MindMapCoMember.objects.filter(
                Q(map=mindMap) &
                Q(user=user)
            )
            if not coRelation.exists():
                return JsonResponse({
                    'status': False,
                    'errMsg': '你对该导图没有权限'
                }, status=403)
            elif coRelation[0].auth == 'ro':
                return JsonResponse({
                    'status': False,
                    'errMsg': '你对改导图没有修改权限'
                }, status=403)
        node = MindNode.objects.filter(
            Q(nodeId=nodeID) &
            Q(belong_Map=mindMap)
        )
        if not node.exists():
            return JsonResponse({
                'status': False,
                'errMsg': '该节点不存在'
            }, status=404)
        node = node[0]
        sonNode = MindNode.objects.filter(
            Q(parent_node=node.nodeId) &
            Q(belong_Map=mindMap)
        )
        # 删除所有的子节点
        sonNode.delete()
        node.delete()
        return JsonResponse({
            'status': True,
            'nodeID': nodeID
        })

    def newNodeID(self):
        from datetime import datetime
        now = datetime.now()
        nodeId = int(str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second))
        return nodeId
