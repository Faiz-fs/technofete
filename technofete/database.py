import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./sdkconnect.json")
app_options = {'projectId': 'technofete-e0554'}
#default_app = firebase_admin.initialize_app(cred)
app = firebase_admin.initialize_app(cred, options=app_options)
print(app.name)

db=firestore.client(app)
#data={"name":"aswath","rollno":"727621bcs027","email":"727621bcs027@mcet.in","phoneno":"8987773881","event":["CodeClueCrew","TreasureHeist"],"teamname":"hello"}
#db.collection("registration").document("727621bcs009").set(data)
#db.collection("registration").document("727621bcs009").update({"event": firestore.ArrayUnion(["Code"])})
docs = db.collection("registration").stream()
for doc in docs:
    dic=doc.to_dict()
    for i in dic.keys():
        if i=='event':
            print(dic[i])