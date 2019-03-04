import os
import random
import json
import time
from django.shortcuts import render
from django.http import *
from ui.models import *
from django.db.models import *
import ui.mg as mg
import ui.page_history as history


# 显示指定序列号的PCS
def show_pcs_page(request, pcs_sn):
    context = {}
    context['request'] = request
    context['pcs_id'] = pcs_sn
    context['pcs_name'] = "%d#PCS" % (pcs_sn + 1)
    context['pcs'] = mg.get_pcs_yaoce(pcs_sn)
    context['type'] = 'pcs'
    return render(request, "pcs/PCS数据模板.html", context=context)


yaotiao_black_list = {"状态标志位"}


# PCS遥调页面
def show_pcs_yaotiao_page(request, pcs_sn):
    if request.method == 'POST':
        X = {key: value for key, value in request.POST.items()}
        if "系统时钟" in X:
            x = request.POST['系统时钟']
            t = [int(x[0:4], 10), int(x[4: 6], 10), int(x[6: 8], 10),
                                  int(x[8: 10], 10), int(x[10: 12], 10), int(x[12: 14], 10)]
            X['系统时钟'] = t
        success = mg.set_pcs_yaotiao(pcs_sn, X, str(request.user))
    else:
        success = True

    yaotiao = mg.get_pcs_yaotiao(pcs_sn)
    yaotiao_list = mg.filter_api_yaotiao(yaotiao, blacklist=yaotiao_black_list, column=2)

    context = {
        "request": request,
        "success": success,
        "pcs_id": pcs_sn,
        "type": "pcs",
        "pcs_name": "%d#PCS" % (pcs_sn + 1),
        "yaotiao_list": yaotiao_list,
    }

    context['type'] = 'yaotiao'
    return render(request, "pcs/PCS遥调模板.html", context=context)


# PCS遥控页面
def show_pcs_yaokong_page(request, pcs_sn):
    context = {}

    if len(request.GET) >= 1:
        for key, value in request.GET.items():
            success = mg.set_pcs_yaokong(pcs_sn, key, int(value), str(request.user))
            context['success'] = success
            context['show_result'] = True
            break # 每次只允许设置一个值

    config_json = None
    try:
        with open("data/PCS遥控选项表.txt", "r") as options:
            config_json = json.load(options)
    except Exception as e:
        config_json = None

    yaokong = mg.get_pcs_yaokong(pcs_sn)
    yaokong_list = []
    for key, value in yaokong.items():
        if key in {"状态标志位"}:
            continue

        if config_json is not None and key in config_json:
            options = config_json[key]
            yaokong = {"name": key, "value": value, "options": options}
        else:
            yaokong = {"name": key, "value": value, "options": []}

        yaokong_list.append(yaokong)

    context['request'] = request
    context['pcs_id'] = pcs_sn
    context['type'] = "pcs"
    context['pcs_name'] = "%d#PCS" % (pcs_sn + 1)
    context['yaokong_list'] = yaokong_list
    context['type'] = 'yaokong'

    return render(request, "pcs/PCS遥控模板.html", context=context)
