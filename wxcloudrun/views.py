import json
import logging

from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from wxcloudrun.models import Counters,Markers
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """

    return render(request, 'index.html')


def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """
    #
    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        logger.info('update_count req: {}'.format(request.body))
        #logger.info('update_count req: start:{}'.format(request.GET['start']))
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' in body:
        if body['action'] == 'inc':
            try:
                data = Counters.objects.get(id=1)
            except Counters.DoesNotExist:
                data = Counters()
            data.id = 1
            data.count += 1
            data.save()
            return JsonResponse({'code': 0, "data": data.count},
                        json_dumps_params={'ensure_ascii': False})
        elif body['action'] == 'clear':
            try:
                data = Counters.objects.get(id=1)
                data.delete()
            except Counters.DoesNotExist:
                logger.info('record not exist')
            return JsonResponse({'code': 0, 'data': 0},
                        json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                        json_dumps_params={'ensure_ascii': False})
    elif 'MsgType' in body:
        if body['MsgType'] == 'location':
            #更新位置信息
            data=Markers()
            data.userid=body['FromUserName']
            data.longtitude=body['Location_Y']
            data.latitude=body['Location_X']
            data.memo=body['Label']
            data.updatedAt=datetime.now()
            data.save()
            return JsonResponse({'marked': 1, "data": data.id},
                        json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'code': -1, 'errorMsg': '暂不解析其他消息'},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action/msgType参数'},
                    json_dumps_params={'ensure_ascii': False})
   

'''
{
    "ToUserName": "gh_d1031e52fbba",
    "FromUserName": "obv5P5rjGYxf06h5kfvCeIqw-mD0",
    "CreateTime": 1639716843,
    "MsgType": "location",
    "Location_X": 20.028543,
    "Location_Y": 110.313248,
    "Scale": 15,
    "Label": "\xe9\xbe\x99\xe5\x8d\x8e\xe5\x8c\xba\xe6\xbb\xa8\xe6\xb5\xb7\xe5\xa4\xa7\xe9\x81\x9389\xe5\x8f\xb7",
    "MsgId": 23475101167457529
    }
'''

def search(request, _):
    if request.method == "GET":  # 如果是翻页将会进入到get方式中
        name = request.GET.get('name')
         # 进行数据库查询
        content = Markers.objects.filter(~Q(userid=name))#这里返回的是多条数据
        #logger.info('update_count req:name: {}'.format(content))
        ## contentj = model_to_dict(content)
        # return HttpResponse(json.dumps(contentj),content_type="application/json")
        #print(content)
        if content.exists():
           paginator = Paginator(content, 30)   # 每页显示5条
           try:
                 num = request.GET.get('index', 1)  # 页面连接，用于翻页
                 number = paginator.page(num)
           except PageNotAnInteger:
                 number = paginator.page(1)
           except EmptyPage:
                 number = paginator.page(paginator.num_pages)
           return render(request,'first.html',{'paginator':paginator})
        return render(request,'first.html')

    else:
        name = request.POST.get('name')
        request.session['name'] = name   # POST 方式中用于接收前台数据并存入session
        # 进行数据库查询
        content = Markers.objects.filter(~Q(userid=name))#这里返回的是多条数据
        if content.exists():
              paginator = Paginator(content, 30)   # 每页显示5条
              try:
                 num = request.GET.get('index', 1)  # 页面连接，用于翻页
                 number = paginator.page(num)
              except PageNotAnInteger:
                 number = paginator.page(1)
              except EmptyPage:
                 number = paginator.page(paginator.num_pages)
              return render(request,'first.html',{'paginator':paginator})
        return render(request,'first.html')