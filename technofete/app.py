from flask import Flask, render_template, redirect, request, url_for, flash, jsonify
from pymongo import MongoClient

app = Flask(__name__, template_folder='templates')

client = MongoClient("mongodb+srv://mohfaiz0504:9mddv4dW51npR3wb@cluster0.nmg1vs4.mongodb.net/technofete?retryWrites=true&w=majority")
db = client["techreg"]
collection = db["collection"]

eventslot = {"TreasureHeist": 2, "SyntaxSmackdown": 2, "CodeClueCrew": 3, "MechMania": 3, "OdetoCode": 1,
             "Civiathon": 5, "Circuitry": 1, "Techtales": 2, "ElectraQuiz": 2,"Posterpresentation":2,"Paperpresentation":2,"Technicalquiz":2,"CaseStudy":2}
eventcount = {"TreasureHeist": 60, "SyntaxSmackdown": 30, "CodeClueCrew": 60, "MechMania": 60, "OdetoCode": 100,
              "Civiathon": 250, "Circuitry": 80, "Techtales": 50, "ElectraQuiz": 40,"Posterpresentation":1000,"Paperpresentation":1000,"Technicalquiz":1000,"CaseStudy":1000}

event9 = ["SyntaxSmackdown", "MechMania", "OdetoCode", "TreasureHeist"]
event2 = ["Circuitry", "CodeClueCrew"]
event11 = ["Civiathon", "Techtales"]

def checkcount(eventcount):
    eventpar = {"TreasureHeist": 0, "SyntaxSmackdown": 0, "CodeClueCrew": 0, "MechMania": 0, "OdetoCode": 0,
                  "Civiathon": 0, "Circuitry": 0, "Techtales": 0, "ElectraQuiz": 0,"Posterpresentation":0,"Paperpresentation":0,"Technicalquiz":0,"CaseStudy":0}
    docs = db.collection.find()
    docs = db.collection.find()
    for doc in docs:
        for event in doc["event"]:
            eventpar[event] += 1
    for key in eventcount.keys():
        if eventcount[key] == eventpar[key]:
            return "Registration Closed"
    return "Registration Opened"

def check(Dict):
    docs = db.collection.find()
    for doc in docs:
        if doc["_id"] in Dict.keys():
            for event in doc["event"]:
                if event in event9 and Dict[doc["_id"]]["event"][0] in event9:
                    return False
                if event in event2 and Dict[doc["_id"]]["event"][0] in event2:
                    return False
                if event in event11 and Dict[doc["_id"]]["event"][0] in event11:
                    return False
            else:
                db.collection.update_one({"_id": doc["_id"]}, {"$addToSet": {"event": {"$each": Dict[doc["_id"]]["event"]}}})
                del Dict[doc["_id"]]
    return Dict

def checkandupdate(rdata):
    Dict = {}
    for d in rdata:
        result = d.split(" ")
        Dict[result[0]] = {"name": result[1], "rollno": result[0], "email": result[2], "phoneno": result[3],
                           "event": result[4:]}
    Dict = check(Dict)
    if Dict:
        for key in Dict.keys():
            db.collection.insert_one(Dict[key])
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
