#  ChronoLogic — Neuro-Symbolic AI Productivity & Task Scheduling System

<p align="center">
  <img src="docs/banner.png" width="100%"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/PyQt6-Desktop_UI-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Django-REST_API-darkgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/MongoDB-NoSQL-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Gemini_API-AI_Powered-orange?style=for-the-badge"/>
</p>

---

# 🚀Overview

ChronoLogic is an AI-powered productivity management system that combines:

*  Generative AI
*  Mathematical Optimization
*  Neuro-Symbolic Computing
*  Desktop UI Engineering
*  Behavioral Analytics

to intelligently prioritize tasks and combat procrastination.

Unlike traditional productivity tools that only store tasks, ChronoLogic actively analyzes user behavior, predicts procrastination tendencies, estimates cognitive workload, and dynamically optimizes task execution order in real time.

The system was designed to solve two major human productivity problems:

* The Planning Fallacy
* Chronic Procrastination

---

# Why ChronoLogic?

Traditional productivity systems treat all tasks equally.

ChronoLogic understands that:

* Writing a quick email
* Solving a complex algorithm
* Preparing for an exam
* Debugging a production system

all require completely different levels of mental energy and behavioral resistance.

Instead of relying entirely on user judgment, ChronoLogic uses AI to evaluate tasks and mathematically optimize schedules based on cognitive difficulty, urgency, and procrastination risk.

The system behaves less like a static to-do list and more like an intelligent productivity strategist.

---

# Core Innovations

✅ Hybrid Neuro-Symbolic Scheduling
✅ AI-Based Cognitive Load Estimation
✅ Dynamic Priority Decay Engine
✅ Constraint-Aware Optimization
✅ Behavioral Penalty Modeling
✅ Real-Time Task Reordering
✅ Generative AI Task Auditing
✅ Procrastination Detection System

---
# System Workflow

```text
User Creates Task
        ↓
Gemini AI Behavioral Analysis
        ↓
Cognitive & Risk Extraction
        ↓
Constraint-Based Optimization
        ↓
Dynamic Priority Calculation
        ↓
Execution Plan Generation
```

---

# AI-Powered Neuro Layer

ChronoLogic uses the Google Gemini API with a custom-engineered behavioral analysis prompt.

When a user creates a task, the backend sends the task title and description to Gemini AI for behavioral interpretation and cognitive evaluation.

The AI then extracts structured productivity metadata from natural language input.

---

##  AI Behavioral Analysis

### User Input Example

```text
“Complete Operating Systems assignment before Friday”
```

---

##  Gemini AI Output

```json
{
  "predicted_hours": 4,
  "category": "Academic",
  "cognitive_score": 2.9,
  "procrastination_risk": 4.3,
  "task_complexity": "High"
}
```

---

##  Extracted Intelligence

| Feature               | Description                            |
| --------------------- | -------------------------------------- |
| Predicted Time        | AI-estimated realistic task duration   |
| Category Detection    | Academic, Work, Personal, Health, etc. |
| Cognitive Score       | Mental workload estimation             |
| Procrastination Score | Probability of avoidance behavior      |
| Task Complexity       | Difficulty classification              |

---

#  Neuro-Symbolic Optimization Engine

After AI analysis, the Symbolic Layer calculates a dynamic Neuro-Symbolic Priority Score (`ns_score`) using behavioral and mathematical constraints.

The optimization engine continuously evaluates:

* Remaining time
* Task difficulty
* Cognitive workload
* Procrastination tendency
* Reschedule behavior
* Deadline urgency

This enables ChronoLogic to intelligently prioritize the most critical and mentally demanding tasks first.

---

# Priority Calculation Logic

ChronoLogic dynamically prioritizes tasks based on:

✅ Urgency
✅ Mental effort
✅ Time pressure
✅ Avoidance behavior
✅ Deadline postponement

Tasks repeatedly delayed receive behavioral penalties, pushing them higher in the execution queue to reduce chronic procrastination.

---

# 🛠️ Technology Stack

| Technology            | Usage                        |
| --------------------- | ---------------------------- |
| Python 3.x            | Core Programming             |
| PyQt6                 | Desktop Frontend             |
| Django REST Framework | Backend API                  |
| MongoDB / MongoEngine | Database                     |
| Google Gemini API     | AI Behavioral Analysis       |
| JWT Authentication    | Secure Authentication        |
| QThread               | Asynchronous Task Processing |
| Matplotlib            | Productivity Analytics       |

---

#  Key Features

## AI Task Auditing

Analyzes tasks using Gemini AI with custom behavioral prompts.

##  Smart Scheduling

Dynamically reorders tasks using Neuro-Symbolic optimization.

##  Cognitive Analysis

Estimates mental effort and complexity for every task.

##  Anti-Procrastination Engine

Detects and penalizes repeated deadline avoidance.

##  Real-Time Analytics

Visual productivity insights and activity charts.

##  Asynchronous Architecture

Background AI requests using `QThread` ensure a smooth UI experience.

##  Modern Desktop Interface

Built with PyQt6 using a scalable modular architecture.

---

#  Productivity Analytics

ChronoLogic provides advanced productivity insights including:

* Neuro-Activity Distribution
* Brainpower Usage
* Cognitive Load Breakdown
* Task Completion Trends
* Workload Distribution
* Scheduling Efficiency

---

#  Repository Structure

```text
ChronoLogic/
│
├── backend/
│   ├── api/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── services/
│   │   └── gemini_analyzer.py
│   │
│   ├── prompts/
│   │   └── behavioral_prompt.txt
│   │
│   ├── config/
│   └── manage.py
│
├── desktop-app/
│   ├── assets/
│   ├── services/
│   │   └── api_client.py
│   │
│   ├── ui/
│   │   ├── views/
│   │   ├── widgets/
│   │   └── windows/
│   │
│   └── main.py
│
├── docs/
│   ├── dashboard.png
│   ├── analytics.png
│   ├── execution_plan.png
│   ├── architecture.png
│   └── demo.gif
│
├── .env
└── README.md
```

---

#  Installation Guide

## 1️ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ChronoLogic.git
cd ChronoLogic
```

---

## 2️ Setup Backend

```bash
cd backend

python -m venv env
env\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Run backend server:

```bash
python manage.py runserver
```

---

## 3️ Setup Desktop Application

```bash
cd ../desktop-app

python -m venv env
env\Scripts\activate

pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```
---
# Real-World Impact

ChronoLogic explores how Artificial Intelligence and behavioral modeling can improve personal productivity through intelligent scheduling systems.

The project demonstrates the intersection of:

* Artificial Intelligence
* Human Psychology
* Optimization Algorithms
* Behavioral Computing
* Productivity Engineering
* Human-Computer Interaction

---

# Support

If you found this project useful or interesting:

⭐ Star the repository
🍴 Fork the project
📢 Share it on LinkedIn

---

# 📬 Contact

## Waliur Rahman

Software Engineering Student
AI/ML Enthusiast | Neuro-Symbolic Systems | Productivity AI
