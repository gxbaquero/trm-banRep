import requests
import datetime
import csv

from bs4 import BeautifulSoup
from os import remove
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors


URL ='https://www.banrep.gov.co/indicators/widgets/TRM/ES/show'
archivo='trm.json'
dataStats='trm.csv'

def run(tipo):
	try:
		response = requests.get(URL)
		if(response.status_code==200):
			soup=BeautifulSoup(response.text,'html.parser')
			TRM=soup.find("div",attrs={"class":"down-big"}).get_text()
			fecha=soup.find("td",attrs={"scope":"row"}).get_text();
			if(tipo=='json'):
				salida='{"day":"'+fecha.strip()+'","trm":"'+TRM.strip()+'"}'
			if(tipo=='csv'):
				salida=fecha.strip()+';'+TRM.strip()+'\n'
			#print(TRM)	print((fecha.strip()))
			return salida
				
		else:
			print('Error: ', response.status_code)
	except e:
		print('Error:', e)

def chkdate():
	today = datetime.date.today()
	tt = today.timetuple()
	dayweek=tt.tm_wday
	if(dayweek==6):
		today=today- datetime.timedelta(days=1)
	return today

def chkfile():
	flag=0 #0=vacio 1=no exite fecha 2=fecha existe
	fecha=chkdate()
	fbuscar='{:%d/%m/%Y}'.format(fecha)
	try:
		f=open(archivo, mode='r', encoding='utf-8')
		g=open(dataStats, mode='r', encoding='utf-8')
		jsonFile=f.read()		
		csvFile=g.read()
	finally:
		f.close()
		g.close()

	#print(jsonFile)
	if(jsonFile!=''):
		existe=jsonFile.find(fbuscar)
		if(existe==-1):
			flag=1
			remove(archivo)
		else:
			flag=2
	
	if(flag!=2):
		with open(archivo, mode='a', encoding='utf-8') as f:
			trm=run('json');
			if(flag==0):
				trm="["+trm+"]"
			if(flag==1):
				trm=jsonFile[:-1]+","+trm+"]"
		#	print(trm)
			f.write(trm)
			f.close()
	flag=0
	if(csvFile!=''):
		existe=csvFile.find(fbuscar)
		if(existe==-1):
			flag=1
			remove(dataStats)
		else:
			flag=2
	
	if(flag!=2):
		with open(dataStats, mode='a', encoding='utf-8') as f:
			trm=run('csv');
			if(flag==0):
				trm="fecha;trm\n"+trm
			if(flag==1):
				trm=csvFile+trm
		#	print(trm)
			f.write(trm)
			f.close()
	salidaPDF();

def salidaPDF():
	w, h = letter
	x_offset = 60
	y_offset = 60
	padding = 15
	max_rows_per_page = 45
	data=[]
	elems=[]

	pdf=SimpleDocTemplate(
		'trm.pdf',
		pagesize=letter
	)
	with open('trm.csv') as csvfile:
		reader = csv.reader(csvfile,delimiter=';')
		for row in reader:
			data.append(row)
	
	table=Table(data)
	style=TableStyle()
	table.setStyle([
		('BACKGROUND',(0,0),(1,0),colors.cadetblue),
		('TEXTCOLOR',(0,0),(1,0),colors.white),
		('ALIGN',(0,0),(-1,0),'CENTER'),
		('FONTSIZE',(0,0),(-1,0),14),
		('BOX',(0,0),(-1,-1),1,colors.gray),
		('GRID',(0,0),(-1,-1),1,colors.gray)
	])

	elems.append(table)

	pdf.build(elems)


if __name__ == '__main__':	
	chkfile()
	#run()