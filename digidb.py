from bs4 import BeautifulSoup
import requests
web=requests.get('http://digidb.io/digimon-list/')
data=BeautifulSoup(web.content,'html.parser')

head=[]
for i in data.findAll('th'):
    head.append(i.text)
head.insert(1,'Picture')
# print(head)

num=[]
for i in data.findAll('b'):
    num.append(i.string[1:])
num=num[1:]
# print(num)

gambar=[]
for i in data.findAll('img'):
    gambar.append(i['src'])
gambar=gambar[2:-2]
# print(gambar)

name=[]
for i in data.findAll('a'):
    name.append(i.text)
name=name[11:-17]
# print(name)

isi=[]
for i in data.findAll('center'):
    isi.append(i.text)
isi=isi[:-1]
# print(isi)

counter=0
listDigi=[]
listKecil=[]

for i in isi:
    listKecil.append(i)
    counter+=1
    if counter%11==0:
        listDigi.append(listKecil)
        listKecil=[]

for i in range(len(listDigi)):
    listDigi[i].insert(0,name[i])
    listDigi[i].insert(0,gambar[i])
    listDigi[i].insert(0,num[i])
# print(listDigi)

digimon=[]
for i in listDigi:
    dictDigi=dict(zip(head,i))
    digimon.append(dictDigi)
# print(digimon)

import pandas as pd
dfDigi=pd.DataFrame(digimon)
dfDigi=dfDigi.set_index('#')
# print(dfDigi)

from flask import Flask, jsonify, render_template
server=Flask(__name__)

@server.route('/')
def depan():
    return render_template('depan.html')

@server.route('/table')
def table():
    return render_template('table.html',data=dfDigi.to_html())

@server.route('/json')
def json():
    return jsonify(digimon)

if __name__=='__main__':
    server.run(debug=True)

# bikin file flask utk scrapping digidb
# tampilkan /table -> html tabel data digidb, /json -> json data digidb