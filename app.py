from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)
app.debug = True
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monitoring.sqlite3'
db = SQLAlchemy(app)

class Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    temperature = db.Column(db.Float, default=0.0)
    humidity = db.Column(db.Float, default=0.0)
    instrument_id = db.Column(db.Integer, db.ForeignKey('instrument.id'), nullable=False)
    instrument = db.relationship('Instrument', backref=db.backref('datas', lazy=False))

    def serialize(self):
        return {
            'id': self.id,
            'created_date': self.created_date,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'instrument_id': self.instrument_id,
            'instrument': self.instrument.serialize()
        }

@app.route("/")
def index():
    results = []
    instruments = Instrument.query.all()
    for ins in instruments:
        data = Data.query.filter_by(instrument_id=ins.id).order_by(desc(Data.created_date)).first()
        if data is None:
            data = Data()
            data.instrument_id = ins.id
            data.instrument = ins
        print(data.instrument.name)
        results.append(data)
    return render_template("index.html", results = results)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/instrument", methods=['GET'])
def getInstrument():
    instruments = Instrument.query.all()
    return jsonify( [i.serialize() for i in instruments] )

@app.route("/instrument", methods=['POST'])
def addInstrument():
    req = request.get_json()
    ins = Instrument(
        name = req['name']
    )
    db.session.add(ins)
    db.session.commit()
    return getInstrument()


@app.route("/data", methods=['GET'])
def getData():
    datas = Data.query.all()
    return jsonify( [d.serialize() for d in datas] )

@app.route("/data", methods=['POST'])
def addData():
    req = request.get_json()
    data = Data(
        temperature= req['temperature'],
        humidity= req['humidity'],
        instrument_id= req['instrument_id']
    )
    db.session.add(data)
    db.session.commit()
    return getData()

if __name__ == "__main__":
    app.run()