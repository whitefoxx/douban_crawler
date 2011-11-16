#encoding=utf-8

import sqlite3
import settings

def init_db():
    con = sqlite3.connect(settings.DB)
    cur = con.cursor()
    cur.execute('''create table if not exists group_user (db_group text, user_name text, user_page text)''')
    con.commit()
    cur.close()

def get_start_urls(which):
    urls = []
    if which == 'group_user':
        f = open("./data/groups", "r")
        for line in f:
            g = line.split()[0]
            start = 'start=0'
            if len(line.split()) > 1:
                start = line.split()[1]
            urls.append('http://www.douban.com/group/' + g.strip() + '/members?' + start)
        f.close()

    if which == 'user_movie':
        con = sqlite3.connect(settings.DB)
        cur = con.cursor()
        cur.execute("select * from user where movie_crawled=0 limit 0,10")
        for row in cur:
            if row[1].startswith("http://"):
                url = row[1].replace("www","movie")
                url = url + "collect" if url[-1] == '/' else url + "/collect"
                urls.append(url)
        print urls
        cur.close()
        con.close()
    return urls
