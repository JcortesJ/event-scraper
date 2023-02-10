import requests
#nos permite conectarnos a la web
import lxml.html as html
#nos permite manipular un archivo html desde python

XPATH_LINK_TO_EVENT = '//a[@class="Evento"]//img/@src'
XPATH_TITLE = '//a[@class="Evento"]//h3/text()'
XPATH_DESC = '//a[@class="Evento"]//p/text()'
XPATH_DATE = '//a[@class="Evento"]//h2/text()'

def parse_home():
    #antes que nada metemos nuestro codigo en  un try-catch
    #porque no siempre estará disponible el sitio
    try:
        #url de la pagina
        print('conectando...')
        response = requests.get('http://bienestar.bogota.unal.edu.co/Actividades-Semanales/Programacion-Bienestar.html')
        #response = requests.get('https://www.google.com')
        if response.status_code == 200:
            #response.content nos trae el archivo html
            #decode lo convierte a utf-8 para que py lo pueda usar
            home = response.content.decode('utf-8')
            #parsed convierte el string a un objeto python
            parsed = html.fromstring(home)
            #luego con xpath seleccionamos lo que nos interesa
            fechas_eventos = parsed.xpath(XPATH_DATE)
            print(fechas_eventos)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        

def run():
    parse_home()
    
if __name__ == '__main__':
    run()