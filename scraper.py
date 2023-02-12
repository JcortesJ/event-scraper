import random
import requests
#nos permite conectarnos a la web
import lxml.html as html
#nos permite manipular un archivo html desde python
from file_creator import create_file





XPATH_LINK_TO_EVENT = '//a[@class="Evento"]//img/@src'
XPATH_TITLE = '//a[@class="Evento"]//h3/text()'
XPATH_DESC = '//a[@class="Evento"]//p/text()'
XPATH_DATE = '//a[@class="Evento"]//h2/text()'
CIRCULAR_LINK = '//div[@class="news-divlist-body"]//div[@class="news-divlist-link"]//a/@href'
CIRCULAR_TEXTO = '//div[@class="news-text-wrap"]//span/text()'
CIRCULAR_FECHA = '//div[@class="news-divlist-startdate"]/text()'
CIRCULAR_TITULO = '//h3[@itemprop="headline"]/text()'
CIRCULAR_LUGAR = '//div[@class="news-divlist-venue"]/text()'
CIRCULAR_INFO = '//div[@class="mediaelement mediaelement-image"]//img/@src'
CIRCULAR_AUTOR = '//div[@class="news-divlist-host"]/text()'


def parse_circular(link):  
    #nos permite ir a un evento y sacar la info. 
    #es como scrapear evento por evento, si está en su propia pagina
    try:
        print('conectando con el evento de circular...')
        response = requests.get('https://bogota.unal.edu.co/'+link,verify=False)
        if response.status_code ==200:
            print('evento conectado')
            event = response.content.decode('utf-8')
            parsed = html.fromstring(event)
            try:
                #une la lista (join)
                lugar = ''.join(parsed.xpath(CIRCULAR_LUGAR))
                title = ''.join(parsed.xpath(CIRCULAR_TITULO))
                #estilizamos el titulo
                title.replace('\"','')
                title.replace('\n','')
                title.replace('\t','')
                summary = ''.join(parsed.xpath(CIRCULAR_TEXTO))
                if summary == '': summary= 'Descripcion no disponible'
                date = ''.join(parsed.xpath(CIRCULAR_FECHA))
                date.replace('\"','')
                date.replace('\n','')
                date.replace('\t','')
                autor = ''.join(parsed.xpath(CIRCULAR_AUTOR))
                autor.replace('\"','')
                autor.replace('\n','')
                autor.replace('\t','')
                m_info = 'https://bogota.unal.edu.co/'+''.join(parsed.xpath(CIRCULAR_INFO))
                m_info.replace('\"','')
                m_info.replace('\n','')
                m_info.replace('\t','')
                print('datos tomados, escribiendo en archivo..')
                
            except IndexError:
                return
            #creamos el archivo
            data_up = {'titulo':title,'lugar':lugar,'creador':autor,'descripcion':summary,'link_img':m_info,'fecha':date}
            create_file(data_up)
    except ValueError as ve:
        print(ve)

def parse_bienestar(link,titles,descs,dates,creador,lugar):
    for i in range(len(link)):
            #creamos el diccionario
            data_up = {'titulo':titles[i],'lugar':lugar,'creador':creador,'descripcion':descs[i],'link_img':link[i],'fecha':dates[i]}
            create_file(data_ev=data_up)

def connect_bienestar():
    #antes que nada metemos nuestro codigo en  un try-catch
    #porque no siempre estará disponible el sitio
    try:
        #url de la pagina
        print('conectando con bienestar...')
        response = requests.get('http://bienestar.bogota.unal.edu.co/Actividades-Semanales/Programacion-Bienestar.html',timeout=20)
     
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
            parse_bienestar(links_to_events,title_to_events,desc_to_events,fechas_eventos,'Eventos Bienestar','No especificado')
            
            
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def connect_circular():
     #circular-un: scrapping
    try:
        #url de la pagina
        print('conectando con circular...')
        response = requests.get('https://bogota.unal.edu.co/circular-un-bogota/',timeout=10,verify=False)
        if response.status_code == 200:
            print('conectado con circular.. buscando eventos')
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_circular = parsed.xpath(CIRCULAR_LINK)
          
            for link in links_circular:
                print('entrando al link: ' + link)
                parse_circular(link)
            
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        

def run():
    connect_bienestar()
    connect_circular()
    
if __name__ == '__main__':
    run()