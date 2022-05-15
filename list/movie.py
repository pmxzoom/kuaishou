import codecs
import os

import PIL
import jieba
import numpy as np
import pymysql
import requests
import re
import csv
import pyecharts.options as opts
from PIL import Image
from matplotlib import pyplot as plt
from pyecharts.charts import Bar, PictorialBar, EffectScatter, Funnel, Pie
import pandas as pd

#### csv文件
from wordcloud import WordCloud


def wcsv():
    f = open('movie.csv',mode='w',encoding='utf-8',newline='')
    csv_writer = csv.DictWriter(f,fieldnames=[
       '片名',
       '演员',
       '题材',
       '观看人数',
    ])
    csv_writer.writeheader()
    url = 'https://www.kuaishou.com'
    headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
    }
    response = requests.get(url=url, headers=headers)
    movie = re.findall('{"movieId":(.*?),"movieName":"(.*?)","directors":null,"releaseDate":null,"actors":{"type":"json","json":(.*?)},"duration":(.*?),"photoId":"(.*?)","coverUrl":"(.*?)","movieTypes":"(.*?)","viewCount":(.*?),"viewCountStr":"(.*?)","llsid":null,"__typename":"VisionMovieFeed"}',response.text)
    for movieId,movieName,actors,duration,photoId,coverUrl,movieTypes,viewCount,viewCountStr in movie:
       print(movieId,movieName,actors,duration,photoId,coverUrl,movieTypes,viewCount,viewCountStr)
       dit =  {
           '片名':movieName,
           '演员':actors,
           '题材':movieTypes,
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
       if file.split('movie.')[-1] in ['csv']:  #判断文件是不是csv文件，file.split('.')[-1]获取‘.’后的字符串
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
from pyecharts.globals import ThemeType, SymbolType
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

        sql_name = """ SELECT 片名 FROM list_movie """
        cursor.execute(sql_name)
        names = cursor.fetchall()
        for name in names:
            namelist.append(name[0])
        print(namelist)
        sql_num = """ SELECT 观看人数 FROM list_movie """
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


def draweBar():
    bar = Bar(
        init_opts=opts.InitOpts(width="2000px",
                                height="900px",
                                theme=ThemeType.WHITE,
                                page_title="观看人数柱状图"
                                )
    )
    bar.add_xaxis(namelist)
    bar.add_yaxis('观看人数', numlist, category_gap=5)
    bar.set_global_opts(
        xaxis_opts=opts.AxisOpts(
                name="片名",
                axislabel_opts=opts.LabelOpts(rotate=-45),
                axisline_opts = opts.AxisLineOpts(symbol="arrow",linestyle_opts=opts.LineStyleOpts(width=1)),
                axistick_opts = opts.AxisTickOpts(is_inside=True,length=20),
                axispointer_opts = opts.AxisPointerOpts(is_show=True,type_="line")
    )
    )
    bar.render('E:/PyCharm/kuaishou/templates/movieBar.html')

def wtxt():
    url = 'https://www.kuaishou.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
    }
    response = requests.get(url=url, headers=headers)
    list = re.findall(
        '{"movieId":(.*?),"movieName":"(.*?)","directors":null,"releaseDate":null,"actors":{"type":"json","json":(.*?)},"duration":(.*?),"photoId":"(.*?)","coverUrl":"(.*?)","movieTypes":"(.*?)","viewCount":(.*?),"viewCountStr":"(.*?)","llsid":null,"__typename":"VisionMovieFeed"}',
        response.text)
    with open('E:\\PyCharm\\kuaishou\\movie.txt', 'w', encoding='utf-8') as bf:
        for movieId,movieName,actors,duration,photoId,coverUrl,movieTypes,viewCount,viewCountStr in list:
            bf.write(movieName + '\n')

def drawWordcloud():
    path_txt = 'E:\\PyCharm\\kuaishou\\movie.txt'
    path_img = "E:\\PyCharm\\kuaishou\\public\\img\\background.jpg"
    f = open(path_txt, 'r', encoding='utf-8').read()
    background_image = np.array(PIL.Image.open(path_img))
    # join() 方法用于将序列中的元素以指定的字符连接生成一个新的字符串
    cut_text = " ".join(jieba.cut(f))
    # mask参数=图片背景，必须要写上，另外有mask参数再设定宽高是无效的
    wordcloud = WordCloud(font_path="simhei.ttf", background_color="white", mask=background_image).generate(cut_text)
    # 生成颜色值
    #image_colors = ImageColorGenerator(background_image)
    # 下面代码表示显示图片
    plt.imshow(wordcloud, interpolation="bilinear")
    # 获得模块所在的路径的
    d = os.path.dirname(__file__)
    # os.path.join()：  将多个路径组合后返回
    wordcloud.to_file(os.path.join(d, "E:\\PyCharm\\kuaishou\\public\\movieWordcloud.jpg"))
    plt.axis("off")

def drawpie():
    """
    中文分词统计
    对两个词以上的次数进行统计
        lcut 进行分词，返回分词后list列表
    :return:
    """
    f = codecs.open("E:\\PyCharm\\kuaishou\\movie.txt", 'r', encoding='utf-8').read()
    counts = {}
    wordsList = jieba.lcut(f)
    for word in wordsList:
        word = word.replace("，", "").replace("！", "").replace("“", "") \
            .replace("”", "").replace("。", "").replace("？", "").replace("：", "") \
            .replace("...", "").replace("、", "").strip(' ').strip('\r\n')
        if len(word) == 1 or word == "":
            continue
        else:
            counts[word] = counts.get(word, 0) + 1  # 单词计数
    items = list(counts.items())  # 将字典转为list
    items.sort(key=lambda x: x[1], reverse=True)  # 根据单词出现次数降序排序
    # 打印前15个
    wc = {}
    for i in range(5):
        word, counter = items[i]
        wc = dict(items)
        print("单词：{},次数：{}".format(word, counter))
    pie = Pie(init_opts=opts.InitOpts(width="2000px", height="1000px", bg_color="#2c343c",page_title="词频统计饼图"))
    pie.add("词频饼图 ", [list(z) for z in zip([i for i in wc.keys()][:5],[i for i in wc.values()][:5])])
    pie.set_colors(["blue", "green", "yellow", "red", "black", "orange", "perpo"])
    pie.set_global_opts(title_opts=opts.TitleOpts(title="词频饼图",pos_left="center",pos_top="20",title_textstyle_opts=opts.TextStyleOpts(color="#fff"),),legend_opts=opts.LegendOpts(is_show=False),)
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.render("E:/PyCharm/kuaishou/templates/billboardpie.html")

def drawFunnel():
    f = codecs.open("E:\\PyCharm\\kuaishou\\movie.txt", 'r', encoding='utf-8').read()
    counts = {}
    wordsList = jieba.lcut(f)
    for word in wordsList:
        word = word.replace("，", "").replace("！", "").replace("“", "") \
            .replace("”", "").replace("。", "").replace("？", "").replace("：", "") \
            .replace("...", "").replace("、", "").strip(' ').strip('\r\n')
        if len(word) == 1 or word == "":
            continue
        else:
            counts[word] = counts.get(word, 0) + 1  # 单词计数
    items = list(counts.items())  # 将字典转为list
    items.sort(key=lambda x: x[1], reverse=True)  # 根据单词出现次数降序排序
    # 打印前15个
    wc = {}
    for i in range(5):
        word, counter = items[i]
        wc = dict(items)
        print("单词：{},次数：{}".format(word, counter))
    funnnel = Funnel(init_opts=opts.InitOpts(width="2000px", height="1000px",page_title="词频统计漏斗图"))
    funnnel.add(
        "词频统计",
        [list(z) for z in zip([i for i in wc.keys()][:5],[i for i in wc.values()][:5])],
        label_opts=opts.LabelOpts(position="inside"),
    )
    funnnel.set_global_opts(title_opts=opts.TitleOpts(title="词频统计漏斗图"))
    funnnel.render("E:/PyCharm/kuaishou/templates/moviefunnel.html")

def drawEffectScatter():
   effectScatter  = EffectScatter(
       init_opts=opts.InitOpts(width="2000px",
                               height="1000px",
                               theme=ThemeType.WHITE,
                               page_title="观看人数涟漪散点图"
                               )
   )
   effectScatter.add_xaxis(namelist)
   effectScatter.add_yaxis("观看人数", numlist)
   effectScatter.set_global_opts(
        title_opts=opts.TitleOpts(title="观看人数涟漪散点图"),
        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True),
                                 axislabel_opts=opts.LabelOpts(rotate=-45)),
        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
    )
   effectScatter.render("E:/PyCharm/kuaishou/templates/movieeffectscatter.html")

def drawPictorialBar():
    pictorialBar = PictorialBar(
        init_opts=opts.InitOpts(width="2000px",
                                height="1000px",
                                theme=ThemeType.WHITE,
                                page_title="观看人数象形柱图"
                                )
    )
    pictorialBar.add_xaxis(namelist)
    pictorialBar.add_yaxis(
        "观看人数",
        numlist,
        label_opts=opts.LabelOpts(is_show=False),
        symbol_size=5,
        symbol_repeat="fixed",
        symbol_offset=[0, 0],
        is_symbol_clip=True,
        symbol=SymbolType.ROUND_RECT,
    )
    pictorialBar.reversal_axis()
    pictorialBar.set_global_opts(
        title_opts=opts.TitleOpts(title="观看人数象形柱图"),
        xaxis_opts=opts.AxisOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(opacity=0)
            ),
        ),
    )
    pictorialBar.render("E:/PyCharm/kuaishou/templates/moviepictorialbar.html")

if __name__ == '__main__':
    wcsv()
    wmysql()
    getdata()
    draweBar()
    wtxt()
    drawWordcloud()
    drawFunnel()
    drawpie()
    drawPictorialBar()
    drawEffectScatter()
