import psycopg2

DBNAME = "news"

def get_most_popular_articles():
	"""return the top three popular articles"""
	db = psycopg2.connect(database=DBNAME)
	c = db.cursor()
	c.execute("select t2.title, count(*) as total from log as t1,articles as t2 where t1.path=concat('/article/',t2.slug) group by t2.title order by total desc limit 3 ;")
	data = c.fetchall()
	db.close()
	return data

def get_most_popular_authors():
	"""return the top three popular author"""
	db = psycopg2.connect(database=DBNAME)
	c = db.cursor()
	c.execute(" select t1.name,count(*) as total from authors as t1, articles as t2,log as t3 where t3.path=concat('/article/',t2.slug) and t1.id=t2.author group by t1.name order by total desc limit 3;")
	data = c.fetchall()
	db.close()

	return data

def get_most_errors():
	"""return the error page more than 1% one day"""
	db = psycopg2.connect(database=DBNAME)
	c = db.cursor()
	c.execute("create IF NOT EXISTS view totalviews as select time::date as date,count(*) as total from log group by date;")
	c.execute("create IF NOT EXISTS view errorviews as select time::date as date,count(*) as total from log where status <> '200 OK' group by date;")
	c.execute("select t1.date, round(t1.total::numeric/t2.total::numeric,3) as err from errorviews as t1,totalviews as t2 where t1.date=t2.date and round(t1.total::numeric/t2.total::numeric,3)>0.01 order by err desc;")
	data = c.fetchall()
	db.close()
	return data
