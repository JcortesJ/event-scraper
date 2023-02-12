import os
#permite trabajar con fechas
import datetime
import random

def create_file(data_ev):
    today = datetime.date.today().strftime('%d-%m-%Y')
            #si no existe la carpeta 'today' crea una:
    if not os.path.isdir(today):
        os.mkdir(today)
    with open(f'{today}/{str(random.randint(0,1000))}.txt','w',encoding='utf-8'
                      ) as f:
                f.write('Titulo evento: ')
                f.write(data_ev['titulo'])
                f.write('\n')
                f.write('Creador: ')
                f.write(data_ev['creador'])
                f.write('\n')
                f.write('Descripcion: ')
                f.write(data_ev['descripcion'])
                f.write('\n')
                f.write('Fecha: ')
                f.write(data_ev['fecha'])
                f.write('\n')
                f.write('Mas informacion: ')
                f.write(data_ev['link_img'])
                f.write('\n')  
                f.write('Lugar: ')
                f.write(data_ev['lugar'])


def run():
    pass

if __name__ == '__main__':
    run()