# Smart Bus Ticket Booking & Reservation System

**Author:** Burhanuddin Qumber

A beginner-friendly Python 3 console application for a small bus service. Users can view routes, search for journeys, book seats, view and cancel bookings, check seat availability, see the route schedule, and generate a booking report, all from a simple text menu.

---

## Purpose

The program manages bus routes and reservations so that:

- Seat counts always stay correct (no overbooking, no negative seats)
- Every booking gets a unique booking ID
- Invalid passenger details are rejected without changing any data
- A cancelled booking restores its seats only once and stays in the history
- Reports count only confirmed bookings in revenue

---

## Requirements

- **Python 3**
- **No external libraries.** Only built-in Python is used.

---

## How to Run

### Option 1: Google Colab

1. Open [Google Colab](https://colab.research.google.com) and create a new notebook.
2. Copy the full contents of `main.py` and paste it into **one** code cell.
3. Run the cell. The menu appears below the cell. Type your choice in the input box and press Enter.
4. To start again with fresh data, run the cell again.

### Option 2: Terminal / VS Code

1. Make sure Python 3 is installed (`python --version`).
2. Open a terminal in the folder that contains `main.py`.
3. Run:

```bash
python main.py
```

(On some systems the command is `python3 main.py`.)

---

## Menu Guide

```
================================
  SMART BUS RESERVATION SYSTEM
================================
1. View Available Routes
2. Search for a Route
3. Book a Ticket
4. View My Bookings
5. Cancel a Booking
6. View Seat Availability
7. Generate Booking Report
8. View Route Schedule
9. Exit
================================
```

| Option | What it does |
|---|---|
| 1. View Available Routes | Lists all routes with journey, time, fare and seats. Optional filter hides fully booked routes. |
| 2. Search for a Route | Search by route ID (e.g. `R101`) or city (e.g. `hyderabad`). Not case-sensitive. Shows a message if nothing matches. |
| 3. Book a Ticket | Asks for name, age, route ID and number of seats. Checks every input, then creates the booking and reduces available seats. |
| 4. View My Bookings | Shows every booking, including cancelled ones. |
| 5. Cancel a Booking | Cancels a Confirmed booking by its ID and gives its seats back. A booking cannot be cancelled twice. |
| 6. View Seat Availability | Shows available / total seats with status: Available, Partially Booked or Fully Booked. Optional filter. |
| 7. Generate Booking Report | Shows total, confirmed and cancelled bookings, reserved seats, confirmed revenue, fully booked routes, and a breakdown by route. |
| 8. View Route Schedule | Groups routes by departure city. Cities with no departures show "No scheduled departures." |
| 9. Exit | Ends the program. |

Invalid menu input (text like `abc` or a number like `15`) shows an error message and returns to the menu.

> **Note:** The PRD menu lists 8 options, but Feature 10 (Route Schedule) is also required. So the schedule was added as option 8, and Exit moved to option 9.

---

## Starting Routes

| Route ID | From | To | Departure | Fare (Rs.) | Seats |
|---|---|---|---|---|---|
| R101 | Karachi | Hyderabad | 08:00 AM | 1,200 | 40 |
| R102 | Karachi | Sukkur | 09:30 AM | 2,000 | 36 |
| R103 | Hyderabad | Mirpur Khas | 11:00 AM | 800 | 32 |
| R104 | Karachi | Lahore | 07:00 PM | 5,000 | 45 |
| R105 | Sukkur | Hyderabad | 02:00 PM | 1,500 | 30 |

---

## Sample Workflow

1. **Book:** choose `3` → Name `Ahmed`, Age `24`, Route `R101`, Seats `2`
   → Booking `B1001` confirmed, total fare Rs. 2400. R101 now has 38/40 seats.
2. **View bookings:** choose `4` → B1001 is listed with status Confirmed.
3. **Cancel:** choose `5` → enter `B1001`
   → Booking cancelled, 2 seats restored, R101 back to 40 seats.
4. **Cancel again:** choose `5` → enter `B1001`
   → "Booking B1001 is already cancelled." Seats are not restored again.
5. **Report:** choose `7`
   → B1001 is counted as Cancelled and its fare is not included in revenue.

---

## Validation Rules

| Input | Rule |
|---|---|
| Name | Cannot be empty or only spaces |
| Age | Must be a whole number greater than 0 |
| Route ID | Must be an existing route |
| Seats | Must be a whole number greater than 0, and not more than the available seats |

If any check fails, the program shows a message and **nothing is changed**: no booking is created and no seats are reduced.

---

## Data Structures Used

| Structure | Used for | Why |
|---|---|---|
| List of dictionaries | `routes`, `bookings` | Many records, each with named fields |
| Tuple | `cities` | Fixed list of cities that never changes |
| Set | `booking_ids` | Keeps every booking ID unique |

---

## Project Files

| File | Description |
|---|---|
| `main.py` | Complete program source code |
| `README.md` | This guide |
| `test_cases.txt` | 12 required test cases with expected and actual results |
| `01_routes.png` ... `10_invalid_menu.png` | Screenshots of the program output |

---

## Limitations

- **Data is stored in memory only.** All routes, bookings and changes are lost when the program closes. Every new run starts with the five original routes and no bookings.
- Console (text) interface only. No website, GUI, database or payment system.
- Seat numbers are not assigned; only the number of seats is booked.
- Search needs the full city name or route ID (e.g. `hyd` will not match `Hyderabad`).
