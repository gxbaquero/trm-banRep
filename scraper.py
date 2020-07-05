import requests
import datetime
import json

from bs4 import BeautifulSoup
from os import remove

URL ='https://www.banrep.gov.co/indicators/widgets/TRM/ES/show'
archivo='trm.json'

def run():
	try:
		response = requests.get(URL)
		if(response.status_code==200):
			soup=BeautifulSoup(response.text,'html.parser')
			TRM=soup.find("div",attrs={"class":"down-big"}).get_text()
			fecha=soup.find("td",attrs={"scope":"row"}).get_text();
			salida='{"day":"'+fecha.strip()+'","trm":"'+TRM.strip()+'"}'
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
		jsonFile=f.read()		
	finally:
		f.close()

	#print(jsonFile)
	if(jsonFile!=''):
		existe=jsonFile.find(fbuscar)
		if(existe==-1):
			flag=1
			remove(archivo)
		
	with open(archivo, mode='a', encoding='utf-8') as f:
		trm=run();
		if(flag==0):
			trm="["+trm+"]"
		if(flag==1):
			trm=jsonFile[:-1]+","+trm+"]"
	#	print(trm)
		f.write(trm)
		f.close()


if __name__ == '__main__':	
	chkfile()
	#run()