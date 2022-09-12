import tkinter as tk
from tkinter import ttk
from connectApi import login,getThing

def insert():
    # 插入数据
    info = [
        ['食品', '薯片', '2021-12-12', '2022-01-25'],
        ['食品', '巧克力', '2021-11-11', '2022-11-08'],
        ['药品', '疯子吃的', '2021-11-11', '2022-09-12' ],
        ['食品', '番薯', '2021-11-11', '2022-04-01'],
        ]
    for index, data in enumerate(info):
        table.insert('', 'end', values=data)  # 添加数据到末尾


def delete():
    obj = table.get_children()  # 获取所有对象
    for o in obj:
        table.delete(o)  # 删除对象


if __name__ == '__main__':
    pass
    win = tk.Tk()  # 窗口
    win.title('物品临期助手')  # 标题
    screenwidth = win.winfo_screenwidth()  # 屏幕宽度
    screenheight = win.winfo_screenheight()  # 屏幕高度
    width = 1000
    height = 500
    x = int((screenwidth - width) / 2)
    y = int((screenheight - height) / 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

    tabel_frame = tk.Frame(win)
    tabel_frame.pack()

    xscroll = tk.Scrollbar(tabel_frame, orient='horizontal')
    yscroll = tk.Scrollbar(tabel_frame, orient='vertical')

    columns = ['类型', '物品', '生产时间', '截止日期']

    table = ttk.Treeview(
            master=tabel_frame,  # 父容器
            height=10,  # 表格显示的行数,height行
            columns=columns,  # 显示的列
            show='headings',  # 隐藏首列
            xscrollcommand=xscroll.set,  # x轴滚动条
            yscrollcommand=yscroll.set,  # y轴滚动条
            )
    for column in columns:
        table.heading(column=column, text=column, anchor='center',
                      command=lambda name=column:
                      win.messagebox.showinfo('', '{}描述信息~~~'.format(name)))  # 定义表头
        table.column(column=column, width=100, minwidth=100, anchor='center', )  # 定义列
    xscroll.config(command=table.xview)
    xscroll.pack(side='bottom', fill='x')
    yscroll.config(command=table.yview)
    yscroll.pack(side='right', fill='y')
    table.pack(fill='both', expand=True)

    insert()
    f = tk.Frame()
    f.pack()
    tk.Button(f, text='添加', bg='yellow', width=20, command=insert).pack(side='left')
    tk.Button(f, text='删除', bg='pink', width=20, command=delete).pack(side='left')
    win.mainloop()