# -*- coding: utf-8 -*-
#coding=utf-8
import MySQLdb
import bs4 as bs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DB(object):
    def addslashes(self,s):
        try:
            d = {'"': '\\"', "'": "\\'", "\0": "\\\0", "\\": "\\\\"}
            return ''.join(d.get(c, c) for c in s)
        except:
            return s
    def __init__(self,**parm):

        self.con=MySQLdb.connect(**parm)
        self.cur=self.con.cursor(MySQLdb.cursors.DictCursor)
        self.cur.execute('set names utf8mb4')
    def getData(self,table,where):
        sql='select * from '+table+where


        self.cur.execute(sql)
        return self.cur.fetchall()
    def inserData(self,data,tabel,keywords):

        for dic in data:
            keys = list()
            values = list()
            for a in dic.keys():
                keys.append('`' + a + '`')
                v=dic[a]
                v=self.addslashes(v)
                # v = "\"" + v + "\"" if type(v) is type("a") else str(v)
                values.append('\'' + v + '\'')
            sql='select * from '+tabel+' where '+keywords+' = '+'\''+dic[keywords]+'\''

            ret=self.cur.execute(sql)
            if ret:
                update=list()
                for key in keys:
                    index =keys.index(key)
                    update.append(key+' = '+values[index])

                action='update '+tabel +' set '+','.join(update)+' where '+keywords+' = '+ '\''+dic[keywords]+'\''
            else:
                action="insert into "+tabel + " (" +','.join(keys)+"  ) values ("+','.join(values)+' )'
                # action="insert into "+tabel +" (picId,image,title )  values ('abc','abc','abc')"

            try:
                print action
                ret=self.cur.execute(action)
                if ret :
                    self.con.commit()
                    print '插入成功  '
                else:
                    self.con.commit()

                    print '插入失败 ！ '
            except Exception as e:

                print '插入失败 ！ ' + str(e)




