import heapq
import numpy as np
import logging
from datetime import datetime, timedelta
import random
import uuid

class CommunicationManager:
    """
    Handles patient communication across multiple channels
    """
    @staticmethod
    def send_notification(patient, message):
        """
        Send notifications via multiple channels
        """
        print(f"Notification to {patient.name} ({patient.source}): {message}")
        logging.info(f"Notification sent to {patient.patient_id}: {message}")

class Patient:
    def __init__(self,
                 name=None,
                 contact_number=None,
                 scheduled_time=None,
                 source=None,
                 medical_condition=None):
        """
        Enhanced Patient class with priority-based queuing
        """
        self.patient_id = str(uuid.uuid4())
        self.name = name or f"Patient_{random.randint(1000, 9999)}"
        self.contact_number = contact_number
        self.scheduled_time = scheduled_time or datetime.now()
        self.arrival_time = datetime.now()
        self.source = source or random.choice(['App', 'Walk-in', 'WhatsApp'])
        self.medical_condition = medical_condition or self._generate_medical_condition()

        self.urgency = self._calculate_urgency()
        self.priority = self.calculate_priority()

        self.status = "Scheduled"
        self.wait_time = None

    def _generate_medical_condition(self):
        """
        Generate medical conditions with inherent urgency
        """
        conditions = [
            ("Minor Checkup", 1),
            ("Routine Prescription", 2),
            ("Chronic Disease Follow-up", 3),
            ("Acute Pain", 4),
            ("Severe Symptoms", 5)
        ]
        return random.choice(conditions)

    def _calculate_urgency(self):
        """
        Calculate urgency based on medical condition
        """
        return self._generate_medical_condition()[1]

    def calculate_priority(self):
        """
        Sophisticated priority calculation
        """
       
        delay = max(0, (self.arrival_time - self.scheduled_time).total_seconds() // 60)

        # Source-based priority adjustment
        source_priority = {
            'Walk-in': -1,
            'App': 1,
            'WhatsApp': 0
        }

        return (self.urgency * 10) - delay + source_priority.get(self.source, 0)

    def __lt__(self, other):
        """
        Allow comparison for priority queue
        """
        return self.priority > other.priority

class Doctor:
    def __init__(self, doctor_id, specialization, availability_blocks=None):
        """
        Advanced Doctor class with priority queue
        """
        self.doctor_id = doctor_id
        self.specialization = specialization

        # Priority queue for patients
        self.queue = []

        # Availability management
        self.availability_blocks = availability_blocks or self._generate_availability_blocks()

        # Consultation parameters
        self.avg_consultation_time = random.randint(10, 25)  # minutes
        self.daily_capacity = random.randint(30, 50)

    def _generate_availability_blocks(self):
        """
        Generate flexible availability blocks
        """
        return [
            (datetime.now().replace(hour=9, minute=0), datetime.now().replace(hour=12, minute=0)),
            (datetime.now().replace(hour=15, minute=0), datetime.now().replace(hour=18, minute=0))
        ]

    def add_patient(self, patient):
        """
        Add patient to priority queue
        """
        heapq.heappush(self.queue, patient)

    def next_patient(self):
        """
        Get next patient based on priority
        """
        return heapq.heappop(self.queue) if self.queue else None

    def estimate_wait_time(self):
        """
        Estimate wait time based on queue
        """
        return len(self.queue) * self.avg_consultation_time

class QueueManagementSystem:
    def __init__(self, num_doctors=50):
        """
        Comprehensive Queue Management System
        """
        self.doctors = {}
        self.communication_manager = CommunicationManager()

        specializations = [
            'General', 'Pediatrics', 'Cardiology',
            'Neurology', 'Orthopedics'
        ]

        for i in range(num_doctors):
            doctor_id = f"DOC-{i+1}"
            specialization = random.choice(specializations)
            self.add_doctor(doctor_id, specialization)

    def add_doctor(self, doctor_id, specialization, availability_blocks=None):
        """
        Add a doctor to the system
        """
        self.doctors[doctor_id] = Doctor(doctor_id, specialization, availability_blocks)

    def assign_patient(self, patient):
        """
        Intelligent patient assignment
        """
        suitable_doctors = [
            doc for doc in self.doctors.values()
            if self._is_doctor_suitable(doc, patient)
        ]

        if not suitable_doctors:
            suitable_doctors = [
                doc for doc in self.doctors.values()
                if doc.specialization == 'General'
            ]

        best_doctor = min(suitable_doctors, key=lambda d: d.estimate_wait_time())

        best_doctor.add_patient(patient)

        wait_time = best_doctor.estimate_wait_time()
        self.communication_manager.send_notification(
            patient,
            f"Assigned to Dr. {best_doctor.doctor_id}. Estimated wait: {wait_time} minutes"
        )

        return best_doctor

    def _is_doctor_suitable(self, doctor, patient):
        """
        Check if doctor is suitable for patient
        """
        return (
            doctor.specialization == 'General' or
            doctor.specialization == self._map_condition_to_specialization(patient.medical_condition)
        )

    def _map_condition_to_specialization(self, medical_condition):
        """
        Map medical conditions to specializations
        """
        mapping = {
            "Chronic Disease Follow-up": "Cardiology",
            "Acute Pain": "Orthopedics",
            "Severe Symptoms": "Neurology"
        }
        return mapping.get(medical_condition[0], "General")

def main():
    # Initialize Queue Management System
    qms = QueueManagementSystem()

    for _ in range(100):
        patient = Patient(
            name=f"Patient_{_}",
            scheduled_time=datetime.now() + timedelta(minutes=random.randint(0, 60)),
            source=random.choice(['App', 'Walk-in', 'WhatsApp'])
        )

        assigned_doctor = qms.assign_patient(patient)

        print(f"Patient {patient.name} (Priority: {patient.priority}) "
              f"assigned to Dr. {assigned_doctor.doctor_id}")

if __name__ == "__main__":
    main()