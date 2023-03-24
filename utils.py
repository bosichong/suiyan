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


def extract_md_header(file_path):
    """
    把每个md文档头部的信息转换成字典
    @param file_path: 文件路径
    @return: header_dict
    """
    with open(file_path, 'r') as f:
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
                print(f"错误：{item} 无法分割成键值对")
                continue
            header_dict[key] = value
        return header_dict


def create_blog_dir(dir_path):
    """
    判断目录是否存在，不存在则创建
    @param dir_path: 目录路径
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"目录 {dir_path} 创建成功")


def xurl(url):
    """
    去掉目录直接取文件名
    @param url: 文件路径
    @return: 文件名
    """
    return os.path.basename(url)


def delete_html_files(dir_path):
    """
    递归删除目录和子目录下所有的.html文件。
    @param dir_path: 目录路径
    """
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.html'):
                os.remove(os.path.join(root, file))
                print(f".html文件 {file} 删除成功")


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
    读取一个文件的数据，去除其头部由"---"包围的内容包括"---"，返回其余所有文本内容。
    @param file_path: 文件路径
    @return: 文件内容
    """
    with open(file_path, 'r') as f:
        content = f.read()
        return content.split('---')[2].strip()


def formatdata(blogdata):
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
            # print(tmplist[-1]["date"])
            if tmplist[-1]["date"] == tmpdate:
                tmplist[-1]["data"].append(item)
            else:
                tmpobj = {}
                tmpobj["date"] = tmpdate
                tmpobj["data"] = []
                tmpobj["data"].append(item)
                tmplist.append(tmpobj)
    return tmplist


def tagsdata(blogdata):
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


if __name__ == "__main__":
    print(read_file_without_header("articles/22.md"))
