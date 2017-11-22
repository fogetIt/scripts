# -*- coding: utf-8 -*-
# @Date:   2017-11-01 16:38:45
# @Last Modified time: 2017-11-01 17:06:05
import sys
import platform
from subprocess import Popen
if platform.version().lower().find("ubuntu") != -1:
    Popen([
        "/bin/bash", "-c",
        """
        python -c 'import wx; exit()'
        if [ $? != 0 ]; then
            apt-get install python-wxtools
            python %s
        fi
        """ % sys.argv[0]
    ]).wait()
else:
    print("error: please install wxPython in your system")
    exit(1)
import os
import re
import json
import socket
from threading import Thread
import wx
from wx.lib.pubsub import pub
import wx.lib.scrolledpanel as scrolled


os.environ["UBUNTU_MENUPROXY"] = "0"
HOST = "10.167.140.19"
PORT = 8888
BUFFER_SIZE = 4096
RED_COLOR = wx.Colour(255, 0, 0)
BLUE_COLOR = wx.Colour(30, 144, 255)
GREEN_COLOR = wx.Colour(0, 139, 69)


class MixedUnicode(unicode):
    """
    如果运行报错，加上
    reload(sys)
    sys.setdefaultencoding('utf-8')
    """
    chinese_code_range = u"[\u4e00-\u9fa5]"

    def __len__(self):
        chinese_list = re.findall(self.chinese_code_range, self)
        return super(MixedUnicode, self).__len__() + len(chinese_list)

    def lcut(self, end):
        if end <= 0:
            return None, None
        num = 0
        result = []
        for i in self:
            if 0 <= num < end:
                if re.match(self.chinese_code_range, i):
                    num += 2
                else:
                    num += 1
                result.append(i)
        left = "".join(result)
        right = self.replace(left, "", 1)
        return left, right

    @staticmethod
    def wrap(text, n, text_list=None):
        text_list = text_list if text_list else []
        left, right = MixedUnicode(text).lcut(n)
        if left:
            text_list.append(left)
            text_list.append("\n")
            if right:
                text_list.append("\t")
                MixedUnicode(right).wrap(right, n, text_list=text_list)
        return "".join(text_list)


class Client(object):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.client.setblocking(1)

    @staticmethod
    def create_message(title, ext_data=None, send_to=""):
        message_dict = {"title": title}
        if ext_data:
            message_dict.update(ext_data)
        if send_to:
            message_dict.update({"send_to": send_to})
        return json.dumps(message_dict)

    def login(self, name, password):
        self.client.connect((HOST, PORT))
        self.client.send(
            self.create_message("login", ext_data={
                                "name": name, "password": password})
        )

    def logout(self):
        self.client.send(self.create_message("logout"))
        self.client.close()

    def send_to_one(self, text, send_to):
        self.client.send(self.create_message(
            "send_to_one", ext_data={"text": text}, send_to=send_to
        ))

    def send_to_all(self, text):
        self.client.send(self.create_message(
            "send_to_all", ext_data={"text": text}
        ))


class MainFrame(wx.Frame):
    n = 48
    user_list = []
    find_sender = -1
    message_store = {}
    my_name = my_password = checked_user = None

    def __init__(self):
        pos = (400, 50)
        size = (700, 600)
        super(MainFrame, self).__init__(
            parent=None,
            id=-1,
            name="main",
            title="simple chat client",
            pos=pos,
            size=size,
            style=wx.DEFAULT_FRAME_STYLE
        )
        self.SetMaxSize(size)
        self.SetMinSize(size)
        self.panel = wx.Panel(parent=self, id=1)

        self.default_font = wx.Font(
            pointSize=12,
            family=wx.SWISS,
            style=wx.NORMAL,
            weight=wx.BOLD
        )  # Chinese/English = 2

        # TODO  left sizer init
        """
        use BoxSizer to avoid hard-coded widget's pos and size
        """
        self.public_box = wx.ListBox(
            parent=self.panel,
            id=11,
            choices=[],
            name='public',
            size=(0, 28),
            style=0
        )
        self.public_box.SetFont(self.default_font)
        self.public_box.SetForegroundColour(RED_COLOR)
        self.public_box.SetBackgroundColour(BLUE_COLOR)
        self.public_box.Append(u"群聊♡")

        self.user_list_box = wx.ListBox(
            parent=self.panel,
            id=12,
            choices=[],
            name='user_list',
            style=wx.LB_SINGLE
        )
        self.user_list_box.SetFont(self.default_font)
        self.user_list_box.SetForegroundColour(RED_COLOR)
        self.user_list_box.SetBackgroundColour(GREEN_COLOR)

        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.left_sizer.Add(
            self.public_box,
            proportion=0,
            flag=wx.EXPAND | wx.ALL,
            border=0
        )
        self.left_sizer.Add(
            self.user_list_box,
            proportion=10,
            flag=wx.EXPAND | wx.ALL,
            border=0
        )

        # TODO  right top sizer init
        self.user_text = wx.StaticText(
            parent=self.panel,
            id=13,
            label="",
            size=(0, 25),
            style=wx.ALIGN_CENTER
        )
        self.user_text.SetFont(self.default_font)
        self.clear_button = wx.Button(
            parent=self.panel,
            id=14,
            label=u"清空"
        )
        self.clear_button.Enable(False)
        self.right_top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.right_top_sizer.Add(
            self.user_text,
            proportion=4,
            flag=wx.EXPAND | wx.LEFT,
            border=150
        )
        self.right_top_sizer.Add(
            self.clear_button,
            proportion=6,
            flag=wx.EXPAND | wx.LEFT | wx.RIGHT,
            border=100
        )
        # TODO  message sizer init
        self.message_sizer = wx.BoxSizer(wx.VERTICAL)
        self.message_panel = scrolled.ScrolledPanel(
            parent=self.panel,
            id=15,
            style=wx.SIMPLE_BORDER
        )
        self.message_panel.SetSizer(self.message_sizer)
        # TODO  right sizer init
        self.input_field = wx.TextCtrl(
            parent=self.panel,
            id=16,
            value="",
            size=(100, 50),
            style=wx.TE_MULTILINE | wx.TE_RICH2
        )
        self.input_field.SetFont(
            wx.Font(
                pointSize=12,
                family=wx.MODERN,
                style=wx.NORMAL,
                weight=wx.NORMAL
            )
        )

        self.send_button = wx.Button(
            parent=self.panel,
            id=17,
            size=(0, 40),
            label=u"发送"
        )
        self.send_button.SetFont(
            wx.Font(
                pointSize=13,
                family=wx.SWISS,
                style=wx.NORMAL,
                weight=wx.BOLD
            )
        )

        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.Add(
            self.right_top_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL,
            border=5
        )
        self.right_sizer.Add(
            self.message_panel,
            proportion=8,
            flag=wx.EXPAND | wx.ALL,
            border=5
        )
        self.right_sizer.Add(
            self.input_field,
            proportion=2,
            flag=wx.EXPAND | wx.ALL,
            border=5
        )
        self.right_sizer.Add(
            self.send_button,
            proportion=0,
            flag=wx.EXPAND | wx.LEFT | wx.RIGHT,
            border=200
        )

        # TODO  main sizer init
        self.main_sizer = wx.BoxSizer()
        self.main_sizer.Add(
            self.left_sizer,
            proportion=2,
            flag=wx.EXPAND | wx.ALL,
            border=15
        )
        self.main_sizer.Add(
            self.right_sizer,
            proportion=8,
            flag=wx.EXPAND | wx.RIGHT | wx.BOTTOM | wx.TOP,
            border=15
        )
        self.panel.SetSizer(self.main_sizer)

        pub.subscribe(self.pub_find_sender, "find_sender")
        pub.subscribe(self.pub_user_list, "user_list")

        self.Show(True)  # TODO == MainFrame().Show()

    def create_label(self, startswith, wrapped_text):
        label = "%s:\n\t%s" % (startswith, wrapped_text)
        return label

    def update_message_store(self, name, wrapped_text, message_sender=None):
        if not message_sender:
            startswith = name
        else:
            startswith = message_sender
        label = self.create_label(startswith, wrapped_text)
        if not self.message_store.get(name):
            self.message_store.update({name: []})
        self.message_store.get(name).append(label)

    def create_static_text_by_label(self, label, name):
        _label = label
        if label.startswith("self:"):
            _label = label.replace("self:\n\t", "\t\t\t\t").replace("\n\t", "\n\t\t\t\t")
            text = MixedUnicode(_label.strip())
            if len(text) <= n:
                _label = "\t" * ((self.n - len(text)) / 4) + _label
        static_text = wx.StaticText(
            parent=self.message_panel,
            label=_label,
            style=wx.ALIGN_LEFT
        )
        static_text.SetFont(self.default_font)
        if name.startswith(u"群聊:") and not label.startswith("self:"):
            static_text.SetForegroundColour(BLUE_COLOR)
        elif not name.startswith(u"群聊:") and not label.startswith("self:"):
            static_text.SetForegroundColour(GREEN_COLOR)
        return static_text

    def show_message(self, name):
        # TODO  销毁 message_panel 的所有子对象
        self.message_panel.DestroyChildren()
        """
        self.message_panel.RemoveChild()
        # 销毁后的子对象，不能再通过 ADD() 添加到 message_sizer
        """
        self.message_sizer.Clear(deleteWindows=False)
        self.message_panel.SetupScrolling()  # TODO  This line must be here.

        label_list = self.message_store.get(name)
        label_list = label_list if label_list else []
        for label in label_list:
            static_text = self.create_static_text_by_label(label, name)
            self.message_sizer.Add(
                static_text,
                proportion=0,
                flag=wx.EXPAND | wx.ALL
            )

    def show_tip(self, message):
        self.tip = wx.MessageDialog(
            parent=None,
            message="\n%s" % message,
            pos=(60, 25),
            style=wx.ICON_EXCLAMATION | wx.OK_DEFAULT
        )
        self.tip.ShowModal()

    def pub_find_sender(self, sender):
        self.find_sender = self.user_list_box.FindString(sender + u"♡")

    def pub_user_list(self):
        self.user_list = [user.strip(u"♡").strip(u"♥")
                          for user in self.user_list_box.GetItems()]


class MainWindow(Thread, Client, MainFrame):
    """
    Read Eval Print Loop
    Can't use super(REPL, self).__init__(*args, **kwargs) to init two super classes.
    """
    app = wx.App()

    def __init__(self):
        self.show_input_tip()
        if not self.my_name or not self.my_password:
            exit(2)

        Thread.__init__(self)
        Client.__init__(self)
        MainFrame.__init__(self)

        self.Bind(wx.EVT_CLOSE, self.close_window_event)
        self.send_button.Bind(wx.EVT_BUTTON, self.send_message_event)
        self.clear_button.Bind(wx.EVT_BUTTON, self.clear_message_event)
        self.public_box.Bind(wx.EVT_LEFT_UP, self.choice_public_event)
        self.user_list_box.Bind(wx.EVT_LEFT_UP, self.choice_user_event)

        self.login(self.my_name, self.my_password)

    def show_input_tip(self):
        self.name_input = wx.TextEntryDialog(
            parent=None,
            message="Enter Your Name",
            caption=""
        )
        if self.name_input.ShowModal() == wx.ID_OK:
            self.my_name = self.name_input.GetValue().strip()
            self.password_input = wx.TextEntryDialog(
                parent=None,
                message="Enter Your Password"
            )
            if self.password_input.ShowModal() == wx.ID_OK:
                self.my_password = self.password_input.GetValue().strip()

    def close_window_event(self, e=None):
        self.logout()
        MainWindow.app.Destroy()  # TODO  notice
        wx.Exit()                 # TODO  better than exit(0)

    def choice_user_event(self, e):
        if self.user_list_box.GetItems():
            self.checked_user = self.user_list_box.GetStringSelection().strip(u"♡").strip(u"♥")
            n = self.user_list_box.GetSelection()
            if n != -1:
                self.user_list_box.Delete(n)
                self.user_list_box.Insert(self.checked_user + u"♡", n)
                self.user_text.SetLabel(self.checked_user)
                self.user_text.SetForegroundColour(GREEN_COLOR)
                self.clear_button.Enable(True)
                self.show_message(self.checked_user)

    def choice_public_event(self, e):
        self.checked_user = u"群聊"
        self.public_box.Clear()
        self.public_box.Set([u"群聊♡"])
        self.user_text.SetLabel(self.checked_user)
        self.user_text.SetForegroundColour(BLUE_COLOR)
        self.clear_button.Enable(True)
        self.show_message(self.checked_user)

    def clear_message_event(self, e):
        if self.checked_user:
            self.message_store.pop(self.checked_user, None)
            self.show_message(self.checked_user)

    def send_message_event(self, e):
        text = self.input_field.GetValue().strip()
        wrapped_text = MixedUnicode.wrap(text, self.n)
        if not self.checked_user:
            self.show_tip(u"未选择用户")
        elif not text:
            self.show_tip(u"发送信息不能为空")
        else:
            if self.checked_user == u"群聊":
                if self.user_list_box.GetItems():
                    self.send_to_all(wrapped_text)
                    self.update_message_store(
                        self.checked_user,
                        wrapped_text,
                        message_sender="self"
                    )
                    self.show_message(self.checked_user)
                else:
                    self.show_tip("can't send message to null")
            else:
                self.send_to_one(wrapped_text, self.checked_user)
                self.update_message_store(
                    self.checked_user,
                    wrapped_text,
                    message_sender="self"
                )
                self.show_message(self.checked_user)

    def run(self):
        MainWindow.app.MainLoop()


class REPL(Thread, Client):

    def __init__(self, window):
        Thread.__init__(self)
        Client.__init__(self)
        self.window = window

    def public_handle(self, text, sender):
        my_name = self.window.my_name
        if my_name != sender:
            wx.CallAfter(
                self.window.update_message_store,
                u"群聊", text, message_sender=sender
            )
        checked_user = self.window.checked_user
        if checked_user == u"群聊":
            wx.CallAfter(
                self.window.show_message,
                checked_user
            )
        else:
            wx.CallAfter(
                self.window.public_box.Set,
                [u"群聊♥"]
            )

    def private_handle(self, text, sender):
        wx.CallAfter(
            self.window.update_message_store,
            sender, text
        )
        checked_user = self.window.checked_user
        if checked_user == sender:
            wx.CallAfter(
                self.window.show_message,
                checked_user
            )
        else:
            pub.sendMessage("find_sender", sender=sender)
            n = self.window.find_sender
            if n != -1:
                wx.CallAfter(
                    self.window.user_list_box.Delete,
                    n
                )
                wx.CallAfter(
                    self.window.user_list_box.Insert,
                    sender + u"♥", n
                )

    def error_handle(self, message_dict):
        wx.CallAfter(
            self.window.show_tip,
            message_dict.get("error_text")
        )
        wx.CallAfter(
            self.window.close_window_event
        )

    def user_list_handle(self, message_dict):
        user_list = message_dict.get("user_list")
        my_name = self.window.my_name
        pub.sendMessage("user_list")
        current_user_list = self.window.user_list
        for user in user_list:
            if user != my_name and user not in current_user_list:
                wx.CallAfter(
                    self.window.user_list_box.Append,
                    user + u"♡"
                )
        for i, user in enumerate(current_user_list):
            if user not in user_list:
                wx.CallAfter(
                    self.window.user_list_box.Delete,
                    i
                )
                wx.CallAfter(
                    self.window.message_store.pop,
                    user, None
                )

    def run(self):
        while True:
            try:
                message = self.client.recv(BUFFER_SIZE)
            except Exception as e:
                print(e)
                break
            if message:
                try:
                    message_dict = json.loads(message)
                    text = message_dict.get("text")
                    title = message_dict.get("title")
                    sender = message_dict.get("sender")

                    if title == "public":
                        self.public_handle(text, sender)
                    elif title == "private":
                        self.private_handle(text, sender)
                    elif title == "error":
                        self.error_handle(message_dict)
                    elif title == "user_list":
                        self.user_list_handle(message_dict)
                except Exception as e:
                    print("data in wrong format:%s\n%s" % (e, message))


if __name__ == '__main__':
    t1 = MainWindow()
    t2 = REPL(t1)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
