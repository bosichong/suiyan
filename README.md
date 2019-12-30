# 碎言静态博客

### 介绍
碎言这个名称取自与"碎言片语"，码兄累了吗？累了就休息一下，为未来的自己留下一些碎言片语吧。
演示： [碎言博客](http://j_sky.gitee.io/suiyan)

![](assets/images/fabu.png)

### 软件架构
前端使用了`jQuery，bootstrap4,font-awesome-4.07,marked.js,highlight.js,jqPaginator,less,等技术框架。`


### 安装教程

首先克隆下载碎言静态博客，
* [Gitee](https://gitee.com/J_Sky/suiyan.git)
* [GitHub](https://github.com/bosichong/suiyan.git)

安装完成。

### 创建文章


    python z.py -n 此处写文章标题


这个时候就会在`articles`目录下创建一篇文章。

### 创建索引

    python z.py -i

### 运行站点

推荐使用`Live Server`这个vscode得插件，非常方便。

### 部署

    git push origin master

提交所有文件到git仓库即可。

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

