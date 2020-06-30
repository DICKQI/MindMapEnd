from django.db import models
from App.account.models import UserInfo
from django.utils.timezone import now


# Create your models here.


class MindMap(models.Model):
    mapId = models.BigIntegerField(verbose_name='导图id', primary_key=True, blank=False, unique=True)  # 同样作为shareID

    mapName = models.CharField(verbose_name='导图名', max_length=100, default='', blank=False)

    roomMaster = models.ForeignKey(UserInfo, verbose_name='导图创建人', on_delete=models.CASCADE, blank=False, default='')

    roomPassword = models.CharField(verbose_name='导图密码', max_length=20, blank=False, default='')

    shareStatus = models.BooleanField(verbose_name='共享状态', default=True)

    create_date = models.DateTimeField(verbose_name='创建时间', default=now)

    last_mod_date = models.DateTimeField(verbose_name='最后修改时间', default=now)

    def __str__(self):
        return str(self.mapId)

    class Meta:
        verbose_name = '线上导图'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'MindMap_room'
        ordering = ['-last_mod_date']


class MindNode(models.Model):
    type = (
        ('root', '根节点'),
        ('seed', '子节点')
    )

    # nodeId = models.BigIntegerField(verbose_name='节点id', primary_key=True, blank=False, unique=True)
    nodeId = models.BigIntegerField(verbose_name='导图节点id', blank=False, unique=False, default=0)

    content = models.CharField(verbose_name='节点内容', max_length=100, default='', blank=True, null=True)  # 节点内容同时作为节点名

    type = models.CharField(verbose_name='节点类型', max_length=20, choices=type, default='root')

    parent_node = models.BigIntegerField(verbose_name='节点的父节点', blank=True, default=0)  # 根节点没有父结点

    belong_Map = models.ForeignKey(MindMap, verbose_name='所属导图', on_delete=models.CASCADE, blank=False, default='')

    # belong_Map = models.(MindMap, verbose_name='所属导图', on_delete=models.CASCADE, blank=False, default='')

    def __str__(self):
        return str(self.nodeId)

    class Meta:
        verbose_name = '节点'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'MindMap_node'


class MindMapCoMember(models.Model):
    """导图协作成员"""

    auth_choose = (
        ('ro', '只读'),
        ('rw', '读写')
    )

    map = models.ForeignKey(MindMap, verbose_name='关联导图', default='', blank=False, on_delete=models.CASCADE)

    user = models.ForeignKey(UserInfo, verbose_name='协作用户', default='', blank=False, on_delete=models.CASCADE)

    auth = models.CharField(verbose_name='用户权限', default='ro', blank=False, choices=auth_choose, max_length=100)

    def __str__(self):
        return self.user.nickname

    class Meta:
        verbose_name = '导图协作关系'
        verbose_name_plural = verbose_name + '列表'
        db_table = 'MindMap_CoMember'
