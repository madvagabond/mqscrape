#!/usr/bin/python
import lxml.html
from time import sleep
from selenium import webdriver
from pymongo import MongoClient
def visiting(url):
        browser = webdriver.PhantomJS()
        browser.get(url)

        sleep(5)
        body = browser.page_source
        browser.close()
        return body

def linkextractor(htm):
        doc = lxml.html.document_fromstring(htm)
        atag = doc.cssselect('a')
        ltag = doc.cssselect('link')
        links = []
        for x in atag:
                try:
                        url = x.attrib['href']
                        links.append(url)
                except:
                    pass
        return links
def scriptrd(bod):
        doc = lxml.html.document_fromstring(bod)
        script = doc.cssselect('script')
        for y in script:
                try:
                        src = y.attrib['src']
                        writer('jssrc', src)
                except:
                        pass
                try:
                        fulljs = lxml.html.tostring(y)
                        writer('javascript', fulljs)
                except:
                        pass
def buttons(bod):
        doc = lxml.html.document_fromstring(bod)
        buttons = doc.cssselect('button')
        for btn in buttons:
                btn = lxml.html.tostring(btn)
                writer('buttons', btn)
def inputs(html):
        sr = lxml.html.document_fromstring(html)
        usrinput = sr.cssselect('input')
        for x in usrinput:
                ui = lxml.html.tostring(x)
                writer('input', ui)
def meta(html):
        sr = lxml.html.document_fromstring(html)
        meta = sr.cssselect('meta')
        for x in meta:
                metat = lxml.html.tostring(x)
                writer('meta', metat)
def forms(html):
        src = lxml.html.document_fromstring(html)
        forms = src.cssselect('form')
        for z in forms:
                form = lxml.html.tostring(z)
                writer('forms', form)
def writer(name, content):
	client = MongoClient()
	db = client.rmqp
	store = db.store
	store.insert({name : content})
