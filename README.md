# 碎言静态博客

<a href='https://gitee.com/J_Sky/suiyan/stargazers'><img src='https://gitee.com/J_Sky/suiyan/badge/star.svg?theme=dark' alt='star'></img></a>

### 介绍
碎言这个名称取自与"碎言片语"，码兄累了吗？累了就休息一下，为未来的自己留下一些碎言片语吧。


演示(github)： [碎言博客](https://2vv.net)


![](blog/assets/images/fabu.png)

### 软件架构
前端使用了`jQuery，bootstrap4,font-awesome-4.07,highlight.js,less,jQuery.toTop等技术框架。`

本地构建博客索引使用了`Python`的相关技术,实现了全站静态页面，并可以通过标题进行全站搜索。

博客文章写作采用Markdown技术支持，让你专注写作更流畅。

推荐使用`Vscode`搭配进行blog文章的编写(因为当创建新文章后会直接使用`vscode`直接打开)

如果新建blog文章无法在`vscode`中打开，请在命令面板中搜索`shell`，在PATH 中安装`code`命令。

博客的管理支持终端和图形界面：

图形界面：

    python3 w.py

![](blog/assets/images/bloggui.png)

终端：

![](blog/assets/images/zhongduan.png)

可以根据自己的喜好进行选择。




### 安装教程

首先克隆下载碎言静态博客，
* [Gitee](https://gitee.com/J_Sky/suiyan)
* [GitHub](https://github.com/Jsky2020/suiyan)

终端运行:

    pip install -r requirements.txt

安装相关依赖

安装完成。

### 创建文章


    python z.py -n 此处写文章标题


这个时候就会在`articles`目录下创建一篇文章,并且使用`vscode`直接打开。


[更多终端操作](https://www.2vv.net/blog/20191230155649.html)

### 创建索引

博客的文章排序及搜索以来此索引`blog_data.json`，每次创建文章的时候回自动更新索引，但是如果你修改了头部的一些索引信息，则需要运行命令来更新索引。

    python z.py -i

### 修改博客及站长资料

`config.json`里存放着一些站点的资料，上传前建议先修改成自己的资料。

[`config`配置详解点击查看](https://www.2vv.net/blog/20191231133518.html)

### 运行站点

推荐使用`Live Server`这个vscode得插件，非常方便。

### 修改站点样式

碎言博客内置了八套网站样式，四套light四套dark，修改四个html页面的外链CSS连接即可。

具体修改方法请点击查看： [细说修改碎言博客站点的样式](https://www.2vv.net/blog/20191230201529.html)

### 部署

    git push origin master

提交`blog`目录下所有文件到git仓库即可，`blog`就是所有博客的全部文件！

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

