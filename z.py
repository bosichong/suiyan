# -*- coding:utf-8 -*-

import argparse
import os
import shutil
import re
import json
import datetime
import random
import time
#线程池
from concurrent.futures import ThreadPoolExecutor
#解析网页创建并填充数据到页面模板
from bs4 import BeautifulSoup 
#导入markdown模块
from markdown import markdown

# from fnmatch import fnmatch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前目录地址
BLOGPAGES = os.path.join(BASE_DIR,"blog")#所有静态资源存放目录
ARTICLES_DIR = os.path.join(BASE_DIR, "articles")  # 博文目录
BLOGLIST = os.path.join(BASE_DIR,"list")

CONFIGJSON = os.path.join(BLOGPAGES,'config.json')
BLOGDATAJSON = os.path.join(BLOGPAGES,'blog_data.json')

JSBUILD = os.path.join(BLOGPAGES,'assets/js/build')
JSSRC =os.path.join(BLOGPAGES,'assets/js/src')
JSUTIL = os.path.join(BLOGPAGES,'assets/js/src/util.js')
JSMAIN = os.path.join(BLOGPAGES,'assets/js/src/main.js')
NN = '\n\n'

TEMPLATES = os.path.join(BLOGPAGES,'assets/templates')#网页模板目录




SUIYANVERSION = "2.0.2"  # 程序版本
# 匹配文章数据的正则
DIVRE = '<div class="blog-article">?([\s\S]*?)</div>'

def xurl(url):
    '''去掉目录直接取文件名'''
    return url.split("/")[-1]#去掉目录，直接取文件名。

def rmblog():
    '''删除blog目录下所有html'''
    for i in os.listdir(BLOGPAGES) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = os.path.join(BLOGPAGES + os.sep , i)#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) and file_data.endswith(".html"):#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
            # print(file_data)

def loadcode(path):
    '''载入文件中的代码'''
    code=''
    with open(os.path.join(path), encoding='utf-8') as f:
        code = f.read()    
    
    return code

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

def load_configjson():
    '''载入blog配置文件config.json'''
    config_code = loadcode(CONFIGJSON)
    
    config = json.loads(config_code)
    return config

def load_blogdatajson():
    '''载入blog配置文件config.json'''
    blogdata = loadcode(BLOGDATAJSON)
    
    blog = json.loads(blogdata)
    return blog

configdata = load_configjson()#得到blog的配置Python字典
blogdata = load_blogdatajson()#获得blog的博文数据

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
                    # print(f_data)
                    data_json.append(f_data)  # 添加到需要返回的数据数组中
    
    data_json.sort(key = lambda x:x["time"],reverse = True)#对数组进行降序排序
    data_json_str = json.dumps(data_json, ensure_ascii=False)  # 转化为json字符串
    # print(data_json_str)
    return data_json_str

def write_data_json(json_str = create_blog_data_Json(ARTICLES_DIR, BASE_DIR)):
    '''
    创建blog索引.json
    :param json_str: json 字符串
    :return:
    '''
    with open(os.path.join(BLOGPAGES, 'blog_data.json'), mode='w', encoding='utf-8') as f:
        f.write(json_str)
    load_blogdatajson()
    # print("写入blog数据索引完毕！")

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

def create_sitemap():
    '''创建网站地图'''
    siteurl = configdata["siteurl"]
    tmpstr = ""
    blogdata = []
    with open(os.path.join(os.path.dirname(__file__), BLOGDATAJSON), mode='r', encoding='utf-8') as f:
        blogdata = json.load(f)
    for ar in blogdata:
        tmpstr += '<url>\
        <loc>'+siteurl+ar["url"]+'.html</loc>\
        <lastmod>'+ar["time"]+'</lastmod>\
        <changefreq>daily</changefreq>\
        <priority>0.8</priority></url>'

    xml_str ='<?xml version="1.0" encoding="utf-8"?>\
    <urlset>'+tmpstr+'</urlset>'
    # print(xml_str)
    with open(os.path.join(BLOGPAGES, 'sitemap.xml'), mode='w', encoding='utf-8') as f:
        f.write(xml_str)

def create_appjs():
    '''合并公共JS文件，每个JS文件的前部文件'''
    util_code = loadcode(JSUTIL)
    main_code= loadcode(JSMAIN)

    app_js_code = util_code + NN + main_code



    # print(app_js_code)
    return app_js_code

def create_js_index():
    '''合并生成环境index.js'''
    index_path_bulid = os.path.join(JSBUILD,'index.js')#和并成功的JS
    index_path_src = os.path.join(JSSRC,'index.js')#源文件
    index_src_code=loadcode(index_path_src)

    index_bulid_code = create_appjs()+index_src_code#合并生产环境下的index.js的代码

    with open(index_path_bulid, mode='w', encoding='utf-8') as f:
        f.write(index_bulid_code)
        print('合并生成环境index.js成功！')

def create_js_archive():
    '''合并生成环境archive.js'''
    archive_path_bulid = os.path.join(JSBUILD,'archive.js')#和并成功的JS
    archive_path_src = os.path.join(JSSRC,'archive.js')#源文件
    archive_src_code=loadcode(archive_path_src)

    archive_bulid_code = create_appjs()+archive_src_code#合并生产环境下的index.js的代码

    with open(archive_path_bulid, mode='w', encoding='utf-8') as f:
        f.write(archive_bulid_code)
        print('合并生成环境archive.js成功！')

def create_js_p():
    '''合并生成环境p.js'''
    p_path_bulid = os.path.join(JSBUILD,'p.js')#和并成功的JS
    p_path_src = os.path.join(JSSRC,'content.js')#源文件
    p_src_code=loadcode(p_path_src)

    p_bulid_code = create_appjs()+p_src_code#合并生产环境下的index.js的代码

    with open(p_path_bulid, mode='w', encoding='utf-8') as f:
        f.write(p_bulid_code)
        print('合并生成环境p.js成功！')
    
def create_js_tags():
    '''合并生成环境tags.js'''
    tags_path_bulid = os.path.join(JSBUILD,'tags.js')#和并成功的JS
    tags_path_src = os.path.join(JSSRC,'tags.js')#源文件
    tags_src_code=loadcode(tags_path_src)

    tags_bulid_code = create_appjs()+tags_src_code#合并生产环境下的index.js的代码

    with open(tags_path_bulid, mode='w', encoding='utf-8') as f:
        f.write(tags_bulid_code)
        print('合并生成环境tags.js成功！')

def create_alljs():
    '''合并所用生产环境下的JS文件'''
    #清理jsbuild目录。
    if os.path.isdir(JSBUILD):
        shutil.rmtree(JSBUILD)#删除目录
    os.mkdir(JSBUILD)#创建目录
    create_js_index()
    create_js_archive()
    create_js_p()
    create_js_tags()

def create_main_html(str):
    '''生成所有静态页面的公共代码，包括：<head> <side> <footer>'''
    


    main_path = os.path.join(TEMPLATES,'main.html')
    main_html_code = loadcode(main_path)
    mainbfs = BeautifulSoup(main_html_code, 'html.parser')

    blogname = mainbfs.find(name='h1',attrs={"class":"blog-name"}).find('a')
    blogdescription = mainbfs.find(name='div',attrs={"class":"blog-description"})
    profileimage = mainbfs.find(name='img',attrs={"class":"profile-image"})
    blogsns = mainbfs.find(name='ul',attrs={"class":"social-list"})#sns
    blognav = mainbfs.find(name='ul',attrs={"class":"blog-nav"})#blognav
    blogfooter = mainbfs.find(name='footer',attrs={"class":"footer"})#blognav

    #blogHTMLhead mata 信息
    metaheml = '<title>'+configdata['blog_name']+'</title>\
        <meta name="keywords" content="' + configdata['meta_keywords'] + '">\
        <meta name="description" content="' + configdata['meta_description'] + '">\
        <meta name="author" content="' + configdata['blog_author'] + '">';
    metabfs = BeautifulSoup(metaheml,'html.parser')
    # print(metaheml) 
    viewport = mainbfs.find(name='meta',attrs={"name":"viewport"})#返回列表
    # print(viewport)
    viewport.insert_after(metabfs)
    
    print('head的代码输出完毕！')


    #修改blog标题

    blogname.string = configdata['blog_name']

    #修改blog简介
    
    blogdescription.string = configdata['blog_description']

    #修改blog头像
    
    profileimage['src']= configdata['profile_image']



    #添加SNS    
    for sns in configdata['blog_sns']:
        snshtml = BeautifulSoup('<li><a class="hide" href="' + sns["url"] + '" target="blank_blank">\
        <i class="fa fa-' + sns["ico"] + ' fa-lg"></li></a></i>'+'\n',"html.parser")
        blogsns.append(snshtml)


    #添加导航
    
    for nav in configdata['nav']:
        navhtml = BeautifulSoup('<li class="nav-item hide"><a class="nav-link"\
         href="' + nav["url"] + '"> <span><i class="fa fa-' + nav["ico"] + ' fa-lg"></i>\
         ' + nav["text"] + '</sapn></a></li>'+'\n',"html.parser")
        blognav.append(navhtml)

    blogfooter.append(BeautifulSoup(str,"html.parser"))#添加相关的Js文件
    # print(mainbfs.head)#headhtml 代码格式化输出


    print('main.html 生成完毕！')
    return mainbfs

def create_index_html():
    '''创建blog站点首页'''

    
    jshtml ='<!-- 站点自定义JS -->\
  <script src="./assets/js/build/index.js"></script>\
  <!-- highlight.js Markdown代码美化 -->\
  <script src="./assets/plugins/highlight/highlight.pack.js"></script>\
  <script >hljs.initHighlightingOnLoad();</script>'


    indexhtml  = str(create_main_html(jshtml))

    cs = int(configdata['blog_list'])#每页的文章个数
    ps = 0#列表页个数
    #页数计算，如果有余数多加一页
    if len(blogdata)%cs == 0 :
        ps = int(len(blogdata)/cs)
    else:
        ps = int(len(blogdata)/cs +1)
    



    
    #单线程
    # for i in range(ps):
    #     create_list_html(indexhtml,i,ps,cs)

    with ThreadPoolExecutor(max_workers=5) as ex:
        for i in range(ps):
            #单线程
            # create_list_html(indexhtml,i,ps,cs)
            # #多线程创建
            ex.submit(create_list_html,indexhtml,i,ps,cs)

def create_list_html(indexhtml,i,ps,cs):
    '''生成列表单页HTML'''

    indexbfs = BeautifulSoup(indexhtml, 'html.parser')
    bloglist = indexbfs.find(name='section',attrs={"class":"blog-list"})

    
    bdata = ''
    #组装每页的blog文章
    if i < ps :
        # print(i,ps)
        maxp= cs*i+cs
        #若是最后一页，且文章有剩余，则添加余下的博文到最后一页
        if i == ps-1 and len(blogdata)%cs > 0 :
            maxp = cs*i+(len(blogdata)%cs)
        for p in range(cs*i,maxp):
            #处理markdownblog
            # print(p)
            # print(cs*i,maxp,cs-len(blogdata)%cs)
            # print(blogdata[p])
            #组装每一页的博文HTML代码
            bdata += markdown(loadcode(os.path.join(ARTICLES_DIR ,blogdata[p]["url"]+'.md')))
        #组装分页代码
        prevurl = 'list_'+str(i-1)+'.html'
        nexturl = 'list_'+str(i+1)+'.html'
        if i == 0 :
            prevurl = '#'
        if i == ps-1 :
            nexturl = '#'

        
        p_prev = '<a href="'+prevurl+'"><button type="button" class="prev btn btn-primary" >Previous</button></a>'
        p_next = '<a href="'+nexturl+'"><button type="button" class="next btn btn-primary" >Next</button></a>'
        p_page ='<button type="button" class="page btn btn-primary">'+str(i)+' / '+str(ps)+' </button>'
        suiyanpage ='<div class="spage">\
        <div id="suiyanpage" class="pagination pagination4 btn-group" role="group" aria-label="Basic example">\
        '+p_prev+p_page+p_next+'\
        </div></div>'

        bdata+=suiyanpage




        #组装首页的博文列表及分页
        homelistbfs = BeautifulSoup(bdata,'html.parser')
        datalist = BeautifulSoup('<div class="data-list list-group">'+str(homelistbfs)+'</div>','html.parser')#首页博文列表
        blbfs = BeautifulSoup(str(datalist),'html.parser')
        bloglist.append(blbfs)
       

        if i == 0:
            #输出最终的listHTML
            indexhtmlpath = os.path.join(BLOGPAGES,'index.html')#首页HTML
            with open(indexhtmlpath, mode='w', encoding='utf-8') as f:
                f.write(indexbfs.prettify())
                print('合并生成环境index.html成功！')

            with open(os.path.join(BLOGPAGES,'list_'+str(i)+'.html'), mode='w', encoding='utf-8') as f:
                f.write(indexbfs.prettify())
                print('合并生成环境list_'+str(i)+'.html 成功！')

        else:
            with open(os.path.join(BLOGPAGES,'list_'+str(i)+'.html'), mode='w', encoding='utf-8') as f:
                f.write(indexbfs.prettify())
                print('合并生成环境list_'+str(i)+'.html 成功！')
        
        bloglist.string = ''

def formatData():
    '''日志归档排序后的数据'''
    tmplist = []
    for item in blogdata:
        
        tmpdate = item["time"][:7]
        # print(tmpdate)
        if len(tmplist) == 0:
            tmpobj = {}
            tmpobj["date"] = tmpdate
            tmpobj["data"] = []
            tmpobj["data"].append(item)
            tmplist.append(tmpobj)
            

        else:
            # print(tmplist[len(tmplist)-1]["date"])
            if(tmplist[len(tmplist)-1]["date"] == tmpdate):
                tmplist[len(tmplist)-1]["data"].append(item)
            else:
                tmpobj = {}
                tmpobj["date"] = tmpdate
                tmpobj["data"] = []
                tmpobj["data"].append(item)
                tmplist.append(tmpobj)
    return tmplist

def tagsData():
    '''tag归档排序后的数据'''
    tmplist = []
    for item in blogdata:
        tmptag = item["tag"]
        if len(tmplist) == 0:
            tmpobj = {}
            tmpobj["tag"] = tmptag
            tmpobj["data"] = []
            tmpobj["data"].append(item)
            tmplist.append(tmpobj)

        else:
            isok = True
            for i in tmplist:
                if i["tag"] == tmptag:
                    i["data"].append(item)
                    isok = False
                    break
            if isok:
                tmpobj = {}
                tmpobj["tag"] = tmptag
                tmpobj["data"] = []
                tmpobj["data"].append(item)
                tmplist.append(tmpobj)
    # print(tmplist)
    return tmplist

def create_archives_html():
    '''生成archives.html'''
    archivestmlpath = os.path.join(BLOGPAGES,'archives.html')#首页HTML

    jshtml ='<!-- 站点自定义JS -->\
  <script src="./assets/js/build/archive.js"></script>'

    archiveshtml  = str(create_main_html(jshtml))
    archivesbfs = BeautifulSoup(archiveshtml, 'html.parser')
    archivesbfs.title.append("  archives日志归档")
    section = archivesbfs.find(name='section',attrs={"class":"blog-list"})

    lihtml = ''
    data = formatData()
    for l in data:
        lihtmlstr=''
        for j in l["data"]:
            burl = j["url"]
            if "/" in burl:
                burl = xurl(burl)
            lihtmlstr += '<li class="list-group-item"><a href="'+burl+'.html" target="_blank">'+j["title"]+'</a> <span title="发布日期">'+j["time"]+'</span></li>'
        ulhtmstr = '<ul class="car-monthlisting list-group" style="display: block;">'+lihtmlstr+'</ul>'
        lihtml += '<li class="nav-item "><span class="car-yearmonth meta" style="cursor:pointer;"><i class="fa fa-list-ul" aria-hidden="true">\
        </i> '+l["date"]+' <span class="meta" title="文章数量">(共'+str(len(l["data"]))+'篇文章)</span></span>'+ulhtmstr+'</li>'

    htmlstr ='<header class="entry-header">\
                <h1 class="single-title">文章归档</h1>\
                <div class="archives-meta"><span class="meta">共有文章:'+str(len(blogdata))+'篇,最后更新:'+blogdata[0]["time"]+'</span></div>\
            </header>\
            <button type="button" class="btn btn-info btn-sm car-all" data-toggle="button" aria-pressed="false" autocomplete="off">折叠所有</button>\
            <ul class="car-list navbar-nav">\
            '+lihtml+'\
            </ul>'
    # print(htmlstr)

    tmhtml = BeautifulSoup(htmlstr, 'html.parser')
    section.append(tmhtml)

    # print(archivesbfs.prettify())
                #输出最终的listHTML
    with open(archivestmlpath, mode='w', encoding='utf-8') as f:
        f.write(archivesbfs.prettify())
        print('合并生成环境archives.html成功！')

def create_tags_html():
    '''生成tags.html页面'''
    tagshtmlpath = os.path.join(BLOGPAGES,'tags.html')#首页HTML

    jshtml ='<!-- 站点自定义JS -->\
  <script src="./assets/js/build/tags.js"></script>'

    tagshtml  = str(create_main_html(jshtml))
    tagsbfs = BeautifulSoup(tagshtml, 'html.parser')
    tagsbfs.title.append("  Tags 标签云")
    section = tagsbfs.find(name='section',attrs={"class":"blog-list"})

    data = tagsData()
    tagstr = ''
    cads = ''
    k=0
    for item in data:
        # print(item)
        tagstr += '<button class="tag-bt btn btn-info btn-sm" type="button" data-toggle="collapse" \
        data-target="#cad'+str(k)+'" aria-expanded="false" aria-controls="collapseExample">\
        <span class="tagval">'+item["tag"]+'</span> <span class="badge badge-light">'+str(len(item["data"]))+'</span></button>'
        tmpcad = ''
        for i in item["data"]:
            burl = i["url"]
            if "/" in burl:
                burl = xurl(burl)
            tmpcad+='<li class="list-group-item"><a target="_blank" href="'+burl+'.html">'+i["title"]+'</a> \
            <span class="meta" title="发布日期">'+i["time"]+'</span></li>'
        
        cads += '<div class="collapse" id="cad'+str(k)+'">\
                    <div class="card-body">\
                    <ul class="navbar-nav">'+tmpcad+'</ul></div></div>'
        
        k+=1

    tmpstr ='<header class="entry-header ">\
                <h1 class="single-title">TAGS</h1>\
                <div class="tags bd-example">\
                '+tagstr+'\
                </div>\
            </header>'+cads
    tmphtml = BeautifulSoup(tmpstr,'html.parser')
    section.append(tmphtml)

    with open(tagshtmlpath, mode='w', encoding='utf-8') as f:
        f.write(tagsbfs.prettify())
        print('合并生成环境tags.html成功！')

def create_allblog():
    '''创建所有blog静态页面'''
    
    jshtml ='<!-- 站点自定义JS -->\
  <script src="./assets/js/build/p.js"></script>\
  <!-- highlight.js Markdown代码美化 -->\
  <script src="./assets/plugins/highlight/highlight.pack.js"></script>\
  <script >hljs.initHighlightingOnLoad();</script>'

    mainhtml  = str(create_main_html(jshtml))
    
    

    # #单线程创建blogHTML
    # for blog in blogdata:
    #     create_blog_html(mainhtml,blog)

    # #多线程创建
    with ThreadPoolExecutor(max_workers=5) as ex:
        for blog in blogdata:
            ex.submit(create_blog_html,mainhtml,blog)
        

def create_blog_html(mainhtml,blog):
    '''
    创建blog页面
    '''
    mainbfs = BeautifulSoup(mainhtml, 'html.parser')
    bloglist = mainbfs.find(name='section',attrs={"class":"blog-list"})
    mainbfs.title.string= ''
    mainbfs.title.append(blog["title"]+'  碎言博客')
    md_path = os.path.join(ARTICLES_DIR,blog["url"]+'.md')
    md_html_code = loadcode(md_path)
    mdbfs = markdown(md_html_code)#博文
    burl = blog["url"]
    if "/" in burl:
        burl = xurl(burl)

    githtml ='<section class="blog-p text-center">\
            <div class="gitedit">发现错误？想参与编辑？<a href="'+configdata["github"]+burl+'.md" class="giturl" target="_blank">\
                在 GitHub 上编辑此页！</a></div>\
            <p class="qqqun">如果您有什么问题，欢迎加入Python/Javascript学习讨论群询问</p>\
            <p class="qqqun">Python/Javascript学习QQ群号：217840699</p>\
        </section>'

    #外层代码
    whtml ='<div class="container-fluid" id="rt">'+mdbfs+githtml+'<div class="blog-article"></div>'
    blogpagehtml = BeautifulSoup(whtml, 'html.parser')
    bloglist.append(blogpagehtml)
    blogurl = os.path.join(BLOGPAGES,burl+'.html')

    # 将文件路径分割出来
    file_dir = os.path.split(blogurl)[0]
    # 判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)


    print(blogurl)
    with open(blogurl, mode='w', encoding='utf-8') as f:
        f.write(mainbfs.prettify())
        print('生成'+blog["title"]+'页面成功！')
    bloglist.string=''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="查询程序版本", action="store_true")
    parser.add_argument("-i", "--index", help="一键更新索引blog数据json及全站的静态资源", action="store_true")
    parser.add_argument("-s", "--sitemap", help="更新sitemap.mxl", action="store_true")
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
        write_data_json()
        print("blog_data.json索引文件更新完毕！")
        create_sitemap()
        print("sitemap.xml 更新完毕！")
    elif args.suiyantest:
        create_test(args.suiyantest)
        print("测试文件创建完毕！")
    elif args.index:
        write_data_json()
        print("blog_data.json索引文件更新完毕！")
        create_sitemap()
        print("sitemap.xml更新完毕！")
        create_alljs()
        print("所有JS文件合并更新完毕！")
        rmblog()
        print("清空所有html!")
        create_index_html()
        print("首页及blog列表页更新完毕！")
        create_archives_html()
        print("文章归档页更新完毕！")
        create_tags_html()
        print("标签页更新完毕！")
        create_allblog()
        print("所有blog文章页更新完毕！")
    elif args.sitemap:
        create_sitemap()
    else:
        print(parser.print_help())  # 默认打印帮助

    




if __name__ == "__main__":
    main()

    




