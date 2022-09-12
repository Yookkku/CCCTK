# 登录窗口关闭时程序没有停止运行
# 删除时下拉框没有同步更新（列表获取问题）
# 忘记密码形如虚设
# 邮件发了三次，但第一次验证信息可用？
# 加载时下拉框出现问题（添加时更新没有到位）
# 阔别太久有点想哭，难搞

import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.widgets import Combobox
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import *
from connectApi import login, register, getThing, addThing, deleteThing, changeThing, autologin, read_file, check_email
from ttkbootstrap.widgets import DateEntry
from tkinter import messagebox
from timeOperation import Date
import time


class App:
    def __init__(self):
        self.l = []
        self.predate = []
        self.ddl = []
        self.id = []
        self.thingname = []
        self.class_ = []
        self.app = ttk.Window()
        self.window = ttk.Toplevel(self.app)
        self.app.withdraw()
        self.image_file = ttk.PhotoImage(file='ins.jpg')
        self.l1 = ttk.Label(self.window, text='用户名', font=('Arial', 12)).place(x=100, y=150)
        self.l2 = ttk.Label(self.window, text=' 密  码', font=('Arial', 12)).place(x=99, y=200)
        self.var_usr_name = ttk.StringVar()
        self.var_usr_psw = ttk.StringVar()
        self.entry_usr_name = ttk.Entry(self.window, textvariable=self.var_usr_name).place(x=200, y=150)
        self.entry_usr_psw = ttk.Entry(self.window, textvariable=self.var_usr_psw, show='*').place(x=200, y=200)
        self.b1 = ttk.Button(self.window, text='注册新用户', command=self.add_new_usr).place(x=180, y=270)
        self.b2 = ttk.Button(self.window, text='忘记密码', command=self.find_usr).place(x=310, y=270)
        self.b3 = ttk.Button(self.window, text='登录', command=self.entry_).place(x=100, y=270)
        self.iflogin = False
        self.var1 = ttk.IntVar()
        self.b4 = ttk.Checkbutton(self.window, text='自动登录', variable=self.var1, onvalue=1, offvalue=0,
                                  command=self.auto).place(x=420, y=280)

    def creat_main_window(self):
        self.app.title('物品临期提醒助手')
        width = 1500
        height = 1000
        screenwidth = self.app.winfo_screenwidth()
        screenheight = self.app.winfo_screenheight()
        size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.app.geometry(size_geo)

    def creat_login_window(self):
        self.window.title('欢迎来到物品临期提醒助手')
        width = 600
        height = 350
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.window.geometry(size_geo)

    def creat_canvas(self):
        canvas = tk.Canvas(self.window, bg='blue', height=100, width=200)
        canvas.create_image(0, 0, anchor='nw', image=self.image_file)
        canvas.pack()

    def entry_(self):
        # self.entry_usr_psw.bi
        self.usr_psw = self.var_usr_psw.get()
        self.usr_name = self.var_usr_name.get()
        if self.usr_name == '':
            tk.messagebox.showwarning(message='请输入用户名')
        elif self.usr_psw == '':
            tk.messagebox.showwarning(message='请输入密码')
        else:
            log = login(self.usr_name, self.usr_psw, 0)

            if log is True:
                tk.messagebox.showinfo(message='登录成功')
                self.iflogin = True
                self.main_main()
                if self.auto() is True:
                    login(self.usr_name, self.usr_psw, '1') or autologin()
                else:
                    login(self.usr_name, self.usr_psw, '0')
            else:
                tk.messagebox.showwarning(message='请检查输入')

    def main_main(self):
        self.window.destroy()
        coldata = ['id', '类型', '物品名', '提醒日期', '过期日期']
        x = getThing(self.user())
        for i in x:
            self.class_.append(i['class_'])
            self.id.append(i['thingid'])
            self.thingname.append(i['thingname'])
            ddlc = i['ddl']
            self.ddl.append(f'{ddlc[0]}/{ddlc[1]}/{ddlc[2]}')
            predatec = i['predate']
            self.predate.append(f'{predatec[0]}/{predatec[1]}/{predatec[2]}')

        for i in range(len(self.class_)):
            x = []
            x.append(self.id[i])
            x.append(self.class_[i])
            x.append(self.thingname[i])
            x.append(self.predate[i])
            x.append(self.ddl[i])
            self.l.append(x)

        self.table = Tableview(
            master=self.app,
            coldata=coldata,
            rowdata=self.l,
            paginated=True,
            pagesize=29,
            searchable=True,
            bootstyle=PRIMARY,
            # stripecolor=(self.colors.light, None),
            height=29,
            autoalign=False
        )
        self.table.place(x=0, y=0)
        self.div_list = set()
        for i in self.class_:
            self.div_list.add(i)
        self.div_list = list(self.div_list)
        self.div_list.insert(0, '全部')
        self.divvar = ttk.StringVar()
        self.divvar.set('物品分类')
        self.division = Combobox(self.app, textvariable=self.divvar)
        self.division["values"] = self.div_list  # 设置下拉框可选的值
        self.division.bind("<<ComboboxSelected>>", self.get_division)  # 绑定选中事件，执行分类方法
        self.division.place(x=1100, y=100)

        # 这个就是Treeview  !!!!!!!!!，修改可以直接将原本的Treeview改成self.table.view
        self.tianjiatixing = ttk.Label(self.app, text='添加物品处:', font=('Arial', 12)).place(x=1020, y=200)
        self.shanchu = ttk.Label(self.app, text='删除物品处:', font=('Arial', 12)).place(x=1020, y=600)
        self.add_class = ttk.Label(self.app, text='类型', font=('Arial', 12)).place(x=1050, y=260)
        self.add_thingname = ttk.Label(self.app, text='名称', font=('Arial', 12)).place(x=1050, y=310)
        self.add_predate = ttk.Label(self.app, text='存入时间', font=('Arial', 12)).place(x=1050, y=360)
        self.add_ddl = ttk.Label(self.app, text='过期时间', font=('Arial', 12)).place(x=1050, y=410)
        self.class_add = ttk.StringVar()
        self.thingname_add = ttk.StringVar()
        # self.predate_add = DateEntry.getvar(self._predate)
        # self.ddl_add = DateEntry.getvar(self._ddl)
        self._class = ttk.Entry(self.app, textvariable=self.class_add).place(x=1200, y=250)
        self._thingname = ttk.Entry(self.app, textvariable=self.thingname_add).place(x=1200, y=300)
        self._predate = DateEntry(self.app)
        self._ddl = DateEntry(self.app)
        self._predate.place(x=1200, y=350)
        self._ddl.place(x=1200, y=400)
        self.id_dele = ttk.StringVar()
        self.dele_label = ttk.Label(self.app, text='输入id', font=('Arial', 12)).place(x=1050, y=655)
        self.dele_entry = ttk.Entry(self.app, textvariable=self.id_dele).place(x=1200, y=650)
        self.add_button = ttk.Button(self.app, text='添加完成', width=10, command=self.newrow).place(x=1200, y=470)
        self.delete_button = ttk.Button(self.app, text='删除完成', width=10, command=self.derow).place(x=1200, y=720)
        self.entry = ttk.Entry(self.app, textvariable='')
        self.entry.bind("<FocusIn>", self.on_FocusIn)
        self.m = ttk.Menu(self.app, background='red')
        self.fm = ttk.Menu(self.m, tearoff=0, background='red')
        self.m.add_cascade(label='用户操作', menu=self.fm, background='red')  # 以‘file’命名fm
        if self.auto() is True or autologin() is True:
            self.fm.add_command(label='取消自动登录', command=self.cancel_auto)
        self.fm.add_command(label='退出登录', command=self.out_job)
        self.fm.add_command(label='退出程序', command=self.app.quit)
        self.table.view.bind("<Double-1>", self.on_Double_1)
        self.app.config(menu=self.m)
        date = Date()
        self.app.update()
        self.app.deiconify()
        for i, j in zip(self.thingname, self.predate):
            j = tuple(int(i) for i in j.split('/'))
            j = date.getTimestamp(*j)
            self.gettime(i, j)

    def add_new_usr(self):
        self.window_add = ttk.Toplevel(self.window)
        self.window_add.title('注册')
        width = 600
        height = 400
        screenwidth = self.window_add.winfo_screenwidth()
        screenheight = self.window_add.winfo_screenheight()
        size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.window_add.geometry(size_geo)
        self.yx = tk.Label(self.window_add, text='邮箱', font=('Arial', 12)).place(x=100, y=70)
        self.yh = tk.Label(self.window_add, text='用户名', font=('Arial', 12)).place(x=100, y=120)
        self.mm = tk.Label(self.window_add, text='密码', font=('Arial', 12)).place(x=100, y=170)
        self.sign_up_yx = tk.StringVar()
        self.sign_up_yh = tk.StringVar()
        self.sign_up_mm = tk.StringVar()
        self.sign_up_yzm = tk.StringVar()
        self.ey = tk.Entry(self.window_add, textvariable=self.sign_up_yx).place(x=250, y=70)
        self.eh = tk.Entry(self.window_add, textvariable=self.sign_up_yh).place(x=250, y=120)
        self.em = tk.Entry(self.window_add, textvariable=self.sign_up_mm).place(x=250, y=170)
        self.yzm = tk.Entry(self.window_add, textvariable=self.sign_up_yzm).place(x=250, y=220)

        def ok():
            sign_yx = self.sign_up_yx.get()
            sign_yh = self.sign_up_yh.get()
            sign_mm = self.sign_up_mm.get()
            reg = register(sign_yx, sign_yh, sign_mm)
            if reg is True and self.sign_up_yzm.get().lower() == send():
                tk.messagebox.showinfo(message='注册成功')
            else:
                tk.messagebox.showwarning(message=reg)
            self.window_add.destroy()

        self.finish = tk.Button(self.window_add, text='完成', command=ok).place(x=280, y=270)

        def send():
            return check_email(self.sign_up_yx.get())

        self.em = tk.Button(self.window_add, text='发送验证码', command=send).place(x=100, y=220)

    def find_usr(self):
        pass

    def user(self):

        return self.var_usr_name.get() or read_file('username')

    def auto(self):
        if self.var1.get() == 1:
            return True
        else:
            return False

    def cancel_auto(self):
        login(read_file('username'), read_file('password'), '0')

    def out_job(self):
        self.cancel_auto()

    def on_FocusIn(self, event):
        pass

    def on_Double_1(self, event):
        if str(event.widget) == ".!tableview.!treeview" and self.table.view.column != '#1':  # 双击触发的是否为表格
            self.table.view = event.widget
            for item in self.table.view.selection():  # 取消表格选取
                self.table.view.selection_remove(item)
            self.row = self.table.view.identify_row(event.y)  # 点击的行
            self.column = self.table.view.identify_column(event.x)  # 点击的列
            select_id = self.table.view.set(self.row, '#1')
            if self.column != '#1':
                if self.column == '#2':
                    mm = 'class_'
                elif self.column == '#3':
                    mm = 'thingname'
                elif self.column == '#4':
                    mm = 'predate'
                else:
                    mm = 'ddl'
                col = int(str(self.table.view.identify_column(event.x)).replace('#', ''))  # 列号
                text = self.table.view.item(self.row, 'value')[col - 1]  # 单元格内容
                x = self.table.view.bbox(self.row, column=col - 1)[0]  # 单元格x坐标
                y = self.table.view.bbox(self.row, column=col - 1)[1]  # 单元格y坐标
                width = self.table.view.bbox(self.row, column=col - 1)[2]  # 单元格宽度
                height = self.table.view.bbox(self.row, column=col - 1)[3]  # 单元格高度

                self.entry.focus_set()
                self.entry.delete(0, END)
                self.entry.place(x=x, y=y + 48, width=width, height=30)
                self.entry.insert(0, text)

            def on_FocusOut(event):
                text = self.entry.get()
                self.table.view.set(self.row, self.column, text)
                self.entry.place_forget()
                if self.column != '#4' and self.column != '#5':
                    changeThing(self.user(), select_id, mm, text)
                else:
                    text = tuple(int(i) for i in text.split('/'))
                    changeThing(self.user(), select_id, mm, text)

            self.entry.bind("<FocusOut>", on_FocusOut)

            # 回车键触发
            def on_Return(event):
                if self.entry.winfo_viewable() == 1:
                    self.entry.place_forget()
                    text = self.entry.get()
                    self.changeval_ = text
                    self.table.view.set(self.row, self.column, text)
                    if self.column != '#4' and self.column != '#5':
                        changeThing(self.user(), select_id, mm, text)
                    else:
                        text = tuple(int(i) for i in text.split('/'))
                        changeThing(self.user(), select_id, mm, text)

            self.entry.bind("<Return>", on_Return)

    def newrow(self):
        date = Date()
        wupin = self.class_add.get()
        mincheng = self.thingname_add.get()
        now = self._predate.entry.get()
        warn = self._ddl.entry.get()
        if wupin == '' or mincheng == '':
            tk.messagebox.showwarning(message="输入信息并不完整，请重新输入")
        else:
            self.class_.append(wupin)
            self.thingname.append(mincheng)
            self.predate.append(now)
            self.ddl.append(warn)
            now_ = tuple(int(i) for i in now.split('/'))
            warn_ = tuple(int(i) for i in warn.split('/'))
            if autologin() is True:
                autologin()
            else:
                login(self.usr_name, self.usr_psw, '0')
            addThing(self.user(), mincheng, wupin, now_, warn_)
            _id = getThing(self.user())[-1]
            xuhao = _id['thingid']
            self.id.append(xuhao)
            self.table.view.insert('', len(self.class_), values=(xuhao, wupin, mincheng, now, warn))
            now_ = date.getTimestamp(*now_)
            self.gettime(mincheng, now_)
            # self.div_list.update()
            if mincheng not in self.div_list:
                self.div_list.append(wupin)
            self.division["values"] = self.div_list  # 设置下拉框可选的值
            self.division.bind("<<ComboboxSelected>>", self.get_division)

    def derow(self):
        a = self.id_dele.get()
        if a.isnumeric():
            if int(a) in self.id:
                for i in self.table.view.get_children():
                    if a == str(self.table.view.set(i, column='#1')):
                        if autologin() is True:
                            autologin()
                        else:
                            login(self.usr_name, self.usr_psw, '0')
                        deleteThing(self.user(), int(a))
                        self.id.remove(int(a))
                        n = self.table.view.set(i, column='#2')
                        x = 0
                        for j in self.class_:
                            if n == j:
                                x = x + 1
                                if x > 1:
                                    break
                        if x == 1:
                            self.div_list.remove(n)
                        # self.division["values"] = self.div_list # 设置下拉框可选的值
                        # print(self.div_list)
                        # self.division.bind("<<ComboboxSelected>>", self.get_division)
                        self.table.view.delete(i)

            else:
                tk.messagebox.showwarning(message='请检查输入！')
        else:
            tk.messagebox.showwarning(message='请检查输入！')

    def get_division(self, _):
        criteria = self.divvar.get()
        if criteria == '全部':
            criteria = ''
        self.table._filtered = True
        self.table.tablerows_filtered.clear()
        self.table.unload_table_data()
        for row in self.table.tablerows:
            for col in row.values:
                if str(criteria).lower() in str(col).lower():
                    self.table.tablerows_filtered.append(row)
                    break

        self.table._rowindex.set(0)

        self.table.load_table_data()

    def gettime(self, name, t):
        if time.time() > t:
            messagebox.showwarning('警告', f'{name}日期到了！！')
        else:
            self.app.after(1000, lambda: self.gettime(name, t))

    def run(self):
        if autologin() is True:
            self.creat_main_window()
            self.main_main()
            # for i, j in zip(self.thingname, self.predate):
            #     # print(i, j)
            #     j = tuple(int(i) for i in j.split('/'))
            #     # print(j)
            #     j = date.getTimestamp(*j)
            #     # print(j)
            #     self.gettime(i, j)
            self.app.mainloop()
        else:
            self.creat_canvas()
            self.creat_login_window()
            self.creat_main_window()
            # for i, j in zip(self.thingname, self.predate):
            #     # print(i, j)
            #     j = tuple(int(i) for i in j.split('/'))
            #     # print(j)
            #     j = date.getTimestamp(*j)
            #     # print(j)
            #     self.gettime(i, j)
            self.app.mainloop()


if __name__ == '__main__':
    App = App()
    App.run()
