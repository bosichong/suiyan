# -*- coding:utf-8 -*-
import s
import tkinter as tk

from utils import get_current_year


def upall():
    s.create_all()


def upindex():
    s.create_data_json(s.ARTICLES_DIR, s.BLOGDATAJSON)
    s.create_sitemap()


def newmd():
    s.create_blog(title='请填写博客标题！',filedir=get_current_year())


def main():
    root = tk.Tk()
    root.title("碎言博客管理程序" + s.SUIYANVERSION)
    root.geometry('+300+300')  # 设置窗口的大小及位置

    frame = tk.Frame(root)
    frame.grid(column=0, row=0, padx=8, pady=4)
    # frame.pack(fill = tk.X, side= tk.TOP)
    mighty = tk.LabelFrame(frame, text=' 博客管理')
    mighty.grid(column=0, row=0, padx=8, pady=4)
    mighty.pack(fill=tk.X, side=tk.TOP)

    bt1 = tk.Button(mighty, width=50, text="新建一篇博客.md",
                    command=newmd).pack(fill=tk.X)
    # bt2 = tk.Button(mighty, text="更新博客索引", command=upindex).pack(fill=tk.X)
    bt3 = tk.Button(mighty, text="更新生成所有静态页面", command=upall).pack(fill=tk.X)

    root.mainloop()


if __name__ == "__main__":
    s.create_blog_dir(s.BLOGPAGES)  # 创建blog目录
    main()
