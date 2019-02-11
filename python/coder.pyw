# -*- coding: utf-8 -*-
# @Date:   2017-11-15 11:48:15
# @Last Modified time: 2017-11-15 13:31:44
import hashlib
from functools import partial
import Tkinter as T
import tkMessageBox


int8 = partial(int, base=8)
int10 = partial(int, base=10)
int16 = partial(int, base=16)


def error_tip(msg, title="error"):
    tkMessageBox.showerror(title, msg)


class BytesUtils(object):

    def str_decorator(func):
        def wrapper(self, _str):
            _list = _str.split(" ")
            result = []
            for i in _list:
                value = func(self, i)
                if value:
                    result.append(value)
                else:
                    break
            return " ".join(result)
        wrapper.__doc__ = func.__doc__
        return wrapper

    @str_decorator
    def chr(self, _str):
        """chr(int) → string"""
        if _str.isdigit() and int10(_str) in range(0, 256):
            return chr(int10(_str))
        error_tip("只接受0~255的数字")

    @str_decorator
    def unichr(self, _str):
        """unichr(int) → unicode"""
        if _str.isdigit() and int10(_str) in range(0, 1114111):
            return unichr(int10(_str))
        error_tip("只接受0~1114111的数字")

    def unicode(self, _str):
        """ord(str) → int"""
        _list = [str(ord(i)) for i in _str]
        return " ".join(_list)

    @str_decorator
    def int2hex(self, _str):
        """hex(int) → string(16 decimal system)"""
        if _str.isdigit():
            return hex(int10(_str))
        error_tip("只接受数字（以空格分割）")

    @str_decorator
    def int2oct(self, _str):
        """oct(int) → string(8 decimal system)"""
        if _str.isdigit():
            return oct(int10(_str))
        error_tip("只接受数字（以空格分割）")

    @str_decorator
    def hex2int(self, _str):
        """int(string, base=16) → int"""
        try:
            return str(int16(_str))
        except:
            error_tip("只接受16进制字符串（以空格分割）")

    @str_decorator
    def oct2int(self, _str):
        """int(string, base=8) → int"""
        try:
            return str(int8(_str))
        except:
            error_tip("只接受8进制字符串（以空格分割）")


class StrUtils(object):

    def upper(self, _str):
        """'aB*c d'.upper() → 'AB*C D'"""
        return _str.upper()

    def lower(self, _str):
        """'aB*c d'.lower() → 'ab*c d'"""
        return _str.lower()

    def swapcase(self, _str):
        """'aB*c d'.swapcase() → 'Ab*C D'"""
        return _str.swapcase()

    def title(self, _str):
        """'aB*c d'.title() → 'Ab*c d'"""
        return _str.title()

    def capitalize(self, _str):
        """'aB*c d'.capitalize() → 'Ab*c d'"""
        return _str.capitalize()

    def reverse(self, _str):
        """'aB*c d' → 'd c*Ba'"""
        # return _str[::-1]
        _list = list(_str)
        _list.reverse()
        return "".join(_list)


class HashlibUtils(object):

    def __exec(self, func_name, _str):
        exec("obj = hashlib.%s()" % func_name)
        obj = eval("obj")
        obj.update(_str)
        return obj.hexdigest()

    def md5(self, _str):
        """string → string(16 decimal system)"""
        return self.__exec("md5", _str)

    def sha1(self, _str):
        """string → string(16 decimal system)"""
        return self.__exec("sha1", _str)

    def sha224(self, _str):
        """string → string(16 decimal system)"""
        return self.__exec("sha224", _str)

    def sha256(self, _str):
        """string → string(16 decimal system)"""
        return self.__exec("sha256", _str)

    def sha384(self, _str):
        """string → string(16 decimal system)"""
        return self.__exec("sha384", _str)

    def sha512(self, _str):
        """string → string(16 decimal system)"""
        return self.__exec("sha512", _str)


class EncodingUtils(object):

    def ascii(self, _str):
        pass


class W(BytesUtils, StrUtils, HashlibUtils, EncodingUtils):
    tk = T.Tk()
    tk.title("coder")
    tk.geometry('800x610')
    tk.resizable(width=False, height=False)

    frame = T.Frame(tk)
    left_frame = T.Frame(frame)
    right_frame = T.Frame(frame)

    def __init__(self):
        self.sv = T.StringVar()
        self.init_left_frame()
        self.init_right_frame()
        self.frame.pack()
        W.tk.mainloop()

    @staticmethod
    def create_font(n):
        return ('Arial', n)

    F = create_font

    def create_list(self, frame, cls, height=None):
        font = W.F(16)
        # TODO  create Label
        text = cls.__name__.replace("Utils", "").lower()
        T.Label(master=frame, text=text, font=font, fg="#2F4F4F").grid(pady=2)
        # TODO  create Listbox
        exclude = ["str_decorator", "_HashlibUtils__exec"]
        items = [attr for attr in dir(cls) if not attr.startswith("__") and attr not in exclude]
        height = height if height else len(items)
        list_box = T.Listbox(
            master=frame,
            width=10, height=height, font=font, borderwidth=3,
            background="#2F4F4F", foreground="#ffffff",
            selectbackground="red", selectforeground="#ffffff"
        )
        list_box.configure(justify=T.CENTER)
        for func_name in items:
            list_box.insert(T.END, func_name)
        list_box.grid()
        list_box.bind("<<ListboxSelect>>", self.trans_coding)

    def init_left_frame(self):
        self.create_list(W.left_frame, BytesUtils)
        self.create_list(W.left_frame, StrUtils)
        self.create_list(W.left_frame, HashlibUtils)
        W.left_frame.pack(side=T.LEFT)

    def create_text(self, row=1):
        text = T.Text(
            master=W.right_frame, width=70, height=13, font=W.F(13)
        )
        text.grid(row=row, column=0, columnspan=2, padx=5)
        return text

    def init_result_text(self):
        T.Label(
            master=W.right_frame, text="result", font=W.F(18)
        ).grid(row=0, column=0, sticky=T.W, pady=5)
        self.format_label = T.Label(
            master=W.right_frame, textvariable=self.sv, font=W.F(15), foreground="red"
        )
        self.format_label.grid(row=0, column=1, sticky=T.W, pady=5)
        self.result_text = self.create_text(row=1)

    def init_input_text(self):
        T.Label(
            master=W.right_frame, text="input", font=W.F(18)
        ).grid(row=2, column=0, columnspan=2, sticky=T.W, pady=5)
        self.input_text = self.create_text(row=3)

    def init_right_frame(self):
        self.init_result_text()
        self.init_input_text()
        W.right_frame.pack(side=T.RIGHT)

    def get_code(self):
        return self.input_text.get("1.0", T.END).strip()

    def trans_coding(self, event):
        wi = event.widget
        if wi.curselection():
            index = int(wi.curselection()[0])
            value = wi.get(index).strip()
            _str = self.get_code() if self.get_code() != "\\" else "\\\\"
            if not value:
                error_tip("未选中转码格式")
            elif not _str:
                error_tip("输入框内容不能为空")
            else:
                exec("doc = self.%s.__doc__" % value)
                self.sv.set(eval("doc"))
                format_string = "result = self.%s('%s')" % (
                    value, _str
                )
                exec(format_string)
                res = eval("result")
                if res:
                    self.result_text.delete('1.0', T.END)
                    self.result_text.insert("1.0", res)


if __name__ == '__main__':
    W()
