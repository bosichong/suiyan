# -*- coding:utf-8 -*-
import s
import tkinter as tk
from tkinter import messagebox  # 导入提示窗口包

from utils import get_current_year


def upall():
    s.create_all()
    messagebox.showinfo("提示！", "所有静态资源创建更新完毕！")


def create_test():
    s.create_test(20)
    messagebox.showinfo("提示！", "测试文档创建完毕！")



def newmd():
    s.create_blog(title='请填写博客标题！', filedir=get_current_year())
    messagebox.showinfo("提示！", "文档创建完毕！")


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

    bt1 = tk.Button(mighty, width=50, text="新建一篇博客.md", command=newmd).pack(fill=tk.X)
    bt2 = tk.Button(mighty, text="创建测试文档", command=create_test).pack(fill=tk.X)
    bt3 = tk.Button(mighty, text="更新生成所有静态页面", command=upall).pack(fill=tk.X)

    root.mainloop()


if __name__ == "__main__":
    main()
