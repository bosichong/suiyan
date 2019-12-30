# -*- coding:utf-8 -*-

import argparse
import os
import re
import json
import datetime
import random

from fnmatch import fnmatch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前目录地址
ARTICLES_DIR = os.path.join(BASE_DIR, "articles")  # 日志目录
CONFIGJSON = 'config.json'
SUIYANVERSION = "1.0.0"  # 程序版本
# 匹配文章数据的正则
DIVRE = '<div class="blog-article">?([\s\S]*?)</div>'


def create_blog_data_Json(adir, bdir):
    '''
    递归获得当前目录及其子目录中所有的.md文件列表。
    并创建blog的data索引JSON
    :param adir: 文章日志所在目录
    :param bdir: 站点根目录
    :return: json字符串
    '''
    data_json = []
    data_json_str = ""
    # 当前目录下所有的文件、子目录、子目录下的文件。
    for root, dirs, files in os.walk(adir):
        # print(root)
        # print(dirs)
        # print(files)  
        for name in files:
            # 值读取.md
            if name.endswith('.md'):
                url = os.path.join(root, name).replace(adir+'/', '').replace('.md','')  # 最后需要组装的相对目录
                furl = os.path.join(root, name)  # 当前文件的绝对目录
                if getmd(furl):
                    datahtml = getmd(furl)  # 取回当前.md文件的HTML头部信息
                    f_data = getjson(datahtml)  # 获取.md的文章信息HTML转化成数组
                    f_data["url"] = url
                    data_json.append(f_data)  # 添加到需要返回的数据数组中

    data_json.sort(key = lambda x:x["time"],reverse = True)#对数组进行降序排序
    data_json_str = json.dumps(data_json, ensure_ascii=False)  # 转化为json字符串

    return data_json_str


def write_data_json(json_str):
    '''
    创建blog索引.json
    :param json_str: json 字符串
    :return:
    '''
    with open(os.path.join(os.path.dirname(__file__), 'blog_data.json'), mode='w', encoding='utf-8') as f:
        f.write(json_str)


def getmd(md):
    '''
    获得md文件内容，并返回md文件头部的文章信息HTML。
    :param md 文件地址
    :return: 存在则返回字符串，没有头部文件信息的返回flase
    '''
    # print(md)
    s = ""
    with open(os.path.join(md), encoding='utf-8') as f:
        s = f.read()
    if re.match(DIVRE, s) != None:
        return re.match(DIVRE, s).group()
    else:
        return False


def getjson(s):
    '''
    获取.md的文章信息HTML转化成数组
    :param s: 待解析的HTML字符串
    :return: 配置信息数组
    '''
    arr = re.findall('<.* class="(.*)">(.*?)</.*>', s)
    data = {}
    for a in arr:
        data[a[0]] = a[1]
    return data


def create_blog(title, author, tag, dir, pagename):
    '''
    创建一篇空白的新blog
    :param title: blog标题
    :param author: blog作者默认为空的话前段渲染为站长昵称，转载可以添加佚名或是原作者。
    :param tag: 标签 默认为为分类
    :param dir 存放目录
    :param pagename: 当前页面的name 例如"hello188.md",如果为空默认为年月日时间字符串
    :return: 
    '''
    # 文章创建时间
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    if pagename == '':
        pagename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if tag == '':
        tag = "未分类"
    if author == '':
        # 从配置文件里加载站长为作者
        with open(os.path.join(os.path.dirname(__file__), CONFIGJSON), mode='r', encoding='utf-8') as f:
            data = json.load(f)
            author = data['blog_author']
    # print(author,tag,pagename)
    # 组装最后生成的文章保存目录
    # blogpath = os.path.join(ARTICLES_DIR, dir)
    # 最后需要生成的文件
    blogfile = os.path.join(ARTICLES_DIR, os.path.join(dir, pagename + '.md'))

    # 将文件路径分割出来
    file_dir = os.path.split(blogfile)[0]

    # 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)


    # print(blogpath)
    bloghtml = '<div class="blog-article">\n\
<h1 class="title">' + title + '</h1>\n\
<span class="author">' + author + '</span>\n\
<span class="time">' + create_time + '</span>\n\
<span class="tag">' + tag + '</span>\n\
</div>\n</br>\n\n\
## 可以开始写blog啦(*￣︶￣)'


    if os.path.isfile(blogfile):
        print('文件存在相同名称，创建失败。')
    else:
        with open(blogfile, mode='w', encoding='utf-8') as f:
            f.write(bloghtml)
        print('blog文章.md创建成功！')

    # print(getjson(str))


def create_test(con):
    '''
    生成测试blog默认1000篇，放在目录suiyantest下。
    获取.md的文章信息HTML转化成数组
    :param con: 需要生成的文章数。
    :return: void
    '''
    dir = "suiyantest"
    for i in range(con):
        #随机生成一些文章数据填充，用来测试
        title = random.choice(("打法撒发射点发斯蒂芬","斯蒂芬阿斯蒂芬斯蒂芬","斯蒂芬阿斯蒂芬","斯蒂芬阿斯蒂芬","斯蒂芬斯蒂芬阿斯蒂芬3",))
        tag = random.choice(("Java","JavaScript","Python","C++","程序员",))
        pagename = str(random.randint(99999,99999999))
        create_blog(title=title,tag=tag,dir=dir,author='',pagename=pagename)




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="查询程序版本", action="store_true")
    parser.add_argument("-i", "--index", help="更新索引blog数据json", action="store_true")
    parser.add_argument("-n", "--newblog", help="创建新日志，请输入标题（必填）。", )
    parser.add_argument("-t", "--tag", help="请输入blog的标签TAG", default='')
    parser.add_argument("-a", "--author", help="请输入文章作者，默认调用站长昵称", default='')
    parser.add_argument("-p", "--pagename", help="请输入文章地址页面名称", default='')
    parser.add_argument("-d", "--dir", help="请输入文章地址所属目录", default='')
    parser.add_argument("-tt", "--suiyantest", help="生成测试blog,填写需要生成的数目，测试文章放在目录suiyantest下。",type=int,)

    args = parser.parse_args()
    if args.version:
        print(SUIYANVERSION)
    elif args.newblog:
        create_blog(title=args.newblog,author=args.author,tag=args.tag,dir=args.dir,pagename=args.pagename,)
        print("新文章.md创建完毕！")
        jsonstr = create_blog_data_Json(ARTICLES_DIR, BASE_DIR)
        write_data_json(jsonstr)
        print("blog_data.json索引文件更新完毕！")
    elif args.suiyantest:
        create_test(args.suiyantest)
        print("测试文件创建完毕！")
    elif args.index:
        jsonstr = create_blog_data_Json(ARTICLES_DIR, BASE_DIR)
        write_data_json(jsonstr)
        print("blog_data.json索引文件更新完毕！")
    else:
        print(parser.print_help())  # 默认打印帮助

        


if __name__ == "__main__":
    main()
