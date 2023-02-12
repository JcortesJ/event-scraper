
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def upload_data(data,collection_name,document_id=''):
    #Funcion sencilla que sube un diccionario a la bd
    print('Conectando a firestore...')
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    db.collection(collection_name).document(document_id).set(data)

def run():
    pass
if __name__ == '__main__':
    run()