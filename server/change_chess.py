from socket import *
import sys
import signal
import pymysql
import os
import re

class Handler():
    def __init__(self):
        self.sock = socket()
        self.sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sock.bind(("127.0.0.1",8888))
        self.sock.listen(5)
    
    #注册判定
    def do_log(self,connfd,db,msg,re):
        name = msg[1]
        pwd = msg[2]
        uname = re.findall(r"\W",name)
        cur = db.cursor()
        l = ["~","!","@","#","$","%","^","&","*","(",")"," "]
        for i in l:
            if i in uname:
                print(uname)
                message = "NO"+" "+"姓名中含有特殊字符请重新注册登录"
                connfd.send(message.encode())
                return
        else:
            sql= "select name from user where name = '%s'"%name
            cur.execute(sql)
            r = cur.fetchone()
            if r != None:
                message = "NO"+" "+"用户名已经存在请重新注册"
                connfd.send(message.encode())
                return
            sql = "insert into user(name,pwd)values('%s',AES_ENCRYPT('%s','zx'));"%(name,pwd)
            try:
                cur.execute(sql)
                db.commit()
                message = "OK"+" "+"注册成功"
                connfd.send(message.encode())

            except Exception as e:
                db.rollback()
                print("failed")
                connfd.send(b"NO")
                return

    #登录
    def do_register(self,connfd,db,msg):
        name = msg[1]
        pwd = msg[2]
        cur = db.cursor()
        sql = "select name,AES_DECRYPT(pwd,'zx') from user where name = '%s' and AES_DECRYPT(pwd,'zx') = '%s';"%(name,pwd)
        cur.execute(sql)
        r = cur.fetchone()
        if r != None:
            sql = "select name from logging where name = '%s';"%name
            cur.execute(sql)
            i = cur.fetchone()
            if i != None:
                mesg = "NO"+" "+"玩家已经登录,请不要重复登录"
                connfd.send(mesg.encode())
                return
            elif i ==None:
                sql = "insert into logging(name)values('%s');"%name
                try:
                    cur.execute(sql)
                    db.commit()
                    message ="OK"
                    connfd.send(message.encode())
                    return 1
                except Exception as e:
                    db.rollback()
                    print("failed")
                    connfd.send(b"NO")
                    return
        elif r==None:
            message = "NO"+" "+"密码错误请重新登录"
            connfd.send(message.encode())
            return

    def do_quit(self,db):
        cur=db.cursor()
        sql ="delete from logging;"
        try:
            cur.execute(sql)
            db.commit()
            sys.exit("BYe")
        except Exception as e:
            db.rollback()

    #处理客户端消息
    def do_subprocess(self,connfd,db,re):
        while True:
            data = connfd.recv(1024).decode()
            if not data:
                break
            msg = data.split(" ")
            if msg[0] == "L":
                self.do_log(connfd,db,msg,re)
            elif msg[0] =="D":
                self.do_register(connfd,db,msg)
                   
            elif msg[0] =="E":
                connfd.close()
                self.do_quit(db,)

    def main(self):

        signal.signal(signal.SIGCHLD,signal.SIG_IGN)
        db = pymysql.connect("localhost","root","123456","chess")

        while True:
            try:
                connfd,addr = self.sock.accept()
                print(addr)
            except KeyboardInterrupt:
                self.sock.close()
                sys.exit("Bye")


            pid = os.fork()
            if pid < 0:
                sys.exit("Subprocess creation failed")
            elif pid == 0:
                self.sock.close()
                self.do_subprocess(connfd,db,re)
            else:
                connfd.close()
                continue

if __name__=="__main__":
    c = Handler()
    c.main()