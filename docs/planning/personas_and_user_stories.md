# File: docs/planning/personas_and_user_stories.md

# 👥 DMForge Personas & User Stories

This file defines the core personas supported by DMForge v2, with explicit user stories tied to roadmap phases and enforcement features.

---

## 🧑‍💻 Persona: Solo Developer (You)

### Description  
Neurodivergent (ADHD/autistic) solo developer learning enterprise-grade Python, architecture, and project discipline through DMForge.

### Key Traits
- Executive dysfunction: hard to start, harder to finish
- High intelligence but prone to overbuilding
- Needs strict external structure to avoid drift

### Stories
| ID | User Story |
|----|------------|
| DEV-1 | As a solo dev, I need `start_dev.py` to echo my last task so I know where to resume. |
| DEV-2 | As a neurodivergent dev, I want ADHD mode to reduce decision fatigue and offer just 1–3 next tasks. |
| DEV-3 | As a learner, I want every feature to teach me system design via enforced best practices. |
| DEV-4 | As a perfectionist, I want golden tests and CI gates to reduce my fear of “doing it wrong.” |

---

## 🎲 Persona: New In-Person Dungeon Master

### Description  
Low-experience DM who needs printable decks to reduce prep time.

### Stories
| ID | User Story |
|----|------------|
| DM-1 | As a new DM, I want to filter spells by class and level so I can quickly build an encounter deck. |
| DM-2 | As a print-prep DM, I want my deck rendered as a PDF so I can bring it to the table. |

---

## 👧 Persona: Neurodivergent Child Player (In-Person)

### Description  
Young player (age 7–12) with ADHD or autism, struggles with abstract rules but thrives on visual aids.

### Stories
| ID | User Story |
|----|------------|
| PLR-1 | As a child player, I want to see colorful spell cards so I understand what I can do. |
| PLR-2 | As a neurodivergent learner, I want short descriptions and art that help me stay engaged. |

---

## 🧙 Persona: Neurodivergent Adult Player (In-Person)

### Description  
Adult player with ND traits (ADHD, autism, anxiety), prefers structure and clear options.

### Stories
| ID | User Story |
|----|------------|
| PLR-3 | As a ND adult, I want to print my own spell list so I don’t forget what’s available. |
| PLR-4 | As a visual learner, I want card layouts to follow a clear, repeatable structure. |

---

## 🧱 Persona: Enterprise Learner

### Description  
You, learning enterprise system design through this project.

### Stories
| ID | User Story |
|----|------------|
| ENT-1 | As a system design student, I want each folder to enforce SRP, SoC, and DI. |
| ENT-2 | As a future architect, I want to log all decisions and risks like in a real org. |
| ENT-3 | As a dev with limited memory, I want `start_dev.py` to summarize session state. |

---

**All roadmap phases must reference at least one persona and fulfill at least one story.**
