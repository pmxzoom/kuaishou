from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.db import connection
from django.template import response

from list import billboard, tube, movie
from django.contrib import messages



# Create your views here.#


def btable(request):
    with connection.cursor() as cursor:
        sql = 'select * from list_billboard'
        cursor.execute(sql)
        rows = cursor.fetchall()

    nrows = []

    for row in rows:
        nrows.append(list(row))
    return render(request, 'billboard.html', {'nrows': nrows})


def mtable(request):
    with connection.cursor() as cursor:
        sql = 'select * from list_movie'
        cursor.execute(sql)
        rows = cursor.fetchall()

    nrows = []

    for row in rows:
        nrows.append(list(row))
    return render(request, 'movie.html', {'nrows': nrows})


def ttable(request):
    with connection.cursor() as cursor:
        sql = 'select * from list_tube'
        cursor.execute(sql)
        rows = cursor.fetchall()

    nrows = []

    for row in rows:
        nrows.append(list(row))
    return render(request, 'tube.html', {'nrows': nrows})


def barb(request):
    return render(request, 'billboardBar.html')


def barm(request):
    return render(request, 'movieBar.html')


def bart(request):
    return render(request, 'tubeBar.html')


def wordb(request):
    return render(request, 'billboardWordcloud.html')

def wordm(request):
    return render(request, 'movieWordcloud.html')

def wordt(request):
    return render(request, 'tubeWordcloud.html')

def pieb(request):
    return render(request, 'billboardpie.html')


def piem(request):
    return render(request, 'moviepie.html')


def piet(request):
    return render(request, 'tubepie.html')


def funnelb(request):
    return render(request, 'billboardfunnel.html')


def funnelm(request):
    return render(request, 'moviefunnel.html')


def funnelt(request):
    return render(request, 'tubefunnel.html')



def pictorialbarb(request):
    return render(request, 'billboardpictorialbar.html')


def pictorialbarm(request):
    return render(request, 'moviepictorialbar.html')


def pictorialbart(request):
    return render(request, 'tubepictorialbar.html')


def effectscatterb(request):
    return render(request, 'billboardeffectscatter.html')


def effectscatterm(request):
    return render(request, 'movieeffectscatter.html')


def effectscattert(request):
    return render(request, 'tubeeffectscatter.html')

def allupdate(request):
    billboard.wcsv()
    billboard.wmysql()
    billboard.getdata()
    billboard.draweBar()
    billboard.wtxt()
    billboard.drawWordcloud()
    billboard.drawEffectScatter()
    billboard.drawPictorialBar()
    billboard.drawpie()
    billboard.drawFunnel()
    tube.wcsv()
    tube.wmysql()
    tube.getdata()
    tube.drawecharts()
    tube.wtxt()
    tube.drawWordcloud()
    tube.drawEffectScatter()
    tube.drawPictorialBar()
    tube.drawpie()
    tube.drawFunnel()
    movie.wcsv()
    movie.wmysql()
    movie.getdata()
    movie.draweBar()
    movie.wtxt()
    movie.drawWordcloud()
    movie.drawEffectScatter()
    movie.drawPictorialBar()
    movie.drawpie()
    movie.drawFunnel()
    messages.success(request,'更新完成')
    return render(request, 'update.html', {})

def allstart(request):
    return render(request, 'index.html')


def file_down(request):
    import os
    filename = os.path.join('filedown', "E:\\PyCharm\\kuaishou\\billboard.csv")  # 要下载的文件路径
    # do something
    file_billboard = 'billboard.csv'  # 显示在弹出对话框中的默认的下载文件名
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'  # 表明他是一个字节流
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_billboard)  # 默认文件名 不过好像加不加都没什么关系
    return response

def file1_down(request):
    import os
    filename = os.path.join('filedown', "E:\\PyCharm\\kuaishou\\movie.csv")  # 要下载的文件路径
    # do something
    file_movie = 'movie.csv'  # 显示在弹出对话框中的默认的下载文件名
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'  # 表明他是一个字节流
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_movie)  # 默认文件名 不过好像加不加都没什么关系
    return response

def file2_down(request):
    import os
    filename = os.path.join('filedown', "E:\\PyCharm\\kuaishou\\tube.csv")  # 要下载的文件路径
    # do something
    file_tube = 'tube.csv'  # 显示在弹出对话框中的默认的下载文件名
    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'  # 表明他是一个字节流
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_tube)  # 默认文件名 不过好像加不加都没什么关系
    return response

def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
