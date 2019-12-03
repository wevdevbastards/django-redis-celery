from __future__ import absolute_import, unicode_literals
from redis_celery.celery import app

@app.task(name="adding_taski")
def adding_taski(x, y):
	return "{} es {}".format(x, y)
	

