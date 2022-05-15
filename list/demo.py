import codecs
import re

import jieba
import matplotlib
import pyecharts.options as opts
import requests
from matplotlib import pyplot as plt
from pyecharts.charts import EffectScatter, PictorialBar, Pie, Funnel

#### csv文件
# f = open('list.csv',mode='w',encoding='utf-8',newline='')
# csv_writer = csv.DictWriter(f,fieldnames=[
#   '排名',
#   '标题',
#   '热度',
#   '种类',
# ])
# csv_writer.writeheader()
# url = 'https://www.kuaishou.com'
# headers = {
#   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
# }
# response = requests.get(url=url, headers=headers)
# list = re.findall(
#   '{"rank":(.*?),"id":"(.*?)","name":"(.*?)","viewCount":null,"hotValue":"(.*?)w","iconUrl":(.*?),"poster":\"(.*?)\","tagType":(.*?),"__typename":"VisionHotRankItem"}',
#   response.text)
# for rank,id,name,hotValue,iconUrl,poster,tagType in list:
#  print(rank,id,name,hotValue,iconUrl,poster,tagType)
#  dit =  {
#      '排名':rank,
#      '标题':name,
#      '热度':hotValue,
#      '种类':tagType
#  }
#  csv_writer.writerow(dit)

### 爬取json文件
# url = 'https://www.kuaishou.com'
# headers = {
#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
# }
# response = requests.get(url=url, headers=headers)
# list = re.findall(
#    '{"rank":(.*?),"id":"(.*?)","name":"(.*?)","viewCount":(.*?),"hotValue":"(.*?)","iconUrl":(.*?),"poster":\"(.*?)\","tagType":(.*?),"__typename":"VisionHotRankItem"}',
#    response.text)
# for i in list:
#    print(i)
# fp = open('./list.json', 'w', encoding='utf-8')
# json.dump(list, fp=fp, ensure_ascii=False)


### mysql文件
# pd.set_option()就是pycharm输出控制显示的设置
# pd.set_option('expand_frame_repr', False)#True就是可以换行显示。设置成False的时候不允许换行
# pd.set_option('display.max_columns', None)# 显示所有列
##pd.set_option('display.max_rows', None)# 显示所有行
# pd.set_option('colheader_justify', 'centre')# 显示居中
#
# try:
#    conn = pymysql.connect(host='localhost', user='root', password='root', db='kuaishou', charset='utf8')
#    cur = conn.cursor()
#    print('数据库连接成功！')
#    print(' ')
# except:
#    print('数据库连接失败！')
#
# os.chdir('E:/PyCharm 2021.3.3/kuaishou/list/')  #将路径设置成你csv文件放的地方
# path = os.getcwd()
# files = os.listdir(path)
#
# i = 0  #计数器，后面可以用来统计一共导入了多少个文件
# for file in files:
#    if file.split('.')[-1] in ['csv']:  #判断文件是不是csv文件，file.split('.')[-1]获取‘.’后的字符串
#        i += 1
#        filename = file.split('.')[0]  #获取剔除后缀的名称
#        filename = 'data_' + filename
#        f = pd.read_csv(file, encoding='utf-8')  #用pandas读取文件，得到pandas框架格式的数据
#        columns = f.columns.tolist()  #获取表格数据内的列标题文字数据
#
#        types = f.dtypes  #获取文件内数据格式
#        field = []  #设置列表用来接收文件转换后的数据，为写入mysql做准备
#        table = []
#        char = []
#        for item in range(len(columns)):  #开始循环获取文件格式类型并将其转换成mysql文件格式类型
#            if 'object' == str(types[item]):
#                char = '`' + columns[item] + '`' + ' VARCHAR(255)'  #必须加上`这个点，否则在写入mysql是会报错
#            elif 'int64' == str(types[item]):
#                char = '`' + columns[item] + '`' + ' INT'
#            elif 'float64' == str(types[item]):
#                char = '`' + columns[item] + '`' + ' FLOAT'
#            elif 'datetime64[ns]' == str(types[item]):
#                char = '`' + columns[item] + '`' + ' DATETIME'
#            else:
#                char = '`' + columns[item] + '`' + ' VARCHAR(255)'
#            table.append(char)
#            field.append('`' + columns[item] + '`')
#
#        tables = ','.join(table)  #将table中的元素用，连接起来为后面写入mysql做准备
#        fields = ','.join(field)
#
#        cur.execute('drop table if exists {};'.format(filename))
#        conn.commit()
#
#        #创建表格并设置表格的列文字跟累数据格式类型
#        table_sql = 'CREATE TABLE IF NOT EXISTS ' + filename + '(' + 'id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,' + tables + ');'
#        print('表:' + filename + ',开始创建数据表...')
#        cur.execute(table_sql)
#        conn.commit()
#        print('表:' + filename + ',创建成功!')
#
#        print('表:' + filename + ',正在写入数据当中...')
#        f_sql = f.astype(object).where(pd.notnull(f), None)  #将原来从csv文件获取得到的空值数据设置成None，不设置将会报错
#        values = f_sql.values.tolist()  #获取数值
#        s = ','.join(['%s' for _ in range(len(f.columns))])  #获得文件数据有多少列，每个列用一个 %s 替代
#        insert_sql = 'insert into {}({}) values({})'.format(filename,fields,s)
#        cur.executemany(insert_sql, values)
#        conn.commit()
#        print('表:' + filename + ',数据写入完成！')
#        print(' ')
# cur.close()
# conn.close()
# print('文件导入数据库完成！一共导入了 {} 个CSV文件。'.format(i))


### 绘图
from pyecharts.globals import ThemeType, SymbolType
from pymysql import *
from twisted import words

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

       sql_name = """ SELECT 标题 FROM data_billboard """
       cursor.execute(sql_name)
       names = cursor.fetchall()
       for name in names:
           namelist.append(name[0])
       print(namelist)
       sql_num = """ SELECT 热度 FROM data_billboard """
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
#
#
# def drawecharts():
#    bar = Bar(
#        init_opts=opts.InitOpts(width="2000px",
#                                height="1000px",
#                                theme=ThemeType.LIGHT,
#                                bg_color="skyblue"
#                                )
#    )
#    bar.add_xaxis(namelist)
#    bar.add_yaxis('w', numlist, category_gap=5)
#    bar.set_global_opts(
#        xaxis_opts=opts.AxisOpts(
#                name="商家名称",
#                axislabel_opts=opts.LabelOpts(rotate=135),
#                axisline_opts = opts.AxisLineOpts(symbol="arrow",linestyle_opts=opts.LineStyleOpts(width=2)),
#                axistick_opts = opts.AxisTickOpts(is_inside=True,length=20),
#                axispointer_opts = opts.AxisPointerOpts(is_show=True,type_="line")
#    )
#    )
#    bar.render()
#
#def drawEffectScatter():
#   effectScatter  = EffectScatter(
#       init_opts=opts.InitOpts(width="2000px",
#                               height="1000px",
#                               theme=ThemeType.WHITE,
#                               page_title="观看人数涟漪散点图"
#                               )
#   )
#   effectScatter.add_xaxis(namelist)
#   effectScatter.add_yaxis("观看人数w", numlist)
#   effectScatter.set_global_opts(
#        title_opts=opts.TitleOpts(title="观看人数涟漪散点图"),
#        xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True),
#                                 axislabel_opts=opts.LabelOpts(rotate=-45)),
#        yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
#    )
#   effectScatter.render("effectscatter.html")

#def drawPictorialBar():
#    pictorialBar=PictorialBar(
#        init_opts=opts.InitOpts(width="2000px",
#                                height="1000px",
#                                theme=ThemeType.WHITE,
#                                page_title="观看人数象形柱图"
#                                )
#    )
#    pictorialBar.add_xaxis(namelist)
#    pictorialBar.add_yaxis(
#        "观看人数",
#        numlist,
#        label_opts=opts.LabelOpts(is_show=False),
#        symbol_size=5,
#        symbol_repeat="fixed",
#        symbol_offset=[0, 0],
#        is_symbol_clip=True,
#        symbol=SymbolType.ROUND_RECT,
#    )
#    pictorialBar.reversal_axis()
#    pictorialBar.set_global_opts(
#        title_opts=opts.TitleOpts(title="观看人数象形柱图"),
#        xaxis_opts=opts.AxisOpts(is_show=False),
#        yaxis_opts=opts.AxisOpts(
#            axistick_opts=opts.AxisTickOpts(is_show=False),
#            axisline_opts=opts.AxisLineOpts(
#                linestyle_opts=opts.LineStyleOpts(opacity=0)
#            ),
#        ),
#    )
#    pictorialBar.render("pictorialbar_base.html")
#
#getdata()
#drawPictorialBar()

def wtxt():
    url = 'https://www.kuaishou.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0'
    }
    response = requests.get(url=url, headers=headers)
    list = re.findall(
        '{"rank":(.*?),"id":"(.*?)","name":"(.*?)","viewCount":null,"hotValue":"(.*?)w","iconUrl":(.*?),"poster":\"(.*?)\","tagType":(.*?),"__typename":"VisionHotRankItem"}',
        response.text)
    with open('E:\\PyCharm\\kuaishou\\billboardname.txt', 'w', encoding='utf-8') as bf:
        for rank, id, name, hotValue, iconUrl, poster, tagType in list:
            bf.write(name + '\n')

def drawpie():
    """
    中文分词统计
    对两个词以上的次数进行统计
        lcut 进行分词，返回分词后list列表
    :return:
    """
    f = codecs.open("E:\\PyCharm\\kuaishou\\billboardname.txt", 'r', encoding='utf-8').read()
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
    pie = Pie(init_opts=opts.InitOpts(width="2000px", height="1000px", bg_color="#2c343c",page_title="快手热榜词频统计饼图"))
    pie.add("词频饼图 ", [list(z) for z in zip([i for i in wc.keys()][:5],[i for i in wc.values()][:5])])
    pie.set_colors(["blue", "green", "yellow", "red", "black", "orange", "perpo"])
    pie.set_global_opts(title_opts=opts.TitleOpts(title="词频饼图",pos_left="center",pos_top="20",title_textstyle_opts=opts.TextStyleOpts(color="#fff"),),legend_opts=opts.LegendOpts(is_show=False),)
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    pie.render("pie_set_color.html")

def drawFunnel():
    f = codecs.open("E:\\PyCharm\\kuaishou\\billboardname.txt", 'r', encoding='utf-8').read()
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
    funnnel = Funnel(init_opts=opts.InitOpts(width="2000px", height="1000px",page_title="快手热榜词频统计漏斗图"))
    funnnel.add(
        "词频统计",
        [list(z) for z in zip([i for i in wc.keys()][:5],[i for i in wc.values()][:5])],
        label_opts=opts.LabelOpts(position="inside"),
    )
    funnnel.set_global_opts(title_opts=opts.TitleOpts(title="快手热榜词频统计漏斗图"))
    funnnel.render("funnel_label_inside.html")

wtxt()
drawpie()
drawFunnel()