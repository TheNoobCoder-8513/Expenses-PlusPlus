# Expenses

A lightweight, high-performance desktop application built using a modern decoupled architecture. It combines the blazing-fast rendering of **Slint UI** with a robust, reliable **Python backend** and **SQLite3** transactional ledger. 

Unlike bloated modern web-wrapped desktop frameworks, this app runs with a very very low memory footprint, delivering instant interface updates and local-first data privacy.

---

### Screenshots
<img width="1920" height="1013" alt="Screenshot From 2026-07-05 13-08-19" src="https://github.com/user-attachments/assets/ac826214-0351-4fd4-b244-bf976d785fa0" />
<img width="1920" height="1013" alt="Screenshot From 2026-07-05 13-08-48" src="https://github.com/user-attachments/assets/324bf7ed-f30d-4f58-aa26-b800d5b45a43" />
<img width="1920" height="1013" alt="Screenshot From 2026-07-05 13-09-08" src="https://github.com/user-attachments/assets/b0a3c60f-08d2-4a91-b1f5-3f04d12a2bdd" />
<img width="1920" height="1013" alt="Screenshot From 2026-07-05 13-09-18" src="https://github.com/user-attachments/assets/8961180f-aa1f-4d65-af3c-eeadb93c3ca8" />

## Key Features

* **Dynamic Ledger Tracking:** Log everyday expenses and income with real-time balance calculations.
* **Local Ledger Architecture:** Stores calculations as signed raw floating-point numbers directly in SQLite3.
* **Interactive Calendar:** Look up daily activities instantly via an adaptive custom grid calendar breakdown.
* **Categorized Spending Analysis:** Automated breakdown of monthly transactions grouped cleanly by categories.
* **Goals and savings:** Track target savings goals alongside liquid balances to manage goals and savings.

---

## The Architecture

The project relies on a strictly decoupled front-end/back-end interface via Slint's IPC bridge:


```

┌────────────────────────┐               ┌────────────────────────┐
│    Slint UI Layer      │  ◄──(Glue)──► │     Python Backend     │
│  (Declarative Layout)  │               │   (SQLite3 / Business) │
└────────────────────────┘               └────────────────────────┘

```

* **Frontend:** `.slint` sheets compile declarative UI components down to native presentation logic. Two-way data binding guarantees layout sync without tedious bubbling up the events.
* **Backend:** A clean Python layer interacts with a local `Expenses.db` database file, exposing business logic securely through registered `@slint.callback` wrappers.

---


## Project Structure

```text
├── Config/
│   └── Theme.slint           
├── Data/
│   └── Expenses.db           
├── Source/
│   └── Main.py               
└── UI/
    ├── UI.slint              
    ├── Glue.slint            
    ├── DataTypes.slint       
    ├── Theme.slint           
    ├── Assets/
    │   └── Icons/            
    ├── Components/           
    │   ├── Base.slint, Button.slint, Chart.slint, ComboBox.slint, Components.slint
    │   ├── Header.slint, Input.slint, Item.slint, Placeholder.slint, Record-Form.slint
    │   └── Sidebar.slint, TabBar.slint, Table.slint
    └── Pages/                
        ├── Page.slint        
        ├── Home/
        │   └── Home.slint, Banner.slint, Today.slint
        ├── Records/
        │   └── Records.slint, RecordItem.slint
        ├── Track/
        │   └── Track.slint, Sidebar.slint
        └── Goals/
            └── Goals.slint, GoalCard.slint, Panel.slint, Summary.slint
```

---


## Quick Start

### 1. Prerequisites

Ensure you have Python 3.10+ installed on your computer.

### 2. Install Dependencies

Set up your virtual environment and install the native Slint compiler toolset pipeline:

```bash
python -m venv .Env
source .Env/bin/activate  # On Windows use: .Env\Scripts\activate
pip install slint

```

### 3. Run the App

Launch the unified native process directly from the project root:

```bash
python Source/Main.py

```
