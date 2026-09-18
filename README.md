# Smart Service Center Engine

**Samsung Innovation Campus — Chapter 4: Algorithm 1 (Data Structures), Units 22–27**
Individual challenge · Single-file Python command-line application

A small service-center system that accepts customer requests, processes them in FIFO order, and lets the user sort, search, and analyze them. Every core data structure and algorithm is written by hand — no `sort()`, `sorted()`, or `dict` shortcuts.

---

## 1. How to Run

**Requirements**

- Python 3.8 or newer
- The `tabulate` package (used only to print tables)

```bash
pip install tabulate
```

**Start the program**

```bash
python task_smart_service_center_engine.py
```

The menu keeps running until you choose option **13 (Exit)**.

### Seed data

On startup the program loads `requests.json` from the same folder as the script. Export the provided Excel data pack to this JSON format (a list of records) and save it as `requests.json`:

```json
[
    { "id": 3, "name": "Sara", "priority": 2, "est_time": 30, "status": "Pending" },
    { "id": 1, "name": "Omar", "priority": 5, "est_time": 15, "status": "Pending" }
]
```

| Field      | Type    | Meaning                                  |
|------------|---------|------------------------------------------|
| `id`       | integer | Unique request ID                        |
| `name`     | text    | Customer name                            |
| `priority` | integer | Priority scale 1–5                       |
| `est_time` | integer | Estimated service time in minutes        |
| `status`   | text    | `Pending` (new) or `Processed`           |

- If `requests.json` does not exist, the program simply starts with an empty queue.
- The seed data does not need to be ordered. On load, the records are sorted by ID using the program's own Insertion Sort before being placed in the Queue.
- New request IDs continue automatically from the highest loaded ID + 1.
- The waiting queue is saved back to `requests.json` after adding/processing a request and on exit.

---

## 2. Menu Features

| #  | Option                                     | What it does                                                                 |
|----|--------------------------------------------|------------------------------------------------------------------------------|
| 1  | Add New Request                            | Asks for name, priority (1–5), and optional est. time, then enqueues it      |
| 2  | Process Next Request                       | Dequeues the oldest request (FIFO), marks it `Processed`, stores it          |
| 3  | View Next Request in Queue                 | Shows the front of the queue without removing it                             |
| 4  | Display Pending Queue                      | Prints the waiting queue as a table                                          |
| 5  | Lookup Request via HashTable               | Direct lookup by ID (works for both pending and processed requests)          |
| 6  | Sort Requests                              | Choose Bubble / Selection / Insertion sort and a field; shows the counts     |
| 7  | Search Request (Sequential)                | Sequential search over the **processed** requests                            |
| 8  | Search Request (Binary)                    | Binary search over the **queue** by ID; gives an insert position if missing  |
| 9  | View Most Recent Search                    | `peek()` on the search-history Stack                                         |
| 10 | Undo/Remove Last Search                    | `pop()` on the search-history Stack                                          |
| 11 | Show algorithm statistics                  | Runs all three sorts on the current queue and compares them                  |
| 12 | Show Processed Requests                    | Prints the processed collection as a table                                   |
| 13 | Exit                                       | Saves the queue and quits                                                    |

---

## 3. How the Program Is Built

### Custom data structures

| Structure     | Implementation                                                                 | Used for                                                 |
|---------------|--------------------------------------------------------------------------------|----------------------------------------------------------|
| `Queue`       | `enqueue()`, `dequeue()`, `front()`, `is_empty()` — first in, first out        | Waiting requests                                         |
| `Stack`       | `push()`, `pop()`, `peek()`, `is_empty()` — last in, first out                 | Search history                                           |
| `HashTable`   | 10 buckets, `hash(key) = key % size`, `put()`, `get()`, separate chaining      | Instant lookup of any request by ID                      |

- `dequeue()` on an empty Queue and `pop()`/`peek()` on an empty Stack return `None` instead of crashing, and the menu prints a friendly message.
- The HashTable resolves collisions with **chaining**: IDs that land in the same bucket (for example 1 and 11) are stored together in that bucket's list, and `put()` on an existing ID updates the record instead of duplicating it.

### Algorithms (all manual)

| Algorithm         | Returns                                                       | Notes                                                                 |
|-------------------|---------------------------------------------------------------|-----------------------------------------------------------------------|
| Bubble Sort       | sorted data, comparisons, swaps, sort field                   | Compares every adjacent pair on every pass (no early-exit flag)       |
| Selection Sort    | sorted data, comparisons, swaps, sort field                   | Always scans the whole unsorted part                                  |
| Insertion Sort    | sorted data, comparisons, shifts, sort field                  | Stops shifting as soon as the correct position is found               |
| Sequential Search | found / not found, index, comparisons, method                 | Works on unsorted data                                                |
| Binary Search     | found / not found, index **or insert position**, comparisons  | Requires data sorted by ID; returns `left` as the insert position     |

Sorting compares `[field_value, id]` pairs, so requests with equal priority or time are ordered by ID and results are always deterministic.

### Search history

Every search (Sequential, Binary, and HashTable lookup) is pushed onto the history Stack as a record containing:

`target ID` · `method` · `result (Found / Not Found)` · `position` · `comparisons`

Option 9 shows the newest record with `peek()`; option 10 removes it with `pop()`.

### Input validation

| Situation                               | Behavior                                                       |
|-----------------------------------------|----------------------------------------------------------------|
| Priority outside 1–5                    | Defaults to priority 5                                         |
| Priority that is not a number           | Request is rejected with an error message                      |
| Estimated time left blank               | Defaults to 15 minutes                                         |
| Estimated time that is not a number     | Request is rejected with an error message                      |
| Search/lookup ID that is not a number   | "Invalid ID" message; the menu continues                       |
| Process/search on an empty collection   | Clear message, no crash                                        |
| Unknown menu choice                     | "Invalid option" message; the menu continues                   |
| Duplicate IDs                           | New IDs are generated automatically, so they never repeat; if the seed file contains the same ID twice, the HashTable keeps the later record |

---

## 4. Screenshots

Screenshots taken from the running program (Windows Command Prompt), using the seed data (IDs 101–107).

### Main menu
![Main menu](screenshots/01_menu.png)

### Option 1 — Add New Request
![Add new request](screenshots/02_add_request.png)

### Option 4 — Display Pending Queue
![Pending queue](screenshots/03_pending_queue.png)

### Option 12 — Show Processed Requests
![Processed requests](screenshots/04_processed_requests.png)

### Option 6 — Sort Requests (Selection Sort by priority)
![Sort requests](screenshots/05_sort_requests.png)

### Option 11 — Show algorithm statistics
![Algorithm statistics](screenshots/06_algorithm_statistics.png)

---

## 5. Sample Terminal Session

Seed data: 5 records (IDs 1–5, loaded out of order from `requests.json`). Lines starting with `>` are user input. Menu redraws are omitted for brevity.

```text
> 1  (Add New Request)
Enter name: Hana
Enter priority(1:5): 1
Enter Estimated Service Time(option): 25
Request added successfully.

> 2  (Process Next Request)
Processed Request ID: 1
> 2
Processed Request ID: 2

> 4  (Display Pending Queue)
╭──────┬────────┬────────────┬────────────┬──────────╮
│   ID │ Name   │   Priority │   Est Time │ Status   │
├──────┼────────┼────────────┼────────────┼──────────┤
│    3 │ Sara   │          2 │         30 │ Pending  │
│    4 │ Mona   │          4 │         20 │ Pending  │
│    5 │ Laila  │          1 │         45 │ Pending  │
│    6 │ Hana   │          1 │         25 │ Pending  │
╰──────┴────────┴────────────┴────────────┴──────────╯

> 7  (Sequential Search, found)
Enter Request ID to search (Sequential): 2
Result: Found at index 1 | Comparisons: 2 | Method: Sequential Search
Request Details: {'id': 2, 'name': 'Youssef', 'priority': 3, 'est_time': 10, 'status': 'Processed'}

> 7  (Sequential Search, not found)
Enter Request ID to search (Sequential): 9
Result: Not Found | Comparisons: 2 | Method: Sequential Search

> 8  (Binary Search, found)
Enter Request ID to search (binary): 4
Result: Found at index 1 | Comparisons: 1 | Method: Binary Search
Request Details: {'id': 4, 'name': 'Mona', 'priority': 4, 'est_time': 20, 'status': 'Pending'}

> 8  (Binary Search, not found -> insert position)
Enter Request ID to search (binary): 7
Result: Not Found (Suggested insert position: index 4) | Comparisons: 3 | Method: Binary Search

> 5  (Hash lookup, found)
Enter Request ID to lookup: 3
Found Request: {'id': 3, 'name': 'Sara', 'priority': 2, 'est_time': 30, 'status': 'Pending'}

> 5  (Hash lookup, not found)
Enter Request ID to lookup: 9
Request not found in HashTable.

> 6  (Sort by estimated time)
Enter sorting method (bubble_sort/select_sort/insert_sort): insert_sort
Enter key to sort by (priority/est_time): est_time
Sorted by est_time using insert_sort. Comparisons: 5, Swaps: 3
╭──────┬────────┬────────────┬────────────┬──────────╮
│   ID │ Name   │   Priority │   Est Time │ Status   │
├──────┼────────┼────────────┼────────────┼──────────┤
│    4 │ Mona   │          4 │         20 │ Pending  │
│    6 │ Hana   │          1 │         25 │ Pending  │
│    3 │ Sara   │          2 │         30 │ Pending  │
│    5 │ Laila  │          1 │         45 │ Pending  │
╰──────┴────────┴────────────┴────────────┴──────────╯

> 9  (View last search)
--- Last Search Record ---
Target ID: 9
Method: HashTable
Result: Not Found
Position: N/A
Comparisons: 1

> 10 (Remove last search)
Removed search record for ID 9 from history.

> 9
--- Last Search Record ---
Target ID: 3
Method: HashTable
Result: Found
Position: N/A
Comparisons: 1

> 13
Goodbye!
```

> The HashTable lookup is recorded as **1 comparison** because it jumps straight to one bucket by index.

---

### Quick comparison (8 items)

| Input          | Bubble Sort | Selection Sort | Insertion Sort |
|----------------|-------------|----------------|----------------|
| Already sorted | 28 comps    | 28 comps       | 7 comps        |
| Reverse sorted | 28 comps    | 28 comps       | 28 comps       |

---

## 6. Notes

- **Sorting and searching scope:** option 6 sorts a *copy* of the waiting queue (the queue itself stays in FIFO order); option 7 searches the processed list; option 8 searches the waiting queue.
- **Binary Search precondition:** the queue must be ordered by ID. This holds automatically because seed data is sorted by ID on load and new IDs always increase.
- **Persistence:** only the waiting queue is saved to `requests.json`. Processed requests live in memory for the current session.
- **Statuses used:** `Pending` and `Processed`.
- **Bonus features included:** hash-collision handling (chaining) and a sorting benchmark (option 11) on the current queue data.
