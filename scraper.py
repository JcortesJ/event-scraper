import requests
#nos permite conectarnos a la web
import lxml.html as html
#nos permite manipular un archivo html desde python
import os
#permite trabajar con fechas
import datetime

XPATH_LINK_TO_EVENT = '//a[@class="Evento"]//img/@src'
XPATH_TITLE = '//a[@class="Evento"]//h3/text()'
XPATH_DESC = '//a[@class="Evento"]//p/text()'
XPATH_DATE = '//a[@class="Evento"]//h2/text()'
CIRCULAR_LINK = '//div[@class="news-divlist-body"]//div[@class="news-divlist-link"]//a/@href'
CIRCULAR_TEXTO
CIRCULAR_FECHA

class Evento:
    def __init__(self,tit,des,fec,e):
        self.titulo = tit
        self.descrip = des
        self.fecha = fec
        self.enlace = e

def parse_circular(link,today):
    #nos permite ir a un evento y sacar la info. 
    #es como scrapear evento por evento, si está en su propia pagina
    try:
        response = requests.get(link)
        if response.status_code ==200:
            event = response.content.decode('utf-8')
            parsed = html.fromstring(event)
            try:
                #el [0] es porque es una lista de datos. y solo
                #nos interesa el 0 que es el contenido
                title = parsed.xpath(XPATH_TITLE)[0]
                #estilizamos el titulo
                title.replace('\"','')
                summary = parsed.xpath(XPATH_DESC)[0]
                date = parsed.xpath(XPATH_DATE)[0]
                
            except IndexError:
                return
            #creamos el archivo
            with open(f'{today}/{title}.txt','w',encoding='utf-8'
                      ) as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n---------\n')
                f.write(date)
                f.write('\n')
    except ValueError as ve:
        print(ve)

def parse_bienestar(link,titles,descs,dates,today):
    #nos permite ir a un evento y sacar la info. 
    #es como scrapear evento por evento, si está en su propia pagina
 
    for i in range(len(link)):
            #creamos el archivo
            with open(f'{today}/{titles[i]}.txt','w',encoding='utf-8'
                      ) as f:
                f.write('Titulo: ')
                f.write(titles[i])
                f.write('\n\n')
                f.write('Descripcion: ')
                f.write(descs[i])
                f.write('\n---------\n')
                f.write('Fecha: ')
                f.write(dates[i])
                f.write('\n')
                f.write('link al evento: ')
                f.write(link[i])
                f.write('\n')
  

def parse_home():
    #antes que nada metemos nuestro codigo en  un try-catch
    #porque no siempre estará disponible el sitio
    try:
        #url de la pagina
        print('conectando...')
        response = requests.get('http://bienestar.bogota.unal.edu.co/Actividades-Semanales/Programacion-Bienestar.html',timeout=20)
        #response = requests.get('https://www.google.com')
        if response.status_code == 200:
            #response.content nos trae el archivo html
            #decode lo convierte a utf-8 para que py lo pueda usar
            home = response.content.decode('utf-8')
            #parsed convierte el string a un objeto python
            parsed = html.fromstring(home)
            #luego con xpath seleccionamos lo que nos interesa
            fechas_eventos = parsed.xpath(XPATH_DATE)
            links_to_events = parsed.xpath(XPATH_LINK_TO_EVENT)
            title_to_events = parsed.xpath(XPATH_TITLE)
            desc_to_events = parsed.xpath(XPATH_DESC)
            
            #print(fechas_eventos)
            #date nos trae una fecha y today la de ahorita
            #strftime nos parsea la fecha a una string
            today = datetime.date.today().strftime('%d-%m-%Y')
            #si no existe la carpeta 'today' crea una:
            if not os.path.isdir(today):
                os.mkdir(today)
            parse_bienestar(links_to_events,title_to_events,desc_to_events,fechas_eventos,today)
            #for link in links_to_events:
             #   parse_notice(link,today)
            
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
    #circular-un: scrapping
    try:
        #url de la pagina
        print('conectando...')
        response = requests.get('https://bogota.unal.edu.co/circular-un-bogota/',timeout=20)
        if response.status_code == 200:
            #response.content nos trae el archivo html
            #decode lo convierte a utf-8 para que py lo pueda usar
            home = response.content.decode('utf-8')
            #parsed convierte el string a un objeto python
            parsed = html.fromstring(home)
            #luego con xpath seleccionamos lo que nos interesa
            fechas_circular = parsed.xpath(CIRCULAR_LINK)
            print(fechas_circular)
            #date nos trae una fecha y today la de ahorita
            #strftime nos parsea la fecha a una string
            today = datetime.date.today().strftime('%d-%m-%Y')
            #si no existe la carpeta 'today' crea una:
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in fechas_circular:
                parse_circular(link,today)
            
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        

def run():
    parse_home()
    
if __name__ == '__main__':
    run()