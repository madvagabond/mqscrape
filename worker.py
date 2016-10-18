#!/usr/bin/python
import pika
import scrapelib
import sys
reload(sys)
sys.setdefaultencoding("utf8")
def publisher(va):
    conn = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = conn.channel()
    channel.basic_publish(exchange="project", routing_key='jobs', body=va)


def callback(ch, method, properties, body):
    print body    
    try:
        s = scrapelib.visiting(body)
        links = scrapelib.linkextractor(s)
    
        for x in links:
                print x
                scrapelib.writer("links", x)
                publisher(x)
	scrapelib.scriptrd(s)
	scrapelib.buttons(s)
	scrapelib.inputs(s)
	scrapelib.meta(s)
	scrapelib.forms(s)

    except:
        pass


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare(exchange="project")
channel.queue_declare(queue="jobs", durable=True)
channel.queue_bind(exchange="project", queue="jobs")
channel.basic_consume(callback, queue="jobs")
channel.start_consuming()
