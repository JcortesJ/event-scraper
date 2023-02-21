
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_data(data,collection_name,document_id=''):
    #Funcion sencilla que sube un diccionario a la bd
    #revisamos si el dato existe en la base de datos con una consulta:
    dato_previo = db.collection(collection_name).where('titulo','==',data['titulo']).get()
    if len(dato_previo) >0:
        #no se usa exists por que en general regresa una lista y no un solo elemento
        print('dato repetido')
    else:
        db.collection(collection_name).document(document_id).set(data)
        print('Dato nuevo agregado')
    return 0
    #queda pendiente una forma en la cual con un mismo nombre se actualice la info
"""    
    if len(eventos_disponibles) == 0:
          db.collection(collection_name).document(document_id).set(data)
          return 0
    else:
        
        for e in eventos_disponibles:
            
            
            print(f'eventos hasta el momento: {len(eventos_disponibles)}')
            titulo = e.to_dict()['titulo']
            if e.id == document_id and titulo != data['titulo']:
                document_id= str(random.radint(0,10000))
                db.collection(collection_name).document(document_id).set(data)
            #    return 0
            elif  titulo == data['titulo']:
            #actualizamos los datos
                db.collection(collection_name).document(e.id).delete()
                db.collection(collection_name).document(document_id).set(data)
             #   return 0
            else:
                db.collection(collection_name).document(document_id).set(data)
              #  return 0
"""        
    