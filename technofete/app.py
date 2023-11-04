from flask import Flask, render_template, redirect, request, url_for, flash, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__, template_folder='templates')

eventslot = {"TreasureHeist": 2, "SyntaxSmackdown": 2, "CodeClueCrew": 3, "MechMania": 3, "OdetoCode": 1,
             "Civiathon": 5, "Circuitry": 1, "Techtales": 2, "ElectraQuiz": 2}
eventcount = {"TreasureHeist": 60, "SyntaxSmackdown": 30, "CodeClueCrew": 60, "MechMania": 60, "OdetoCode": 100,
              "Civiathon": 250, "Circuitry": 80, "Techtales": 50, "ElectraQuiz": 40}

event9 = ["SyntaxSmackdown", "MechMania", "OdetoCode", "TreasureHeist"]
event2 = ["Circuitry", "CodeClueCrew"]
event11 = ["Civiathon", "Techtales"]

cred = credentials.Certificate("sdkconnect.json")
app_options = {'projectId': 'technofete-e0554'}
dbapp = firebase_admin.initialize_app(cred, options=app_options)
db = firestore.client(dbapp)

def checkcount(eventcount):
    eventpar = {"TreasureHeist": 0, "SyntaxSmackdown": 0, "CodeClueCrew": 0, "MechMania": 0, "OdetoCode": 0,
                  "Civiathon": 0, "Circuitry": 0, "Techtales": 0, "ElectraQuiz": 0}
    docs = db.collection("registration").stream()
    for doc in docs:
        dic = doc.to_dict()
        for i in dic["event"]:
            eventpar[i]+=1
    for key in eventcount.keys():
        if eventcount[key]==eventpar[key]:
            return "Registration Closed"
    return "Registration Opened"


def check(Dict):
    docs = db.collection("registration").stream()
    for doc in docs:
        if doc.id in Dict.keys():
            dic = doc.to_dict()
            for e in dic["event"]:
                print(e, Dict[doc.id]["event"])
                if e in event9 and Dict[doc.id]["event"][0] in event9:
                    # print(e)
                    return False
                if e in event2 and Dict[doc.id]["event"][0] in event2:
                    return False
                if e in event11 and Dict[doc.id]["event"][0] in event11:
                    return False
            else:
                db.collection("registration").document(doc.id).update(
                    {"event": firestore.ArrayUnion(Dict[doc.id]["event"])})
                del (Dict[doc.id])

    return Dict


def checkandupdate(rdata):
    # docs = db.collection("registration").stream()
    Dict = {}
    for d in rdata:
        result = d.split(" ")
        Dict[result[0]] = {"name": result[1], "rollno": result[0], "email": result[2], "phoneno": result[3],
                           "event": result[4:]}
    Dict = check(Dict)
    if Dict:
        for key in Dict.keys():
            db.collection("registration").document(key).set(Dict[key])
        return "Successful"
    else:
        return "Event clash"


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/association')
def association():
    return render_template('association.html')

@app.route('/ignite')
def ignite():
    return render_template('ignite.html')


@app.route('/signup')
def signup():
    aid = request.args.get('id', default='', type=str)
    status=checkcount(eventcount)
    print(status)
    if status=="Registration Closed":
        return render_template("association.html",data=status)
    else:
        return render_template('signup.html', data=[aid, eventslot[aid]])


@app.route('/data', methods=['POST'])
def data():
    jsdata = request.json
    # print(jsdata)
    # checkandupdate(jsdata)
    response_data = {"message": checkandupdate(jsdata)}
    return jsonify(response_data)
    # return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
