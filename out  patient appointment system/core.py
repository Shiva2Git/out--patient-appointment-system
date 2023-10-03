from flask import Flask, jsonify, request, render_template
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Sample doctor data

doctors = [
    {"id": 1, "name": "Dr.AMMU", "max_patients": 15 ,"specialist":"Immunologists"},
    {"id": 2, "name": "Dr.BANU",  "max_patients": 13 ,"specialist":"Anesthesiologists"},
    {"id": 3, "name": "Dr.KARTHIK", "max_patients":10 ,"specialist":"Critical Care Medicine Specialists"},
    {"id": 4, "name": "Dr.KHUSHI", "max_patients":10 ,"specialist":"Cardiologists"},
    {"id": 5, "name": "Dr.SHIVA", "max_patients":12 ,"specialist":"Colon and Rectal Surgeons"},
    {"id": 6, "name": "Dr.ANU", "max_patients":14 ,"specialist":"Dermatologists"},
    {"id": 7, "name": "Dr.TNNU", "max_patients":17 ,"specialist":"Family Physicians"},
    {"id": 8, "name": "Dr.KUMARI", "max_patients":12 ,"specialist":"Gastroenterologists"}
]


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    max_patients = db.Column(db.Integer, nullable=False)
    specialist = db.Column(db.String(80), nullable=False)
    

with app.app_context():
    db.create_all()
    for doctor in doctors:
        doctor = Doctor(name=doctor['name'],max_patients=doctor['max_patients'], specialist=doctor['specialist'])
        db.session.add(doctor)
    
    # db.session.commit()
    # db.session.add(doctor2)
    #  db.session.commit()
    # db.session.query(Doctor).delete()
    #  # db.session.query(Appointment).delete()
    # db.session.commit()

@app.route('/')
def home():
    return render_template("home.html")



# Endpoint to list all doctors
@app.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    output=[]
    for doctor in doctors:
        output.append({
            'doctor_id':doctor.id,
            'name': doctor.name,
            'specialist': doctor.specialist,
        })
    return jsonify(output)

@app.route('/<string:doctor_name>', methods=['POST','GET'])
def doctor_name(doctor_name):
    doctors=Doctor.query.all()
    for doctor in doctors:
        if doctor_name==doctor.name or doctor.name.upper()==doctor_name.upper() or doctor.name.lower()==doctor_name.lower() or doctor.name.title()==doctor_name.title():
           doctor={
            'id': doctor.id,
            'name': doctor.name,
            'specialist': doctor.specialist,
            'max_patients': doctor.max_patients
           }
           return jsonify(doctor)
    return jsonify({'error': 'Doctor not found'}), 404

   

# Endpoint to get details of a specific doctor
@app.route('/<int:doctor_id>', methods=['POST','GET'])
def doctor_id(doctor_id):
    doctors=Doctor.query.all()
    doctor = next((doctor for doctor in doctors if doctor.id == doctor_id), None)
    if doctor is None:
        return jsonify({'error': 'Doctor not found'}), 404
    doctor={
            'id': doctor.id,
            'name': doctor.name,
            'specialist': doctor.specialist,
            'max_patients': doctor.max_patients
           }
    return jsonify(doctor)


# Endpoint to book an appointment
@app.route('/appointments', methods=['POST','GET'])
def appointments():
    doctors=Doctor.query.all()
    doctor_id=int(request.form['doctor_id'])
    doctor_name=str(request.form['doctor_name'])
    appointment_date=str(request.form['appointment_date'])
    appointment_time=request.form['appointment_time']
   
    appointment_date=appointment_date.replace('-','/')
    day=datetime.strptime(appointment_date,"%Y/%m/%d")
    day_name=day.strftime('%A')
    time=''
    for i in appointment_time:
        if i==':':
            break
        else:
            time+=i
    

    # Check if the doctor exists
    for doctor in doctors:
        if (doctor.id==doctor_id):
            if doctor.name==doctor_name or doctor.name.upper()==doctor_name.upper() or doctor.name.lower()==doctor_name.lower() or doctor.name.title()==doctor_name.title():
                if day_name != "Sunday":
                   if int(time)>=18 and int(time)<=20:
                        count=doctor.max_patients+1
                        db.session.query(Doctor).filter_by(id=doctor_id).update({"max_patients":count})
                        db.session.commit()
                        return jsonify({"doctor_id":doctor_id,"doctor_name":doctor_name,"appointment_date":appointment_date,'appointment_time': appointment_time,'message': 'Appointment booked successfully'})
                   else:
                        return jsonify({'message': 'oops! Please choose eveng time only '}),
                else:
                    return jsonify({'error':'Today is holiday'})
    return jsonify({'error': 'Doctor not found'}), 404



@app.route('/book-appointment', methods=['POST','GET'])
def show_booking_page():
    return render_template("booking.html")

if __name__ == '__main__':
    app.run(debug=True)
