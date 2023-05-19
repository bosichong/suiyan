# -*- coding: UTF-8 -*-
"""
@Author   : J.sky
@Mail     : bosichong@qq.com
@Site     : https://github.com/bosichong
@QQ交流群  : python交流学习群号:217840699
@file      :s.py
@time     :2023/03/21

"""
import random
import sys

# 导入相关模块
from jinja2 import FileSystemLoader, Environment
import argparse
import asyncio
import aiofiles
# 导入markdown模块
from markdown import markdown
from utils import *

APP_CONFIG = "config.json"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前目录地址
CONFIG = load_configjson(os.path.join(BASE_DIR, APP_CONFIG))  # 获取当前配置
BLOGPAGES = os.path.join(BASE_DIR, CONFIG["build"])  # 所有静态资源存放目录
ARTICLES_DIR = os.path.join(BASE_DIR, CONFIG["md_dir"])  # 博文目录
THEME = os.path.join(BASE_DIR, "theme")  # 主题目录
CONFIGJSON = os.path.join(BASE_DIR, APP_CONFIG)
BLOGCONFIG = os.path.join(BLOGPAGES, 'config.json')
BLOGDATAJSON = os.path.join(BLOGPAGES, 'blog_data.json')
SUIYANVERSION = "3.1.0"  # 程序版本


def create_context():
    """
    创建模板的上下文
    """
    context = load_configjson(CONFIGJSON)
    # 如果有自定义的上下文，可以在这里添加
    context["title"] = "Home"
    blog_data = load_blogdata_json(BLOGDATAJSON)
    tags = create_tagsdata(blog_data)
    tag_count = len(tags)  # 标签数量
    blog_count = len(blog_data)  # 博文数量
    context["tag_count"] = tag_count
    context["blog_count"] = blog_count
    # dev = 1 确定为本地开发环境，会调用config.json中blog_test_url，方便本地调用。
    # dev = 0 确定为线上生产模式，要把最终的网址换成线上的。
    # 这样做主要方便本地调试，因为本地调试静态网页使用的服务器不一，所以产生的地址也会不同。

    if context["dev"]:
        context["site_url"] = context["blog_test_url"]
    else:
        context["site_url"] = context["blog_url"]
    return context


def create_sitemap():
    """创建网站地图"""
    config = load_configjson(CONFIGJSON)  # 得到blog的配置Python字典
    blog_data = load_blogdata_json(BLOGDATAJSON)  # 获得blog的博文数据
    # 设置jinja模板
    env = Environment(loader=FileSystemLoader(os.path.join(THEME, config["theme"])))
    context = create_context()
    tmp = env.get_template("sitemap.xml")  # 模板
    sitemap_path = os.path.join(BLOGPAGES, 'sitemap.xml')  # 网站地图
    context["sitemap_data"] = blog_data
    with open(sitemap_path, mode='w', encoding='utf-8') as f:
        f.write(tmp.render(**context))
    # 创建文本站点地图
    sitemap_text_path = os.path.join(BLOGPAGES, 'sitemap.txt')  # 网站地图
    site_map_url = []
    for blog in blog_data:
        site_map_url.append(context["site_url"] + blog["url"] + ".html")
    site_map_text = "\n".join(site_map_url)
    with open(sitemap_text_path, mode="w", encoding="utf-8") as f:
        f.write(site_map_text)
    logger.info("sitemap.xml、sitemap.txt更新完毕！")


def create_rss():
    """
    创建站点的rss
    """
    config = load_configjson(CONFIGJSON)  # 得到blog的配置Python字典
    blog_data = load_blogdata_json(BLOGDATAJSON)
    # 设置jinja模板
    env = Environment(loader=FileSystemLoader(os.path.join(THEME, config["theme"])))
    context = create_context()
    tmp = env.get_template("rss.xml")  # 模板
    rss_path = os.path.join(BLOGPAGES, 'rss.xml')  # rss
    # 取最近的博文10篇
    rss_data = []
    # 如果blog的文章数小于10个，就取文章数。
    con = 10
    if len(blog_data) < 10:
        con = len(blog_data)
    for i in range(con):
        rss_data.append(blog_data[i])
    context["rss_data"] = rss_data
    with open(rss_path, mode='w', encoding='utf-8') as f:
        f.write(tmp.render(**context))
    logger.info('生成rss.xml成功！')


def create_index_html():
    """
    批量生成首页和列表页
    """
    blog_data = load_blogdata_json(BLOGDATAJSON)
    # 根据博文数量推导列表页数
    config = load_configjson(CONFIGJSON)
    ps = calculate_page_num(config["blog_page_num"], len(blog_data))
    # 设置jinja模板
    env = Environment(loader=FileSystemLoader(os.path.join(THEME, config["theme"])))
    tmp = env.get_template("index.html")  # 模板

    # 异步
    ct = [create_list_html(config, blog_data, tmp, i, ps) for i in range(ps)]  # 列表生成式
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(asyncio.wait(ct))
    logger.info('生成首页、列表页成功！')


async def create_list_html(config, blog_data, tmp, i, ps):
    """
    批量生成首页和列表页的详细方法
    @i 当前页
    @ps 总页数
    """
    articles = []
    context = create_context()
    index_html_path = os.path.join(BLOGPAGES, 'index.html')  # 首页HTML
    cs = config["blog_page_num"]  # 每页博文数量
    if i < ps:
        maxp = cs * i + cs  # 末尾文章数。
        # 若是最后一页，且文章有剩余，则添加余下的博文到最后一页
        if i == ps - 1 and len(load_blogdata_json(BLOGDATAJSON)) % cs > 0:
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
                logger.debug('生成index.html成功！')
            # 同时生成一个列表页的第一页
            async with aiofiles.open(os.path.join(BLOGPAGES, 'list_' + str(i) + '.html'), mode='w', encoding='utf-8') as f:
                await f.write(tmp.render(**context))
                logger.debug('生成list_' + str(i) + '.html 成功！')
        else:
            context["title"] = "List Pages" + " 第" + str(i) + "页"
            async with aiofiles.open(os.path.join(BLOGPAGES, 'list_' + str(i) + '.html'), mode='w', encoding='utf-8') as f:
                await f.write(tmp.render(**context))
                logger.debug('生成list_' + str(i) + '.html 成功！')


def create_archives_html():
    """生成archives.html"""
    blog_data = load_blogdata_json(BLOGDATAJSON)
    config = load_configjson(CONFIGJSON)
    # 设置jinja模板
    env = Environment(loader=FileSystemLoader(os.path.join(THEME, config["theme"])))
    context = create_context()
    tmp = env.get_template("archives.html")  # 模板
    archives_html_path = os.path.join(BLOGPAGES, 'archives.html')  # 首页HTML
    # 组装archives页面的上下文数据。
    data = formatdata(blog_data)
    for k in data:
        k["num"] = len(k["data"])
    context["pages_num"] = len(blog_data)
    context["update"] = blog_data[0]["time"]
    context["archives"] = data
    context["title"] = "Archives"
    with open(archives_html_path, mode='w', encoding='utf-8') as f:
        f.write(tmp.render(**context))
    logger.info('生成archives.html成功！')


def create_tags_html():
    """生成archives.html"""
    blog_data = load_blogdata_json(BLOGDATAJSON)
    config = load_configjson(CONFIGJSON)
    # 设置jinja模板
    env = Environment(loader=FileSystemLoader(os.path.join(THEME, config["theme"])))
    context = create_context()
    tmp = env.get_template("tags.html")  # 模板
    tags_html_path = os.path.join(BLOGPAGES, 'tags.html')  # 首页HTML
    # 组装archives页面的上下文数据。
    data = create_tagsdata(blog_data)
    # logger.debug(data)
    for item in data:
        item["sum"] = len(item["data"])
    context["tags"] = data
    context["title"] = "Tags"
    context["tag_num"] = len(data)

    with open(tags_html_path, mode='w', encoding='utf-8') as f:
        f.write(tmp.render(**context))
    logger.info('生成tags.html成功！')


def create_allblog():
    """创建所有blog静态页面"""
    blogdata = load_blogdata_json(BLOGDATAJSON)  # 获得blog的博文数据
    tagsdata = create_tagsdata(blogdata)

    # #单线程创建blogHTML
    # for blog in blogdata:
    #     create_blog_html(mainhtml,blog)

    # #多线程创建
    # with ThreadPoolExecutor(max_workers=5) as ex:
    #     for blog in blogdata:
    #         ex.submit(create_blog_html, mainhtml, blog)

    config = load_configjson(CONFIGJSON)
    # 设置jinja模板
    env = Environment(loader=FileSystemLoader(os.path.join(THEME, config["theme"])))
    tmp = env.get_template("blog.html")  # 模板

    ct = [create_blog_html(blogdata, tagsdata, tmp, blog) for blog in blogdata]  # 列表生成式
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(asyncio.wait(ct))
    # loop.close()
    logger.info('生成所有文章页成功！')


async def create_blog_html(blogdata, tagsdata, tmp, blog):
    """
    创建blog页面
    """

    blog_path = os.path.join(BLOGPAGES, blog["url"] + '.html')  # 首页HTML
    create_file_dir(blog_path)
    context = create_context()
    context["pn"] = get_prev_next(blog["title"], blogdata)  # 前后页面
    context["related"] = get_related(blog["tag"], tagsdata, blog)  # 相关页面
    context["blog"] = blog
    context["data"] = markdown(read_file_without_header(os.path.join(ARTICLES_DIR, blog["url"] + ".md")))
    async with aiofiles.open(blog_path, mode='w', encoding='utf-8') as f:
        await f.write(tmp.render(**context))
        logger.debug('生成' + blog["title"] + '博文成功！')


def create_blog(title='', author='', tag='', filedir='', pagename='', vscode=True):
    """
    创建一篇空白的新blog
    :param title: blog标题
    :param author: blog作者默认为空的话前段渲染为站长昵称，转载可以添加佚名或是原作者。
    :param tag: 标签 默认为为分类
    :param filedir 存放目录
    :param pagename: 当前页面的name 例如"hello188.md",如果为空默认为年月日时间字符串
    :return:
    """
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
    blogfile = os.path.join(ARTICLES_DIR, os.path.join(filedir, pagename + '.md'))
    create_file_dir(blogfile)  # 如果有不存在的目录则创建
    bloghtml = f'---\ntitle: {title}\nauthor: {author}\ntime: {create_time}\ntag: {tag}\ndescription:\n---\n\n\n### 可以开始写blog啦(*￣︶￣)'

    if os.path.isfile(blogfile):
        logger.error('文件存在相同名称，创建失败。')
    else:
        with open(blogfile, mode='w', encoding='utf-8') as f:
            f.write(bloghtml)
        logger.info('blog文章.md创建成功！')
        if vscode:
            os.system('code ' + blogfile)  # 使用VS Code打开文件


def create_blog_jsfile(dev):
    """
    从配置文件里更换前端JavaScript文件中的网站web地址。
    """
    config = load_configjson(CONFIGJSON)
    if dev:
        js_code = "var suiyan = { url : '" + config["blog_test_url"] + "'}"
    else:
        js_code = "var suiyan = { url : '" + config["blog_url"] + "'}"
    create_blog_url_jsfile(os.path.join(BLOGPAGES, "assets/js/url.js"), js_code)
    logger.debug("url.js创建成功！")


def create_test(con):
    """
    生成测试blog默认1000篇，放在目录suiyantest下。
    获取.md的文章信息HTML转化成数组
    :param con: 需要生成的文章数。
    :return: void
    """
    test_dir = "suiyantest"
    for i in range(con):
        # 随机生成一些文章数据填充，用来测试
        title = random.choice(
            ("打法撒发射点发斯蒂芬", "斯蒂芬阿斯蒂芬斯蒂芬", "斯蒂芬阿斯蒂芬", "斯蒂芬阿斯蒂芬", "斯蒂芬斯蒂芬阿斯蒂芬3",))
        tag = random.choice(("Java", "JavaScript", "Python", "C++", "程序员",))
        pagename = str(random.randint(99999, 99999999))
        create_blog(title=title, tag=tag, filedir=test_dir,
                    author='', pagename=pagename, vscode=False)
    logger.info("测试文件创建完毕！")


def create_all():
    """
    一键生成所有静态文件。
    """
    before_create()
    created()
    copy_seo()
    logger.info("所有静态资源创建更新完毕！")


def created():
    """
    创建所有静态资源
    """
    create_index_html()
    create_archives_html()
    create_tags_html()
    create_allblog()
    create_sitemap()
    create_rss()


def before_create():
    """
    这里是所有静态资源生成前的一些处理
    """
    config = load_configjson(CONFIGJSON)  # 加载最新的文件
    create_dir(BLOGPAGES)  # 创建静态文件目录
    clear_build(BLOGPAGES)  # 清理静态文件目录下的HTML
    # 复制配置文件到blog
    copy_file(os.path.join(BASE_DIR, APP_CONFIG), BLOGCONFIG)
    copy_assets()  # 复制其他静态文件
    create_blog_jsfile(config["dev"])  # 创建blog的搜索数据连接前缀。
    create_data_json(ARTICLES_DIR, BLOGDATAJSON)  # 创建blog的索引数据
    create_context()  # 创建blog的上下文。


def copy_assets():
    """
    复制模板下的assets文件到blog/assets
    编辑模板的样式生成静态文件前拷贝过去，方便保存模板样式。
    """
    config = load_configjson(CONFIGJSON)
    tmp_assets_path = os.path.join(THEME, config["theme"], "assets")
    blog_assets_path = os.path.join(BLOGPAGES, "assets")
    create_dir(tmp_assets_path)
    # 复制模板下的js css到blog下
    copy_dir(tmp_assets_path, blog_assets_path)


def copy_seo():
    """
    复制SEO相关的文件到根目录，例如站点验证、robots.txt 等
    """
    seo_dir = os.path.join(BASE_DIR, "seo")
    if os.path.isdir(seo_dir):
        copy_all_files(seo_dir, BLOGPAGES)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="查询程序版本", action="store_true")
    parser.add_argument(
        "-i", "--index", help="一键更新索引blog数据json及全站的静态资源", action="store_true")
    parser.add_argument("-n", "--newblog", help="创建新日志，请输入标题（必填）。", )
    parser.add_argument("-t", "--tag", help="请输入blog的标签TAG", default='')
    parser.add_argument("-a", "--author", help="请输入文章作者，默认调用站长昵称", default='')
    parser.add_argument("-p", "--pagename", help="请输入文章地址页面名称", default='')
    parser.add_argument("-d", "--filedir", help="请输入文章地址所属目录", default=get_current_year())

    parser.add_argument("-test", "--suiyantest",
                        help="生成测试blog,填写需要生成的数目，测试文章放在目录suiyantest下。", type=int, )

    args = parser.parse_args()
    if args.version:
        logger.info(SUIYANVERSION)
    elif args.newblog:
        create_blog(title=args.newblog, author=args.author,
                    tag=args.tag, filedir=args.filedir, pagename=args.pagename, )
    elif args.suiyantest:
        create_test(con=args.suiyantest)
    elif args.index:
        create_all()
    else:
        print(parser.print_help())  # 默认打印帮助


if __name__ == "__main__":
    main()

    # blog_data = load_blogdata_json(BLOGDATAJSON)
    # tagdata = create_tagsdata(blog_data)
    # ts = "前端框架,HTML".split(",")
    # kk = get_related(ts, tagdata,
    #                   {'title':       '2023重学前端:HTML CSS JavaScript基础复习', 'author': 'J.sky', 'time': '2023-04-13 09:59:13',
    #                    'tag':         '前端框架,HTML',
    #                    'description': '最近写了一些前端的项目使用了一些框架例，但是突然发现自己的前端基础是如此的渣，渣的自己好尴尬，遂决定重新学习并复习一下前端的HTML CSS JavaScript基础。',
    #                    'url':         '2023/20230413095913', 'uptime': '2023-04-16 18:03:47'})
    # print(kk)
