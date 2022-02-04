from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://itxuqhkooddblw:9f893945714a623478a73d2847e6344c2d6d2fc3cebdcd94bf7b90d438a50475@ec2-3-216-113-109.compute-1.amazonaws.com:5432/d7tug9k5e7akgn"

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Month(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    days_in_month = db.Column(db.Integer, nullable=False)
    days_in_previous_month = db.Column(db.Integer, nullable=False)
    start_day = db.Column(db.Integer, nullable=False)

    def __init__(self, name, year, days_in_month, days_in_previous_month, start_day):
        self.name = name
        self.year = year
        self.days_in_month = days_in_month
        self.days_in_previous_month = days_in_previous_month
        self.start_day = start_day

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)

    def __init__(self, day, mont, year, text):
        self.day = day
        self.month = month
        self.year = year
        self.text = text


class MonthSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "year", "days_in_month", "days_in_previous_month", "start_day")

month_schema = MonthSchema()
multiple_month_schema = MonthSchema(many=True)

class ReminderSchema(ma.Schema):
    class Meta:
        fields = "id", "day", "month", "year", "text"

reminder_schema = ReminderSchema()
multiple_reminder_schema = ReminderSchema(many=True)

@app.route("/reminder/get", methods=["GET"])
def get_all_reminders():
    records = db.session.query(Reminder).all()
    return jsonify(multiple_reminder_schema.dump(records))

@app.route("/reminder/get/<month>/<year>", methods=["GET"])
def get_all_reminders():
    records = db.session.query(Reminder).filter(Reminder.month == month).filter(Reminder.year == year).all()
    return jsonify(multiple_reminder_schema.dump(records))

@app.route("/reminder/update/<id>", methods=["PUT"])
def update_reminder(id):
    record = db.session.query(Reminder).filter(Reminder.id == id).first()

    put_data = request.get_json()
    text = put_data.get("text")

    if text is not None:
        record.text = text
        db.session.commit()

    
    return jsonify("Reminder Updated")

@app.route("/reminder/delete/<id>", methods=["DELETE"])
def delete_reminder(id):
    record = db.session.query(Reminder).filter(Reminder.id == id).first()

    db.session.delete(record)
    db.session.commit()

    return jsonify("Reminder deleted")


if __name__ == "__main__":
    app.run(debug=True)