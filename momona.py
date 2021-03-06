# -*- coding: utf-8 -*-

from mastodon import *
import time, re, sys, os, io
import threading, codecs
from time import sleep
import warnings, traceback
from xml.sax.saxutils import unescape as unesc
import JCbot as JC

"""
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,
                              encoding=sys.stdout.encoding,
                              errors='backslashreplace',
                              line_buffering=sys.stdout.line_buffering)
warnings.simplefilter("ignore", UnicodeWarning)
"""


"""ログイントークン取得済みで動かしてね（*'∀'人）"""

url_ins = open("instance.txt").read()

mastodon = Mastodon(
    client_id="cred.txt",
    access_token="auth.txt",
    api_base_url=url_ins)  # インスタンス


class Re1():  # Content整頓用(๑°⌓°๑)
    def text(text):
        return (re.sub('<p>|</p>|<a.+"tag">|<a.+"_blank">|<'
                       'a.+mention">|<span>|</span>|</a>|<span class="'
                       '[a-z-]+">', "", str(text)))


class Log():  # toot記録用クラス٩(๑❛ᴗ❛๑)۶
    def __init__(self, status):
        self.account = status["account"]
        self.mentions = status["mentions"]
        self.content = unsec(Re1.text(status["content"]))
        self.non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    def read(self):
        name = self.account["display_name"]
        acct = self.account["acct"]
        non_bmp_map = self.non_bmp_map
        print(str(name).translate(non_bmp_map) + "@" + str(
            acct).translate(self.non_bmp_map))
        print(str(self.content).translate(non_bmp_map))
        print(str(self.mentions).translate(non_bmp_map))

    def write(self):
        text = self.content
        acct = self.account["acct"]

        f = codecs.open('log\\' + 'log_' + nowing + '.txt', 'a', 'UTF-8')
        f.write(re.sub('<br />', '\\n', str(text)) + ',<acct="' + acct + '">\r\n')
        f.close()


class men_toot(StreamListener):  # 通知&ホーム監視クラス(๑・ .̫ ・๑)
    def on_notification(self, notification):
        try:
            print("===通知が来ました===", "タイプ:" + str(notification["type"]))
            if notification["type"] == "mention":
                status = notification["status"]
                account = status["account"]
                mentions = status["mentions"]
                content = unesc(Re1.text(status["content"]))
                log = threading.Thread(Log(status).read())
                log.run()
                men = threading.Thread(JC.MEN(status))
                men.run()
                bot.thank(account, 64)  # 好感度が上がります
            elif notification["type"] == "favourite":
                account = notification["account"]
                non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                print(str(account["display_name"]).translate(non_bmp_map) + "@" + str(
                    account["acct"]) + "からニコってくれたよ₍₍ ◝(●˙꒳˙●)◜ ₎₎")
                bot.thank(account, 32)  # 好感度が上がります
            pass
        except Exception as e:
            print("エラー情報\n" + traceback.format_exc())
            with open('error.log', 'a') as f:
                traceback.print_exc(file=f)
            pass
        print("   ")

    def on_update(self, status):
        try:
            print("===タイムライン【ホーム】===")
            log = threading.Thread(Log(status).read())
            log.run()
            ltl = threading.Thread(JC.TL(status))
            ltl.run()
            pass
        except Exception as e:
            print("エラー情報\n" + traceback.format_exc())
            with open('error.log', 'a') as f:
                traceback.print_exc(file=f)
            pass
        print("   ")


class res_toot(StreamListener):  # LTL監視クラス((ヾ(๑ゝω･)ﾉ♡
    def on_update(self, status):
        try:
            print("===タイムライン【ローカル】===")
            log = threading.Thread(Log(status).read())
            log.run()
            ltl = threading.Thread(JC.LTL(status))
            ltl.run()
            pass
        except Exception as e:
            print("エラー情報\n" + traceback.format_exc())
            with open('error.log', 'a') as f:
                traceback.print_exc(file=f)
            pass
        print("   ")

    def on_delete(self, status_id):
        print("===削除されました===")
        print("   ")


class count():
    timer_toot = 0
    timer_hello = 0


class ready():
    def go():
        count.timer_hello = 1

    def stop():
        count.timer_hello = 0


class Emo():
    def emo01(time=10800):  # 定期的に評価を下げまーーす♪（無慈悲）
        while 1:
            sleep(time)
            data_dir_path = u"./thank/"
            file_list = os.listdir(r'./thank/')
            for file_name in file_list:
                root, ext = os.path.splitext(file_name)
                if ext == u'.txt':
                    abs_name = data_dir_path + '/' + file_name
                    f = open(abs_name, 'r')
                    x = f.read()
                    y = int(x)
                    y += -1
                    f.close()
                    f = open(abs_name, 'w')
                    f.write(str(y))
                    f.close()

    def emo02(point):
        sleep(time)
        data_dir_path = u"./thank/"
        file_list = os.listdir(r'./thank/')
        for file_name in file_list:
            root, ext = os.path.splitext(file_name)
            if ext == u'.txt':
                abs_name = data_dir_path + '/' + file_name
                f = open(abs_name, 'r')
                x = f.read()
                y = int(x)
                y += point
                f.close()
                f = open(abs_name, 'w')
                f.write(str(y))
                f.close()
        pass

    def emo03(user, point):
        sleep(time)
        data_dir_path = u"./thank/"
        file_list = os.listdir(r'./thank/')
        abs_name = data_dir_path + '/' + user + '.txt'
        f = open(abs_name, 'r')
        x = f.read()
        y = int(x)
        y += point
        f.close()
        f = open(abs_name, 'w')
        f.write(str(y))
        f.close()
        pass


if __name__ == '__main__':
    count()
    ready.go()
    bot.timer_toot = False
    uuu = threading.Thread(bot.t_local)
    lll = threading.Thread(bot.t_user)
    fff = threading.Thread(Emo.emo01, [10800])
    uuu.start()
    lll.start()
    fff.start()
