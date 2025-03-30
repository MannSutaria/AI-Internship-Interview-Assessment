# Intelligent Queue Management System for Medical Practices

## Solution Overview

This repository contains a sophisticated implementation of an Intelligent Queue Management System designed for medical practices with multiple doctors, varied scheduling patterns, and patients arriving through different channels.

## System Architecture

The system is built around three core components:

1. **Patient Management**
   - Priority-based queueing using patient medical conditions
   - Handling of multiple appointment sources (App, Walk-in, WhatsApp)
   - UUID-based patient identification
   - Status tracking throughout the patient journey

2. **Doctor Management**
   - Support for doctor specializations
   - Flexible availability blocks
   - Priority queue implementation for patient assignment
   - Wait time estimation based on queue length and consultation time

3. **Communication System**
   - Multi-channel patient notifications
   - Wait time updates
   - Logging of all communications

## Key Features

### Intelligent Patient Assignment
- Matches patients to doctors based on medical specialization
- Considers doctor availability and current queue length
- Falls back to general practitioners when specialists aren't available

### Sophisticated Priority Calculation
- Urgency-based priority derived from medical conditions
- Adjustments based on appointment source
- Wait time considerations in priority formula

### Dynamic Doctor Scheduling
- Support for varied availability blocks
- Realistic consultation time modeling
- Capacity planning with daily patient limits

### Comprehensive Simulation
- Generates realistic patient flows
- Creates varied medical conditions with appropriate urgency levels
- Maps conditions to relevant medical specializations

## Measuring System Effectiveness

The system provides several metrics to evaluate its performance:
- Average wait times per doctor and overall
- Queue efficiency scores
- Patient notification statistics

## Communication Strategy

Patient communication is handled through:
- Source-specific notifications (App, Walk-in, WhatsApp)
- Real-time wait time updates
- Comprehensive logging for auditing

## Installation & Usage

```python
# Basic usage example
from queue_management import QueueManagementSystem, Patient

# Initialize the system with 50 doctors
qms = QueueManagementSystem(num_doctors=50)

# Create a patient
patient = Patient(
    name="John Doe",
    scheduled_time=datetime.now() + timedelta(minutes=30),
    source="App"
)

# Assign patient to most suitable doctor
assigned_doctor = qms.assign_patient(patient)
```

## Simulation

The system includes a simulation function that creates 100 patients with varied characteristics and assigns them to appropriate doctors based on the intelligent queuing algorithm.