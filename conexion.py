
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_data(data,collection_name,document_id=''):
    #Funcion sencilla que sube un diccionario a la bd
    print('Conectando a firestore...')
    repetido = False
    eventos_disponibles = db.collection(collection_name).get()
        #revisamos si el id existe, si si generamos uno nuevo:
        #adicionalmente revisamos que no haya un evento con el mismo titulo. Si lo hay, se actualiza
    for e in eventos_disponibles:
        if e.id == document_id:
            document_id= str(random.radInt(0,10000))
            db.collection(collection_name).document(document_id).set(data)
            return 0
        if e.to_dict()['titulo'] == data['titulo']:
            #actualizamos los datos
            db.collection(collection_name).document(e.id).update(data)
            return 0
