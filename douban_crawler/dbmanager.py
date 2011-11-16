# encoding=utf-8

import sqlite3
from douban_crawler.items import GroupUserItem, UserMovieItem
import settings

class DBManager(object):
    count = 0
    cur_user_page = ''
    urls = []

    def __init__(self):
        self.open_db()

    def open_db(self):
        if settings.DB_CONN == None:
            settings.DB_CONN = sqlite3.connect(settings.DB)

    def create_tables(self):
        self.open_db()
        settings.DB_CONN.execute('''create table if not exists group_user (\
            db_group text, user_name text, user_page text)''')
        settings.DB_CONN.execute('''create table if not exists user_movie (\
            user text, subject integer, rating integer, date text,\
            tags text, comment text)''')
        settings.DB_CONN.commit()

    def close_db(self):
        try:
            if settings.DB_CONN != None:
                settings.DB_CONN.commit()
                settings.DB_CONN.close()
                settings.DB_CONN = None
        except Exception:
            settings.DB_CONN = None

    def store_item(self, item):
        if isinstance(item, GroupUserItem):
            try:
                print item['homepage'][0]
                settings.DB_CONN.execute("insert into group_user values(?,?,?)",\
                        (item['group'][0],item['name'][0],
                        item['homepage'][0]))
                self.count += 1
                if self.count % 100 == 0:
                    settings.DB_CONN.commit()
            except Exception,e:
                print e
                pass
        if isinstance(item, UserMovieItem):
            try:
                print item['user'],item['subject']
                cur = settings.DB_CONN.cursor()
                cur.execute("select * from user_movie where user=? and \
                        subject=?",(item['user'][0],int(item['subject'][0])))
                if cur.rowcount == -1:
                    settings.DB_CONN.execute("insert into user_movie values(?,?,?,?,?,?)"\
                        ,(item['user'][0],int(item['subject'][0]),int(item['rating'][0]),\
                        item['date'][0],item['tags'][0],item['comment'][0]))
                    self.count += 1
                if self.count % 100 == 0:
                    settings.DB_CONN.commit()
            except Exception,e:
                print "Error in store UserMovieItem:", e
        return item

    
    def get_start_urls(self, which):
        urls = []
        if which == 'group_user':
            f = open("./data/groups", "r")
            for line in f:
                g = line.split()[0]
                start = 'start=0'
                if len(line.split()) > 1:
                    start = line.split()[1]
                urls.append('http://www.douban.com/group/' + g.strip() \
                        + '/members?' + start)
            f.close()
    
        if which == 'user_movie':
            url = self.more_url(which)
            urls.append(url)
        return urls

    def more_url(self, which):
        if(which == 'user_movie'):
            if self.cur_user_page != '':
                settings.DB_CONN.execute("update user set movie_crawled=1 where \
                        user_page=?", (self.cur_user_page,))
            settings.DB_CONN.commit()
            if len(self.urls) == 0:
                cur = settings.DB_CONN.cursor()
                cur.execute("select * from user where movie_crawled=0 limit 0,1000")
                for row in cur:
                    if row[0].startswith("http://"):
                        url = row[0].replace("www","movie")
                        url = url + "collect" if url[-1] == '/' else url + "/collect"
                        self.urls.append(url)
            if len(self.urls) > 0:
                url = self.urls.pop()
                self.cur_user_page = url.replace("movie","www").replace("collect","")
                return url
            else:
                self.cur_user_page = ''
                return None

    def gen_user(self):
        settings.DB_CONN.execute('create table if not exists user (\
	        user_page text, movie_crawled boolean)')
        settings.DB_CONN.commit()
        cur = settings.DB_CONN.cursor()
        cur.execute("select * from group_user")
        s = set()
        for row in cur:
            page = row[2]
            if page[-1] != '/':
                page += '/'
            if page in s:
                continue
            s.add(page)
            settings.DB_CONN.execute("insert into user values(?,0)", (page,))
        settings.DB_CONN.commit()
        cur.close()
        settings.DB_CONN.close()

    def clear_table(self,table):
        settings.DB_CONN.execute("delete from ?", (table,))
