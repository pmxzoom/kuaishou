from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from list import billboard, tube, movie


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


def showb(request):
    return render(request, 'b.html')


def showm(request):
    return render(request, 'm.html')


def showt(request):
    return render(request, 't.html')


def allupdate(request):
    billboard.wcsv()
    billboard.wmysql()
    billboard.getdata()
    billboard.drawecharts()
    tube.wcsv()
    tube.wmysql()
    tube.getdata()
    tube.drawecharts()
    movie.wcsv()
    movie.wmysql()
    movie.getdata()
    movie.drawecharts()
    return HttpResponse('完成')


def allquit(requesst):
    return HttpResponse('退出')

def allstart(requesst):
    return HttpResponse('欢迎')
