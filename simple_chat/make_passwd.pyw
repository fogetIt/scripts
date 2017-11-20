# -*- coding: utf-8 -*-
# @Date:   2017-11-15 17:09:08
# @Last Modified time: 2017-11-15 17:09:12
"""
管理员统一注册、管理密码
"""
import json
import hashlib
import tkFont
import Tkinter as T


class W(object):
    tk = T.Tk()
    tk.title("make password")
    tk.geometry('400x200')
    tk.resizable(width=False, height=False)

    frame = T.Frame(tk)
    font11 = ('Arial', 11)
    font13 = tkFont.Font(family='Arial', size=13, weight=tkFont.BOLD)

    def __init__(self):
        self.init_top()
        self.init_bottom()
        self.frame.pack()

    def init_top(self):
        top_frame = T.Frame(W.frame)
        T.Label(top_frame, text="姓名", font=W.font13).grid(
            row=0, column=0, padx=10, pady=25,
        )
        T.Label(top_frame, text="密码", font=W.font13).grid(
            row=1, column=0, padx=10, pady=0,
        )
        self.sv0 = T.StringVar()
        self.sv1 = T.StringVar()
        self.sv0.set("your name")
        self.sv1.set("your password")
        self.e1 = T.Entry(top_frame, textvariable=self.sv0, font=W.font11)
        self.e2 = T.Entry(top_frame, textvariable=self.sv1, font=W.font11)
        self.e1.grid(row=0, column=1, ipadx=25, ipady=6)
        self.e2.grid(row=1, column=1, ipadx=25, ipady=6)
        self.e1.bind("<Button-1>", self.clear_sv0)
        self.e2.bind("<Button-1>", self.clear_sv1)
        top_frame.pack(side=T.TOP)

    def init_bottom(self):
        bottom_frame = T.Frame(W.frame)
        T.Button(bottom_frame,
                 text="提交",
                 font=W.font13,
                 command=self.make_password).grid(
            padx=0, pady=20,
            ipadx=10, ipady=0
        )
        bottom_frame.pack(side=T.BOTTOM)

    def clear_sv0(self, event):
        self.sv0.set("")

    def clear_sv1(self, event):
        self.sv1.set("")

    def make_password(self):
        m = hashlib.md5()
        name = self.e1.get()
        m.update(name)
        m.update(self.e2.get())
        password = m.hexdigest()
        if name and password:
            with open("password.json", "r") as reader:
                _dict = json.loads(reader.read())
                _dict.update({name: password})
                with open("password.json", "w") as writer:
                    writer.write(json.dumps(_dict))

    def run(self):
        W.tk.mainloop()


if __name__ == '__main__':
    w = W()
    w.run()
