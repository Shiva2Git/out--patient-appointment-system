# out--patient-appointment-system
# Doctor Appointment System

This is a simple web-based Doctor Appointment System built using Flask and SQLAlchemy.

## Overview

The Doctor Appointment System is designed to help patients book appointments with specific doctors. It provides a list of doctors, their specialties, and allows patients to schedule appointments based on doctor availability.

## Software Used

- **Flask**: A lightweight and easy-to-use web framework in Python.
- **SQLAlchemy**: A Python SQL toolkit and Object-Relational Mapping (ORM) library.

## Requirements

- Python 3.6 or higher
- Flask
- SQLAlchemy
  
How it Works

The system utilizes Flask, a web framework, to handle HTTP requests and responses.
It uses SQLAlchemy to manage the SQLite database for storing doctor information and appointments.
The application defines endpoints for viewing doctors, booking appointments, and displaying appointment details.
The Doctor class represents a doctor and their attributes in the database.
Users can interact with the system through the provided web interface, viewing doctors and scheduling appointments.

How to RUN :
python core.py

API Endpoints

/doctors: Get a list of all doctors.
/<string:doctor_name>: Get details of a specific doctor by name.
/<int:doctor_id>: Get details of a specific doctor by ID.
/appointments: Book an appointment with a doctor.


Contributing
Contributions to this project are welcome! If you have any suggestions or would like to report issues, please open an issue or create a pull request.









