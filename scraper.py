import random
import requests
#nos permite conectarnos a la web
import lxml.html as html
#nos permite manipular un archivo html desde python
from file_creator import create_file
from conexion import upload_data





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

DEPORTES_FECHA = '//a[@class="Evento"]//h2/text()'
DEPORTES_LINK= '//a[@class="Evento"]//img/@src'
DEPORTES_TITULO = '//a[@class="Evento"]//h3/text()'
#no olvides el text() que hace que no nos marque error al traer un elemento html
DEPORTES_INFO = '//a[@class="Evento"]//p/text()'

HORA_VITA = '//div[@class="Marco"]//div[@class="Hora"]/text()'
DESC_VITA = '//div[@class="Marco"]//div[@class="Txt"]//p/text()'
TITU_VITA = '//div[@class="Marco"]//div[@class="ACT"]//h3/text()'
LUGAR_VITA = '//div[@class="Marco"]//div[@class="ACT"]//h4/text()'
LINK_VITA = '//div[@class="Banner Arriba"]//img/@src'


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
                print('-----------')
                
            except IndexError:
                return
            #creamos el archivo
            data_up = {'titulo':title,'lugar':lugar,'creador':autor,'descripcion':summary,'link_img':m_info,'fecha':date}
           # create_file(data_up)
            upload_data(data=data_up,collection_name='Evento',document_id=str(random.randint(0,10000)))
    except ValueError as ve:
        print(ve)

def parse_bienestar(link,titles,descs,dates,creador,lugar):
    #esta funcion recibe una seria de listas: links, titulos, infos y fechas.
    #se organizan en un for, donde se crea un diccionario que se sube a la base de datos
    #cada diccionario simboliza un evento
    
    for i in range(len(link)):
            #creamos el diccionario
           # print('evento bienestar: ' +str(i))
            if type(lugar) !=  list:
                data_up = {'titulo':titles[i],'lugar':lugar,'creador':creador,'descripcion':descs[i],'link_img':link[i],'fecha':dates[i]}
            else:
                data_up = {'titulo':titles[i],'lugar':lugar[i],'creador':creador,'descripcion':descs[i],'link_img':link[i],'fecha':dates[i]+' Actividad Semanal'}
            #create_file(data_ev=data_up)
            upload_data(data=data_up,collection_name='Evento',document_id=str(random.randint(0,10000)))

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

def connect_deportes():
    #antes que nada metemos nuestro codigo en  un try-catch
    #porque no siempre estará disponible el sitio
    try:
        #url de la pagina
        print('conectando con deportes...')
        response = requests.get('http://bienestar.bogota.unal.edu.co/Cartelera-Deportes/Cartelera_Deportes.html',timeout=20)
     
        if response.status_code == 200:
            #response.content nos trae el archivo html
            #decode lo convierte a utf-8 para que py lo pueda usar
            home = response.content.decode('utf-8')
            #parsed convierte el string a un objeto python
            parsed = html.fromstring(home)
            #luego con xpath seleccionamos lo que nos interesa
            fechas_eventos = parsed.xpath(DEPORTES_FECHA)
            links_to_events = parsed.xpath(DEPORTES_LINK)
            title_to_events = parsed.xpath(DEPORTES_TITULO)
            desc_to_events = parsed.xpath(DEPORTES_INFO) 
            parse_bienestar(links_to_events,title_to_events,desc_to_events,fechas_eventos,'Eventos Deportes','No especificado')
            
            
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        
def connect_vitalizate():
    #antes que nada metemos nuestro codigo en  un try-catch
    #porque no siempre estará disponible el sitio
    try:
        #url de la pagina
        print('conectando con vitalizate...')
        response = requests.get('http://bienestar.bogota.unal.edu.co/Cartelera-Deportes/Cartelera_Deportes.html',timeout=20)
     
        if response.status_code == 200:
            #response.content nos trae el archivo html
            #decode lo convierte a utf-8 para que py lo pueda usar
            home = response.content.decode('utf-8')
            #parsed convierte el string a un objeto python
            parsed = html.fromstring(home)
            #luego con xpath seleccionamos lo que nos interesa
            fechas_eventos = parsed.xpath(HORA_VITA)
            links_to_events = []
            for i in range(len(fechas_eventos)):
                links_to_events.append(parsed.xpath(LINK_VITA)[0])
            title_to_events = parsed.xpath(TITU_VITA)
            desc_to_events = parsed.xpath(DESC_VITA) 
            lugar_evento = parsed.xpath(LUGAR_VITA)
            parse_bienestar(links_to_events,title_to_events,desc_to_events,fechas_eventos,'Programa Vitalizate',lugar=lugar_evento)
            
            
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
                parse_circular(link)
            
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        
        
def run():
    connect_bienestar()
    connect_circular()
    connect_deportes()
    connect_vitalizate()
    
if __name__ == '__main__':
    run()