#! /usr/bin/env python
# Importing psycopg2 from python standard library

import psycopg2

DBNAME = "newsdata.article"


def exer(cmd):
    dbm = psycopg2.connect(database=DBNAME)
    cr = dbm.cursor()
    cr.execute(cmd)
    resc = cr.fetchall()
    dbm.close()
    return resc

# Question 1


def popular_author():
    cmd = """select authors.name, count(*)
          as number from authors
          join articles
          on authors.id = articles.author
          join log
          on log.path like concat('/article/%',articles.slug)
          group by authors.name
          order by number
          desc limit 3; """
    result = exer(cmd)
    counter = 1
    print("\nBest Authors:")
    for z in result:
        print(str(counter) + '.' + z[0] + '---' + str(z[1]) + " views")
        counter += 1

# Question 2

raw_input()
def famous_article():
    cmd = """select articles.title, count(*)
          as number from articles
          join log
          on log.path like concat('/article/%',articles.slug)
          group by articles.title
          order by number
          desc limit 3;"""

    result = exer(cmd)
    counter = 1
    print("Best Articles:")
    for z in result:
        numbers = str(counter) + '. "'
        titles = z[0]
        views = '" --- ' + str(z[1]) + " views"
        print(numbers + titles + views)
        counter += 1

# Quesion 3


def error_ter():
    cmd = """select tot.day,((errors.er*100)/tot.ers)as percent
          from ( select date_trunc('day', time) "day", count(*) as er from log
          where status like '404%' group by day) as errors
          join( select date_trunc('day',time) "day", count(*) as ers from log
          group by day) as tot on tot.day =  errors.day
          where (((errors.er*100)/tot.ers)>1)
          order by percent desc;"""
    result = exer(cmd)
    print("\nMaximum errors on:")
    for z in result:
        dat = z[0].strftime('%B %d, %Y')
        err = str(z[1]) + "%" + " errors"
        print(dat + "---" + err)
# here,functions are called
famous_article()
popular_author()
error_ter()
raw_input()
