
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_data(data,collection_name,document_id=''):
    #Funcion sencilla que sube un diccionario a la bd
    print('Conectando a firestore...')
   
    #revisamos si el id existe, si si le sumamos 1. Si no no worries:
    verify = db.collection(collection_name).document(document_id).get()
    if verify.exists:
        document_id+=1
    db.collection(collection_name).document(document_id).set(data)
    return 0
