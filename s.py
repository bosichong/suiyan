# -*- coding: UTF-8 -*-
"""
@Author   : J.sky
@Mail     : bosichong@qq.com
@Site     : https://github.com/bosichong
@QQ交流群  : python交流学习群号:217840699
@file      :s.py
@time     :2023/03/21

"""
import datetime
import random

# 导入相关模块
from jinja2 import FileSystemLoader, Environment
import argparse
import asyncio
import aiofiles
# 导入markdown模块
from markdown import markdown
from utils import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前目录地址
BLOGPAGES = os.path.join(BASE_DIR, "blog")  # 所有静态资源存放目录
ARTICLES_DIR = os.path.join(BASE_DIR, "articles")  # 博文目录

CONFIGJSON = os.path.join(BLOGPAGES, 'config.json')
BLOGDATAJSON = os.path.join(BLOGPAGES, 'blog_data.json')
# 匹配文章数据的正则

SUIYANVERSION = "2.0.2"  # 程序版本


def create_sitemap():
    '''创建网站地图'''
    config = load_configjson(CONFIGJSON)  # 得到blog的配置Python字典
    siteurl = config["site_url"]
    tmpstr = ""
    blogdata = load_blogdatajson(BLOGDATAJSON)  # 获得blog的博文数据
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


def create_context():
    """
    创建模板的上下文
    """

    context = {
        "config": load_configjson(CONFIGJSON),
        "title":  "Home"
    }
    return context


def create_index_html():
    """
    批量生成首页和列表页
    """
    blog_data = load_blogdatajson(BLOGDATAJSON)
    # 根据博文数量推导列表页数
    config = load_configjson(CONFIGJSON)
    ps = calculate_page_num(config["blog_page_num"], len(blog_data))
    # 获取上下文

    # 异步
    ct = [create_list_html(i, ps) for i in range(ps)]  # 列表生成式
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(ct))


async def create_list_html(i, ps):
    """
    批量生成首页和列表页的详细方法
    @i 当前页
    @ps 总页数
    """
    articles = []
    blog_data = load_blogdatajson(BLOGDATAJSON)
    config = load_configjson(CONFIGJSON)
    # 设置jinja模板
    env = Environment(loader=FileSystemLoader('./templates'))
    context = create_context()
    tmp = env.get_template("index.html")  # 模板
    index_html_path = os.path.join(BLOGPAGES, 'index.html')  # 首页HTML
    cs = config["blog_page_num"]  # 每页博文数量
    if i < ps:
        maxp = cs * i + cs  # 末尾文章数。
        # 若是最后一页，且文章有剩余，则添加余下的博文到最后一页
        if i == ps - 1 and len(load_blogdatajson(BLOGDATAJSON)) % cs > 0:
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
        context["page_num"] = str(i) + ' / ' + str(ps - 1)
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
            context["title"] = "List Pages" + " 第" + str(i) + "页"
            async with aiofiles.open(os.path.join(BLOGPAGES, 'list_' + str(i) + '.html'), mode='w', encoding='utf-8') as f:
                await f.write(tmp.render(**context))
                print('生成list_' + str(i) + '.html 成功！')


def create_archives_html():
    """生成archives.html"""
    blog_data = load_blogdatajson(BLOGDATAJSON)
    config = load_configjson(CONFIGJSON)
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
    context["title"] = "Archives"
    with open(archives_html_path, mode='w', encoding='utf-8') as f:
        f.write(tmp.render(**context))
        print('生成archives.html成功！')


def create_tags_html():
    """生成archives.html"""
    blog_data = load_blogdatajson(BLOGDATAJSON)
    config = load_configjson(CONFIGJSON)
    # 设置jinja模板
    env = Environment(loader=FileSystemLoader('./templates'))
    context = create_context()
    tmp = env.get_template("tags.html")  # 模板
    tags_html_path = os.path.join(BLOGPAGES, 'tags.html')  # 首页HTML
    # 组装archives页面的上下文数据。
    data = tagsdata(blog_data)
    for item in data:
        item["sum"] = len(item["data"])
    context["tags"] = data
    context["title"] = "Tags"

    with open(tags_html_path, mode='w', encoding='utf-8') as f:
        f.write(tmp.render(**context))
        print('生成tags.html成功！')


def create_allblog():
    '''创建所有blog静态页面'''
    blogdata = load_blogdatajson(BLOGDATAJSON)  # 获得blog的博文数据

    # #单线程创建blogHTML
    # for blog in blogdata:
    #     create_blog_html(mainhtml,blog)

    # #多线程创建
    # with ThreadPoolExecutor(max_workers=5) as ex:
    #     for blog in blogdata:
    #         ex.submit(create_blog_html, mainhtml, blog)

    ct = [create_blog_html(blog) for blog in blogdata]  # 列表生成式
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(ct))
    # loop.close()


async def create_blog_html(blog):
    '''
    创建blog页面
    '''
    # 设置jinja模板
    env = Environment(loader=FileSystemLoader('./templates'))
    tmp = env.get_template("blog.html")  # 模板
    blog_path = os.path.join(BLOGPAGES, blog["url"] + '.html')  # 首页HTML
    create_dir(blog_path)
    context = create_context()
    context["blog"] = blog
    context["data"] = markdown(read_file_without_header(os.path.join(ARTICLES_DIR, blog["url"] + ".md")))
    async with aiofiles.open(blog_path, mode='w', encoding='utf-8') as f:
        await f.write(tmp.render(**context))
        print('生成' + blog["title"] + '博文成功！')


def create_blog(title='', author='', tag='', dir='', pagename=''):
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
        config = load_configjson(CONFIGJSON)
        author = config['blog_author']
    blogfile = os.path.join(ARTICLES_DIR, os.path.join(dir, pagename + '.md'))
    create_dir(blogfile)  # 如果有不存在的目录则创建
    bloghtml = '---' + '\ntitle:' + title + '\nauthor:' + author + '\n\
time:' + create_time + '\ntag:' + tag + '\n+' - --'+\n\
</br>\n\n## 可以开始写blog啦(*￣︶￣)'

    if os.path.isfile(blogfile):
        print('文件存在相同名称，创建失败。')
    else:
        with open(blogfile, mode='w', encoding='utf-8') as f:
            f.write(bloghtml)
        print('blog文章.md创建成功！')
        os.system('code ' + blogfile)  # 使用VS Code打开文件


def create_test(con):
    '''
    生成测试blog默认1000篇，放在目录suiyantest下。
    获取.md的文章信息HTML转化成数组
    :param con: 需要生成的文章数。
    :return: void
    '''
    dir = "suiyantest"
    for i in range(con):
        # 随机生成一些文章数据填充，用来测试
        title = random.choice(
            ("打法撒发射点发斯蒂芬", "斯蒂芬阿斯蒂芬斯蒂芬", "斯蒂芬阿斯蒂芬", "斯蒂芬阿斯蒂芬", "斯蒂芬斯蒂芬阿斯蒂芬3",))
        tag = random.choice(("Java", "JavaScript", "Python", "C++", "程序员",))
        pagename = str(random.randint(99999, 99999999))
        create_blog(title=title, tag=tag, dir=dir,
                    author='', pagename=pagename)
    print("测试文件创建完毕！")


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
        create_blog(title=args.newblog, author=args.author,
                    tag=args.tag, dir=args.dir, pagename=args.pagename, )
    elif args.suiyantest:
        create_test()
    elif args.index:
        create_data_json()
        create_sitemap()
        delete_html_files()
        create_data_json(ARTICLES_DIR, BLOGDATAJSON)
        create_sitemap()
        create_index_html()
        create_archives_html()
        create_tags_html()
        create_allblog()
    elif args.sitemap:
        create_sitemap()
    else:
        print(parser.print_help())  # 默认打印帮助


if __name__ == "__main__":
    create_blog_dir(BLOGPAGES)  # 所有blog目录，存放blog中的所有静态资源。
    # main()
    delete_html_files(BLOGPAGES)
    create_data_json(ARTICLES_DIR, BLOGDATAJSON)
    create_sitemap()
    create_index_html()
    create_archives_html()
    create_tags_html()
    create_allblog()
