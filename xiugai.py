from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from PIL import Image, ImageTk


class MyTable(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack()  # frame加入root
        tableColumns = ['序号', '权限', '用户', '密码']
        tableValues = [
            ["1", "0", "user1", "password1"],
            ["2", "1", "user2", "password2"],
            ["3", "1", "user3", "password3"],
            ["4", "2", "user4", "password4"],
            ["5", "2", "user5", "password5"],
            ["6", "3", "user4", "password6"],
            ["7", "2", "user7", "password7"],
            ["8", "2", "user8", "password8"],
            ["9", "1", "user9", "password9"]
        ]
        # 设置滚动条
        xscroll = Scrollbar(self, orient=HORIZONTAL)
        yscroll = Scrollbar(self, orient=VERTICAL)
        xscroll.pack(side=BOTTOM, fill=X)
        yscroll.pack(side=RIGHT, fill=Y)
        self.table = ttk.Treeview(
            master=self,  # 父容器
            columns=tableColumns,  # 列标识符列表
            height=30,  # 表格显示的行数
            show='headings',  # 隐藏首列
            style='Treeview',  # 样式
            xscrollcommand=xscroll.set,  # x轴滚动条
            yscrollcommand=yscroll.set  # y轴滚动条
        )
        xscroll.config(command=self.table.xview)
        yscroll.config(command=self.table.yview)

        self.table.pack()  # TreeView加入frame

        # self.table.heading(column="#0", text="用户头像", anchor=CENTER, command=lambda: print("您点击了“用户头像”列"))  # 定义表头
        for i in range(len(tableColumns)):
            self.table.heading(column=tableColumns[i], text=tableColumns[i], anchor=CENTER,
                               command=lambda: print(tableColumns[i]))  # 定义表头
            self.table.column(tableColumns[i], minwidth=100, anchor=CENTER, stretch=True)  # 定义列
        style = ttk.Style(master)
        style.configure('Treeview', rowheight=40)
        self.image = ImageTk.PhotoImage(Image.open("ins.jpg"))
        for data in tableValues:
            # insert()方法插入数据
            self.table.insert('', 'end', text="这里是头像", image=self.image, value=data)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('800x300')
    root.title("TreeView演示")
    MyTable(root)
    root.mainloop()