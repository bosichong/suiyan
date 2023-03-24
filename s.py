# -*- coding: UTF-8 -*-
"""
@Author   : J.sky
@Mail     : bosichong@qq.com
@Site     : https://github.com/bosichong
@QQ交流群  : python交流学习群号:217840699
@file      :s.py
@time     :2023/03/21

"""
# 导入相关模块
from jinja2 import FileSystemLoader, Environment
import argparse
import os
import shutil
import re
import json
import datetime
import random
import time
import asyncio
import aiofiles
# 导入markdown模块
from markdown import markdown
from utils import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前目录地址
BLOGPAGES = os.path.join(BASE_DIR, "blog")  # 所有静态资源存放目录
ARTICLES_DIR = os.path.join(BASE_DIR, "articles")  # 博文目录

CONFIGJSON = os.path.join('config.json')
BLOGDATAJSON = os.path.join('blog_data.json')
# 匹配文章数据的正则

SUIYANVERSION = "2.0.2"  # 程序版本


def loadcode(path):
    """载入文件中的代码"""
    try:
        with open(os.path.join(path), encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"文件{path}不存在")
        code = ''

    return code


def load_configjson():
    '''载入blog配置文件config.json'''
    config_code = loadcode(CONFIGJSON)
    config = json.loads(config_code)
    return config


def load_blogdatajson():
    '''载入blog数据blog_data.json'''
    blogdata = loadcode(BLOGDATAJSON)
    blog = json.loads(blogdata)
    return blog


def create_blog_data_Json(adir):
    '''
    递归获得当前目录及其子目录中所有的.md文件列表。
    并创建blog的data索引JSON
    :param adir: 文章日志所在目录
    :param bdir: 站点根目录
    :return: json字符串
    '''
    data_json = []
    # 当前目录下所有的文件、子目录、子目录下的文件。
    for root, dirs, files in os.walk(adir):
        for name in files:
            # 值读取.md
            if name.endswith('.md'):
                url = os.path.join(root, name).replace(
                    adir + os.sep, '').replace('.md', '')  # 最后需要组装的相对目录
                furl = os.path.join(root, name)  # 当前文件的绝对目录
                f_data = extract_md_header(furl)  # 获取.md的文章信息转成字典
                f_data["url"] = url
                # print(f_data)
                data_json.append(f_data)  # 添加到需要返回的数据数组中

    data_json.sort(key=lambda x: x["time"], reverse=True)  # 对数组进行降序排序
    data_json_str = json.dumps(data_json, ensure_ascii=False)  # 转化为json字符串
    # print(data_json_str)
    return data_json_str


def create_data_json():
    '''
    创建blog索引.json
    @param json_str: json 字符串
    @return:
    '''
    json_str = create_blog_data_Json(ARTICLES_DIR)
    with open(os.path.join(BASE_DIR, 'blog_data.json'), mode='w', encoding='utf-8') as f:
        f.write(json_str)
    print("blog数据索引更新完毕！")


def create_sitemap():
    '''创建网站地图'''
    config = load_configjson()  # 得到blog的配置Python字典
    siteurl = config["site_url"]
    tmpstr = ""
    blogdata = load_blogdatajson()  # 获得blog的博文数据
    for ar in blogdata:
        if os.sep in ar["url"]:
            ar["url"] = xurl(ar["url"])

        tmpstr += '<url>\
        <loc>' + siteurl + ar["url"] + '.html</loc>\
        <lastmod>' + ar["time"] + '</lastmod>\
        <changefreq>daily</changefreq>\
        <priority>0.8</priority></url>'

    xml_str = '<?xml version="1.0" encoding="utf-8"?>\
    <urlset>' + tmpstr + '</urlset>'
    # print(xml_str)
    with open(os.path.join(BLOGPAGES, 'sitemap.xml'), mode='w', encoding='utf-8') as f:
        f.write(xml_str)
    print("sitemap.xml更新完毕！")


def jinja_test(template, context, file_path):
    """
    把字符串保存到./templates/XXX.html 用来预览页面
    """
    with open(file_path, 'w') as f:
        f.write(template.render(**context))


# 上下文

def create_context():
    """
    创建模板的上下文
    """

    context = {
        "config": load_configjson(),
        "title":  "Home"
    }
    return context


async def create_list_html(i, ps):
    """
    批量生成首页和列表页的详细方法
    @i 当前页
    @ps 总页数
    """
    articles = []
    blog_data = load_blogdatajson()
    config = load_configjson()
    # 设置jinja模板
    env = Environment(loader=FileSystemLoader('./templates'))
    context = create_context()
    tmp = env.get_template("index.html")  # 模板
    index_html_path = os.path.join(BLOGPAGES, 'index.html')  # 首页HTML
    cs = config["blog_page_num"]  # 每页博文数量
    if i < ps:
        maxp = cs * i + cs  # 末尾文章数。
        # 若是最后一页，且文章有剩余，则添加余下的博文到最后一页
        if i == ps - 1 and len(load_blogdatajson()) % cs > 0:
            maxp = cs * i + (len(blog_data) % cs)
        for p in range(cs * i, maxp):
            article = blog_data[p]
            article["blog"] = markdown(read_file_without_header(os.path.join(ARTICLES_DIR,
                                                                             blog_data[p]["url"] + '.md')))
            articles.append(article)
            context["articles"] = articles  # 把当前页的blog数据加入上下文

        # 组装分页加入上下文
        context["prevurl"] = 'list_' + str(i - 1) + '.html'
        context["nexturl"] = 'list_' + str(i + 1) + '.html'
        context["page_num"] = str(i) + ' / ' + str(ps)
        if i == 0:
            context["prevurl"] = '#'
        if i == ps - 1:
            context["nexturl"] = '#'

        if i == 0:
            async with aiofiles.open(index_html_path, mode='w', encoding='utf-8') as f:
                await f.write(tmp.render(**context))
                print('生成index.html成功！')
            # 同时生成一个列表页的第一页
            async with aiofiles.open(os.path.join(BLOGPAGES, 'list_' + str(i) + '.html'), mode='w', encoding='utf-8') as f:
                await f.write(tmp.render(**context))
                print('生成list_' + str(i) + '.html 成功！')
        else:
            context["title"] = "List Pages" + " 第"+str(i)+"页"
            async with aiofiles.open(os.path.join(BLOGPAGES, 'list_' + str(i) + '.html'), mode='w', encoding='utf-8') as f:
                await f.write(tmp.render(**context))
                print('生成list_' + str(i) + '.html 成功！')


def create_index_html():
    """
    批量生成首页和列表页
    """
    blog_data = load_blogdatajson()
    # 根据博文数量推导列表页数
    config = load_configjson()
    ps = calculate_page_num(config["blog_page_num"], len(blog_data))
    # 获取上下文

    # 异步
    ct = [create_list_html(i, ps) for i in range(ps)]  # 列表生成式
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(ct))


def create_archives_html():
    """生成archives.html"""
    blog_data = load_blogdatajson()
    config = load_configjson()
    # 设置jinja模板
    env = Environment(loader=FileSystemLoader('./templates'))
    context = create_context()
    tmp = env.get_template("archives.html")  # 模板
    archives_html_path = os.path.join(BLOGPAGES, 'archives.html')  # 首页HTML
    # 组装archives页面的上下文数据。
    data = formatdata(blog_data)
    for l in data:
        l["num"] = len(l["data"])
    context["pages_num"] = len(blog_data)
    context["update"] = blog_data[0]["time"]
    context["archives"] = data
    with open(archives_html_path, mode='w', encoding='utf-8') as f:
        f.write(tmp.render(**context))
        print('生成archives.html成功！')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="查询程序版本", action="store_true")
    parser.add_argument(
        "-i", "--index", help="一键更新索引blog数据json及全站的静态资源", action="store_true")
    parser.add_argument("-s", "--sitemap",
                        help="更新sitemap.mxl", action="store_true")
    parser.add_argument("-n", "--newblog", help="创建新日志，请输入标题（必填）。", )
    parser.add_argument("-t", "--tag", help="请输入blog的标签TAG", default='')
    parser.add_argument("-a", "--author", help="请输入文章作者，默认调用站长昵称", default='')
    parser.add_argument("-p", "--pagename", help="请输入文章地址页面名称", default='')
    parser.add_argument("-d", "--dir", help="请输入文章地址所属目录", default='')

    parser.add_argument("-tt", "--suiyantest",
                        help="生成测试blog,填写需要生成的数目，测试文章放在目录suiyantest下。", type=int, )

    args = parser.parse_args()
    if args.version:
        print(SUIYANVERSION)
    elif args.newblog:
        print("新文章.md创建完毕！")
    elif args.suiyantest:
        print("测试文件创建完毕！")
    elif args.index:
        create_data_json()
        create_sitemap()
        delete_html_files()

        print("首页及blog列表页更新完毕！")

        print("文章归档页更新完毕！")

        print("标签页更新完毕！")

        print("所有blog文章页更新完毕！")
    elif args.sitemap:

        print("sitemap.xml更新完毕！")
    else:
        print(parser.print_help())  # 默认打印帮助


if __name__ == "__main__":
    create_blog_dir(BLOGPAGES)  # 所有blog目录，存放blog中的所有静态资源。
    # main()
    create_data_json()
    create_sitemap()
    create_index_html()
    create_archives_html()