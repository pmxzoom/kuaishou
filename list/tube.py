import os

import pymysql
import requests
import re
import csv
import pyecharts.options as opts
from pyecharts.charts import Bar
import pandas as pd

#### csv文件
def wcsv():
    f = open('tube.csv',mode='w',encoding='utf-8',newline='')
    csv_writer = csv.DictWriter(f,fieldnames=[
       '剧名',
       '简介',
       '最近更新',
       '观看人数',
    ])
    csv_writer.writeheader()
    url = 'https://www.kuaishou.com'
    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
    }
    response = requests.get(url=url, headers=headers)
    tube = re.findall('{"name":"(.*?)","caption":"(.*?)","tubeId":"(.*?)","description":"(.*?)","totalEpisodeCount":(.*?),"totalEpisodeCountIgnoreStatus":(.*?),"lastEpisodeName":"(.*?)","viewCount":(.*?),"coverUrl":"(.*?)","__typename":"VisionTubeFeed"}',response.text)
    for name,caption,tubeId,description,totalEpisodeCount,totalEpisodeCountIgnoreStatus,lastEpisodeName,viewCount,coverUrl in tube:
       print(name,caption,tubeId,description,totalEpisodeCount,totalEpisodeCountIgnoreStatus,lastEpisodeName,viewCount,coverUrl)
       dit =  {
           '剧名':caption,
           '简介':description,
           '最近更新':lastEpisodeName,
           '观看人数':viewCount
       }
       csv_writer.writerow(dit)

def wmysql():
    #pd.set_option()#就是pycharm输出控制显示的设置
    pd.set_option('expand_frame_repr', False)#True就是可以换行显示。设置成False的时候不允许换行
    pd.set_option('display.max_columns', None)# 显示所有列
    pd.set_option('colheader_justify', 'centre')# 显示居中

    try:
       conn = pymysql.connect(host='localhost', user='root', password='root', db='kuaishou', charset='utf8')
       cur = conn.cursor()
       print('数据库连接成功！')
       print(' ')
    except:
       print('数据库连接失败！')

    os.chdir('E:/PyCharm/kuaishou/')  #将路径设置成你csv文件放的地方
    path = os.getcwd()
    files = os.listdir(path)

    i = 0  #计数器，后面可以用来统计一共导入了多少个文件
    for file in files:
       if file.split('tube.')[-1] in ['csv']:  #判断文件是不是csv文件，file.split('.')[-1]获取‘.’后的字符串
           i += 1
           filename = file.split('.')[0]  #获取剔除后缀的名称
           filename = 'list_' + filename
           f = pd.read_csv(file, encoding='utf-8')  #用pandas读取文件，得到pandas框架格式的数据
           columns = f.columns.tolist()  #获取表格数据内的列标题文字数据

           types = f.dtypes  #获取文件内数据格式
           field = []  #设置列表用来接收文件转换后的数据，为写入mysql做准备
           table = []
           char = []
           for item in range(len(columns)):  #开始循环获取文件格式类型并将其转换成mysql文件格式类型
               if 'object' == str(types[item]):
                   char = '`' + columns[item] + '`' + ' VARCHAR(255)'  #必须加上`这个点，否则在写入mysql是会报错
               elif 'int64' == str(types[item]):
                   char = '`' + columns[item] + '`' + ' INT'
               elif 'float64' == str(types[item]):
                   char = '`' + columns[item] + '`' + ' FLOAT'
               elif 'datetime64[ns]' == str(types[item]):
                   char = '`' + columns[item] + '`' + ' DATETIME'
               else:
                   char = '`' + columns[item] + '`' + ' VARCHAR(255)'
               table.append(char)
               field.append('`' + columns[item] + '`')

           tables = ','.join(table)  #将table中的元素用，连接起来为后面写入mysql做准备
           fields = ','.join(field)

           cur.execute('drop table if exists {};'.format(filename))
           conn.commit()

           #创建表格并设置表格的列文字跟累数据格式类型
           table_sql = 'CREATE TABLE IF NOT EXISTS ' + filename + '(' + 'id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,' + tables + ');'
           print('表:' + filename + ',开始创建数据表...')
           cur.execute(table_sql)
           conn.commit()
           print('表:' + filename + ',创建成功!')

           print('表:' + filename + ',正在写入数据当中...')
           f_sql = f.astype(object).where(pd.notnull(f), None)  #将原来从csv文件获取得到的空值数据设置成None，不设置将会报错
           values = f_sql.values.tolist()  #获取数值
           s = ','.join(['%s' for _ in range(len(f.columns))])  #获得文件数据有多少列，每个列用一个 %s 替代
           insert_sql = 'insert into {}({}) values({})'.format(filename,fields,s)
           cur.executemany(insert_sql, values)
           conn.commit()
           print('表:' + filename + ',数据写入完成！')
           print(' ')
    cur.close()
    conn.close()
    print('文件导入数据库完成！一共导入了 {} 个CSV文件。'.format(i))



### 绘图
from pyecharts.globals import ThemeType
from pymysql import *

namelist = []
numlist = []


def getdata():
    conn = connect(host='127.0.0.1',
                   port=3306,
                   user='root',
                   password='root',
                   db='kuaishou',
                   charset='utf8')
    cursor = conn.cursor()
    try:

        sql_name = """ SELECT 剧名 FROM list_tube """
        cursor.execute(sql_name)
        names = cursor.fetchall()
        for name in names:
            namelist.append(name[0])
        print(namelist)
        sql_num = """ SELECT 观看人数 FROM list_tube """
        cursor.execute(sql_num)
        nums = cursor.fetchall()
        for num in nums:
            numlist.append(num[0])
        print(numlist)
    except:
        print("未查询到数据！")
        conn.rollback()
    finally:
        conn.close()


def drawecharts():
    bar = Bar(
        init_opts=opts.InitOpts(width="2000px",
                                height="1000px",
                                theme=ThemeType.LIGHT,
                                bg_color="skyblue"
                                )
    )
    bar.add_xaxis(namelist)
    bar.add_yaxis('w', numlist, category_gap=5)
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(
                name="片名",
                axislabel_opts=opts.LabelOpts(rotate=-45),
                axisline_opts = opts.AxisLineOpts(symbol="arrow",linestyle_opts=opts.LineStyleOpts(width=2)),
                axistick_opts = opts.AxisTickOpts(is_inside=True,length=20),
                axispointer_opts = opts.AxisPointerOpts(is_show=True,type_="line")
    )
    )
    bar.render('E:/PyCharm/kuaishou/templates/t.html')


if __name__ == '__main__':
    wcsv()
    wmysql()
    getdata()
    drawecharts()