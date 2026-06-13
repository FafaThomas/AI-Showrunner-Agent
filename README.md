# 📺 AI Showrunner Agent

An experimental multi-stage AI system that simulates the daily operations of a television network by generating editorially curated broadcast schedules using Large Language Models (LLMs), historical audience insights, and deterministic validation.

---

## Overview

AI Showrunner Agent explores the intersection of:

* Artificial Intelligence
* Television Programming
* Data Engineering
* Prompt Engineering
* Multi-stage Decision Systems

The project began as an attempt to generate realistic television scheduling datasets for analytics and evolved into an AI-driven scheduling system capable of proposing, validating, and reviewing an entire day of programming.

---

## Features

### 🎬 Synthetic Broadcast Dataset Generation

Generate years of mock television operational data including:

* Program scheduling
* Commercial placement
* Audience viewership metrics
* Retention and drop-off rates
* Advertising revenue estimates

Generated data is stored in PostgreSQL for later analysis.

---

### 🧠 AI Showrunner

Using a local LLM through Ollama, the Showrunner:

* Determines a daily editorial theme
* Considers network identity
* Incorporates historical viewing insights
* Builds a complete 24-hour broadcast schedule
* Provides editorial reasoning for every programming decision

---

### 🏛 Structural Validation

Schedules undergo deterministic validation to ensure:

* Exactly 24 slots are returned
* All slot identifiers exist
* All selected programs exist
* Duplicate slot assignments are prevented
* JSON responses conform to the expected schema

This prevents the LLM from generating structurally invalid schedules.

---

### 👔 Editorial Review Board

Beyond technical correctness, schedules are evaluated for quality.

Examples include:

* Prime Time consistency
* Theme alignment
* Morning programming suitability
* Genre balance
* Audience appropriateness

The goal is to answer:

> "Should this schedule actually air?"

rather than merely:

> "Can this schedule air?"

---

### 🔁 Executive Revision Loop

Rejected schedules receive feedback and are regenerated.

The workflow resembles a real television organization:

Showrunner → Executive Notes → Revision → Approval

Instead of failing immediately, the agent attempts multiple revisions before terminating.

---

## System Architecture

```
Historical Insights
        │
        ▼
Network Identity
        │
        ▼
Prompt Builder
        │
        ▼
Qwen 2.5 14B (Ollama)
        │
        ▼
Pydantic Models
        │
        ▼
Structural Validator
        │
        ▼
Editorial Review
        │
        ▼
XML Export
```

---

## Technology Stack

### Backend

* Python 3
* PostgreSQL
* Docker

### AI

* Ollama
* Qwen 2.5 14B

### Validation

* Pydantic v2

### Data Access

* psycopg2

### Configuration

* python-dotenv

---

## Database Components

The system models a television network using:

### Program Catalog

Contains:

* Program titles
* Genres
* Program types
* Target demographics
* Ratings information

### Broadcast Slots

Defines:

* Hourly scheduling windows
* Dayparts
* Slot durations

### Viewership Metrics

Stores:

* Viewer counts
* Average watch times
* Retention rates
* Drop-off rates
* Advertising revenue

---

## Synthetic Dataset Generation

A separate generation pipeline was used to create several years of operational broadcast data.

Generated records include:

### Slot Program Assignments

```
slot_program
```

Maps programs to scheduled slots.

### Commercial Placements

```
slot_commercial
```

Stores commercial sequencing.

### Audience Metrics

```
slot_viewership
```

Captures simulated audience behavior.

The dataset can be reused for:

* Data engineering projects
* SQL analytics
* Dashboarding
* Machine learning experiments
* Recommendation systems

---

## Example Workflow

```
Load Historical Memory
        │
Determine Theme
        │
Consult Showrunner
        │
Generate Schedule
        │
Validate Structure
        │
Review Editorial Quality
        │
Approved?
 ┌──────┴──────┐
 │             │
No            Yes
 │             │
Revision     Export XML
 │
Retry
```

---

## Motivation

This project originally started as an experiment in synthetic data generation for portfolio projects involving SQL and analytics.

Over time, it evolved into a question:

> "Can an AI behave like a television programming department?"

Rather than simply producing JSON, the system attempts to simulate the actual organizational workflow behind broadcast decision-making.

---

## Future Directions

Potential future enhancements include:

* Retrieval-Augmented Generation (RAG)
* Catalog Librarian agents
* Multi-agent scheduling workflows
* Audience segmentation models
* Recommendation engines
* Ratings forecasting
* Automated commercial optimization
* Interactive scheduling dashboards

---

## Repository Goals

This project serves as a demonstration of:

* Applied AI engineering
* System design
* Data engineering
* Prompt engineering
* Validation strategies
* Human-in-the-loop style workflows

It is intentionally experimental and designed as a learning platform for exploring how deterministic systems and generative models can work together.

---

## License

This repository is intended for educational and portfolio purposes.
