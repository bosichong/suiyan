# -*- coding: UTF-8 -*-
"""
@Author   : J.sky
@Mail     : bosichong@qq.com
@Site     : https://github.com/bosichong
@QQ交流群  : python交流学习群号:217840699
@file      :s.py
@time     :2023/03/23

封装了一些常用的方法

"""

import os
import json
import datetime
import shutil
import sys
from loguru import logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前目录地址
LOG_LEVEL = "INFO"
logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
logger.add(os.path.join(BASE_DIR, "logs/logger.log"), level=LOG_LEVEL)
handler_id = logger.add(sys.stderr, level=LOG_LEVEL)


def loadcode(path):
    """载入文件中的代码"""
    try:
        with open(os.path.join(path), encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        logger.error(f"文件{path}不存在")
        code = ''
    return code


def load_configjson(jsonpath):
    """载入blog配置文件config.json"""
    config_code = loadcode(jsonpath)
    config = json.loads(config_code)
    return config


def load_blogdata_json(jsonpath):
    """
    载入blog数据blog_data.json
    return dict
    """
    blogdata = loadcode(jsonpath)
    blog = json.loads(blogdata)
    return blog


def create_blogdata_json(adir):
    """
    递归获得当前目录及其子目录中所有的.md文件列表。
    并创建blog的data索引JSON
    :param adir: 文章日志所在目录
    :param bdir: 站点根目录
    :return: json字符串
    """
    data_json = []
    # 当前目录下所有的文件、子目录、子目录下的文件。
    for root, dirs, files in os.walk(adir):
        for file in files:
            # 值读取.md
            if file.endswith('.md'):
                url = os.path.join(root, file).replace(
                    adir + os.sep, '').replace('.md', '').replace('\\', '/')  # 最后需要组装的相对目录
                furl = os.path.join(root, file)  # 当前文件的绝对目录
                f_data = extract_md_header(furl)  # 获取.md的文章信息转成字典
                f_data["url"] = url
                f_data["uptime"] = get_file_modification_time(os.path.join(root, file))
                data_json.append(f_data)  # 添加到需要返回的数据数组中

    data_json.sort(key=lambda x: x["time"], reverse=True)  # 对数组进行降序排序
    data_json_str = json.dumps(data_json, ensure_ascii=False)  # 转化为json字符串
    return data_json_str


def create_data_json(articles_path, file_path):
    """
    创建blog索引.json
    @param articles_path md文档目录地址
    @param file_path 索引保存的地址
    @return:
    """
    json_str = create_blogdata_json(articles_path)
    with open(file_path, mode='w', encoding='utf-8') as f:
        f.write(json_str)
    logger.info("blog数据索引更新完毕！")


def extract_md_header(file_path):
    """
    把每个md文档头部的信息转换成字典
    @param file_path: 文件路径
    @return: header_dict
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        header_str = content.split('---')[1].strip()
        header_list = header_str.split('\n')
        header_dict = {}
        for item in header_list:
            try:
                key, value = item.split(':', 1)
                key = key.strip()
                value = value.strip()
            except ValueError:
                logger.error(f"错误：{header_list} 无法分割成键值对")
                continue
            header_dict[key] = value
        return header_dict


def create_dir(dir_path):
    """
    判断目录是否存在，不存在则创建
    @param dir_path: 目录路径
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logger.info(f"目录 {dir_path} 创建成功")


def xurl(url):
    """
    去掉目录直接取文件名
    @param url: 文件路径
    @return: 文件名
    """
    return os.path.basename(url)


def clear_build(dir_path):
    """
        递归删除目录和子目录下所有的.html文件。
        @param dir_path: 目录路径
        """
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.html'):
                os.remove(os.path.join(root, file))
                logger.debug(f".html文件 {file} 删除成功")
    logger.info("清理所有静态html成功！")


def calculate_page_num(cs, num):
    """
    根据每页文章数和文章总数计算返回页数
    @param cs: 每页文章数
    @param num: 文章总数
    @return: 页数
    """
    if num % cs == 0:
        return int(num / cs)
    else:
        return int(num / cs + 1)


def read_file_without_header(file_path):
    """
    读取一个.md的博文的数据，去除其头部由"---"包围的内容包括"---"，返回其余所有文本内容。
    @param file_path: 文件路径
    @return: 文件内容
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        return content.split('---')[2].strip()


def formatdata(blogdata):
    '''日志归档排序后的数据'''
    tmplist = []
    for item in blogdata:
        tmpdate = item["time"][:7]
        if not tmplist or tmplist[-1]["date"] != tmpdate:
            tmpobj = {"date": tmpdate, "data": []}
            tmplist.append(tmpobj)
        tmplist[-1]["data"].append(item)
    return tmplist


def create_tagsdata(blogdata):
    '''
    tag归档排序后的数据
    支持多标签，用","号分隔。
    '''
    tag_dict = {}
    for item in blogdata:
        tmptags = item["tag"].split(",")
        for tag in tmptags:
            if tag not in tag_dict:
                tag_dict[tag] = {"tag": tag, "data": []}
            tag_dict[tag]["data"].append(item)
    return list(tag_dict.values())


def create_file_dir(blogurl):
    '''
    将文件路径从一个文件地址中分割出来
    判断文件路径是否存在，如果不存在，则创建，此处是创建多级目录
    '''
    file_dir = os.path.split(blogurl)[0]
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)


def create_blog_url_jsfile(path, str):
    """
    创建rul.js文件，这个文件主要是用来定义站内搜索使用的.json文件的地址。
    """
    with open(path, mode='w', encoding='utf-8') as f:
        f.write(str)


def copy_file(src_file, dst_file):
    """
    读取一个文件的全部内容，保存到另一个目录，如果文件存在则覆盖
    @param src_file: 源文件路径
    @param dst_file: 目标文件路径
    """
    with open(src_file, 'rb') as f:
        content = f.read()
        with open(dst_file, 'wb') as f2:
            f2.write(content)
    logger.info(f"文件{src_file}已复制到{dst_file}")


def get_current_year():
    """
    返回当年的年份字符串
    """
    return str(datetime.datetime.now().year)


def copy_dir(src_dir, dst_dir):
    """
    遍历源目录，提取子目录和文件，复制目标目录，先创建目录和子目录，如果不存在则创建，在复制文件到目标目录的对应目录下，文件存在则覆盖。
    @param src_dir: 源目录路径
    @param dst_dir: 目标目录路径
    """
    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)


def copy_all_files(src_dir, dst_dir):
    """
    复制源目录根目录下所有文件到指定目录
    @param src_dir: 源目录路径
    @param dst_dir: 目标目录路径
    """
    for file in os.listdir(src_dir):
        src_file = os.path.join(src_dir, file)
        dst_file = os.path.join(dst_dir, file)
        if os.path.isfile(src_file):
            copy_file(src_file, dst_file)


def get_file_modification_time(file_path):
    """
    获取文件的更新时间
    @param file_path: 文件路径
    @return: 更新时间
    """
    return datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')


def get_prev_next(title, blog_data):
    """
    返回博文的上一篇和下一篇文章
    Args:
        blog_data (_type_): _description_
    return dict
    """
    pn = {}
    for i in range(len(blog_data)):
        if blog_data[i]["title"] == title:
            if i > 0:
                pn["prev"] = blog_data[i - 1]
            else:
                pn["prev"] = None
            if i < len(blog_data) - 1:
                pn["next"] = blog_data[i + 1]
            else:
                pn["next"] = None
            break
    return pn


def get_related(tstr, tags, blog):
    """
    返回一个列表，包含了当前文章的相关文章。
    """
    # logger.debug(tags)
    # logger.debug(blog)
    tl = tstr.split(",")
    arr = []
    for t in tl:
        for i in range(len(tags)):
            # 如果文章标签相同，但相关文章的列表中部存在则添加。
            if t == tags[i]["tag"] and tags[i] not in arr:
                arr += tags[i]["data"]
    arr1 = remove_duplicates(arr)
    arr2 = []
    for j in arr1:
        if j != blog:
            if len(arr2) < 10:  # 只保留最多10个相关文章。
                arr2.append(j)

    return arr2


def remove_duplicates(l):
    """
    list去重
    """
    new_list = []
    for i in l:
        if i not in new_list:
            new_list.append(i)
    return new_list


if __name__ == "__main__":
    pass
