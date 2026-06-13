# 📺 AI Showrunner Agent v2

> A multi-agent television network simulation where AI executives collaborate, argue, revise, and ultimately decide what goes on air.

---

## Overview

AI Showrunner Agent is a multi-agent system that simulates how a real television network builds its daily broadcast schedule.

Instead of relying on a single prompt to generate a schedule, the system divides responsibilities among specialized agents that each represent a department within a television organization.

The result is not simply a generated lineup.

It is a negotiation process.

Creative vision, content availability, scheduling constraints, executive oversight, and editorial compromises all shape the final broadcast day.

---

## The Problem

Most AI scheduling systems work like this:

```
Input Programs
↓
LLM
↓
Output Schedule
```

This approach often leads to:

* Hallucinated program selections
* Random thematic shifts
* Poor schedule flow
* Weak editorial consistency
* No governance over creative decisions

Television networks don't actually work this way.

Schedules emerge from multiple departments with competing priorities.

This project attempts to simulate that process.

---

# The Television Organization

## 🎬 Showrunner

The creative leader of the network.

Responsibilities:

* Defines the editorial theme of the day
* Establishes the emotional goals
* Creates the creative vision for the broadcast

Example:

> "Fantasy and Family Adventure"

> "Create a day filled with imagination, wonder, optimism, and shared family experiences."

---

## 📚 Librarian

The acquisitions and programming department.

Responsibilities:

* Reviews the entire program inventory
* Curates a shortlist of suitable programs
* Protects the integrity of the Showrunner's vision
* Revises selections based on executive feedback

The Librarian asks:

> "Which programs genuinely belong in this television day?"

---

## 🗓️ Scheduler

The operations department.

Responsibilities:

* Assigns approved programs to broadcast slots
* Maintains daypart flow
* Builds Prime Time around flagship content
* Creates a schedule that feels intentional

The Scheduler asks:

> "How do we turn these ingredients into a coherent day?"

---

## ✅ Validator

The compliance department.

Responsibilities:

* Ensures structural correctness
* Verifies slot assignments
* Prevents invalid program selections
* Guarantees JSON integrity

The Validator asks:

> "Can this schedule legally exist?"

---

## 🏛️ Editorial Review Board

The executive committee.

Responsibilities:

* Reviews the proposed schedule
* Evaluates whether the experience matches the promised vision
* Balances quality against practical constraints
* Approves or rejects schedules for broadcast

The Editorial Board asks:

> "Would we actually put this on the air?"

---

# Workflow

```
Showrunner
↓
Librarian
↓
Scheduler
↓
Validator
↓
Editorial Review Board
```

If approved:

```
Export XML
↓
Broadcast Ready
```

If rejected:

```
Editorial Feedback
↓
Librarian Revision
↓
Scheduler
↓
Validator
↓
Editorial Review Board
```

The system continues iterating until an acceptable schedule is produced.

---

# One Unexpected Discovery

During development, the system repeatedly failed.

Not because of syntax errors.

Not because of Python bugs.

But because the agents exposed a very real television problem:

## Limited Inventory.

Sometimes the network simply doesn't own enough perfectly aligned content to fulfill the creative vision.

This forced the agents to negotiate trade-offs:

* Should a fantasy day tolerate some drama?
* Is repetition acceptable?
* How much compromise is realistic?
* When is a schedule "good enough" to air?

The result became less about optimization and more about organizational decision-making.

---

# Program Repetition

Repeated program assignments are interpreted as:

* Different episodes
* Reruns
* Alternate entries within the same franchise
* Rotating broadcast inventory

For example:

```
Lost Empire
07:00
10:00
14:00
19:00
```

does NOT necessarily mean the same episode aired four times.

It may represent:

```
Lost Empire S01E03
Lost Empire S01E07
Lost Empire S02E01
Lost Empire S02E08
```

This mirrors real broadcast scheduling practices.

---

# Technologies Used

* Python 3
* Ollama
* Qwen 2.5 14B
* PostgreSQL
* Pydantic
* XMLTV Export

---

# Why This Project Exists

This project started as an experiment:

> "Can an LLM generate a television schedule?"

It evolved into something far more interesting:

> "Can multiple AI agents simulate the organizational dynamics of a real television network?"

The answer appears to be:

> Yes.

Not through perfection.

But through negotiation, revision, and compromise.

---

# Future Improvements

Potential future enhancements include:

* Episode-level scheduling
* Agent accountability and blame assignment
* Audience analytics integration
* Historical performance feedback loops
* Programming acquisition agents
* Seasonal and holiday strategies
* Multi-channel network support
* Automatic XMLTV publishing

---

# Final Thought

Television schedules are rarely perfect.

They are products of limited inventory, competing priorities, executive judgment, and practical compromise.

This project attempts to capture that reality.

Because sometimes the most interesting AI systems aren't the ones that always get the right answer.

They're the ones that argue their way toward a decision.

---

*"Would we actually put this on the air tomorrow?"*
