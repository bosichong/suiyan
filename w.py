# -*- coding:utf-8 -*-
import z
import tkinter as tk


def upall():
    '''更新所有静态资源'''
    z.write_data_json()
    print("blog_data.json索引文件更新完毕！")
    z.create_sitemap()
    print("sitemap.xml更新完毕！")
    z.create_alljs()
    print("所有JS文件合并更新完毕！")
    z.rmblog()
    print("清空所有html!")
    z.create_index_html()
    print("首页及blog列表页更新完毕！")
    z.create_archives_html()
    print("文章归档页更新完毕！")
    z.create_tags_html()
    print("标签页更新完毕！")
    z.create_allblog()
    print("所有blog文章页更新完毕！")


def upindex():
    z.write_data_json()
    print("blog_data.json索引文件更新完毕！")
    z.create_sitemap()
    print("sitemap.xml更新完毕！")


def newmd():
    z.create_blog(title='请填写博客标题！')


def main():
    root = tk.Tk()
    root.title("碎言博客管理程序" + z.SUIYANVERSION)
    root.geometry('+300+300')  # 设置窗口的大小及位置

    frame = tk.Frame(root)
    frame.grid(column=0, row=0, padx=8, pady=4)
    # frame.pack(fill = tk.X, side= tk.TOP)
    mighty = tk.LabelFrame(frame, text=' 博客管理')
    mighty.grid(column=0, row=0, padx=8, pady=4)
    mighty.pack(fill=tk.X, side=tk.TOP)

    bt1 = tk.Button(mighty, width=50, text="新建一篇博客.md",
                    command=newmd).pack(fill=tk.X)
    bt2 = tk.Button(mighty, text="更新博客索引", command=upindex).pack(fill=tk.X)
    bt3 = tk.Button(mighty, text="更新生成所有静态页面", command=upall).pack(fill=tk.X)

    root.mainloop()


if __name__ == "__main__":
    main()
