from itertools import chain
from django.db.models.fields.related import ManyToManyField, ForeignKey
from django.db.models.fields import DateTimeField


def model_to_dict(instance, fields=None, exclude=None, *args, **kwargs):
    """
        改造django.forms.models.model_to_dict()方法
        :param instance:
        :type instance: django.db.models.Model
        :param fields:  成员名称白名单（设置时将按这个名单为准，否则输出全部）
        :param exclude: 成员名称黑名单
        :return:
        为了使外键展开，ManyToMany键展开
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        value = f.value_from_object(instance)
        if not getattr(f, 'editable', False):
            continue
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        if isinstance(f, DateTimeField):
            value = formatDatetime(value)
        data[f.name] = value
    return data


def formatDatetime(value):
    data_time = str(value)
    year = data_time[0:4]
    month = data_time[5:7]
    day = data_time[8:10]
    hour = data_time[11:13]
    min = data_time[14:16]
    sec = data_time[17:19]
    value = year + "-" + month + "-" + day + " " + hour + ":" + min + ":" + sec
    return value
