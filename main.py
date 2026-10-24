# =========================================================
# SMART BUS TICKET BOOKING & RESERVATION SYSTEM
# A Python 3 console application (built-in Python only)
# Note: all data is stored in memory and is lost when the program ends
# =========================================================


# ===== STEP 1: DATA SETUP =====

# All bus routes: a list where each route is a dictionary
routes = [
    {
        "route_id": "R101",
        "departure_city": "Karachi",
        "destination_city": "Hyderabad",
        "departure_time": "08:00 AM",
        "ticket_price": 1200,
        "total_seats": 40,
        "available_seats": 40
    },
    {
        "route_id": "R102",
        "departure_city": "Karachi",
        "destination_city": "Sukkur",
        "departure_time": "09:30 AM",
        "ticket_price": 2000,
        "total_seats": 36,
        "available_seats": 36
    },
    {
        "route_id": "R103",
        "departure_city": "Hyderabad",
        "destination_city": "Mirpur Khas",
        "departure_time": "11:00 AM",
        "ticket_price": 800,
        "total_seats": 32,
        "available_seats": 32
    },
    {
        "route_id": "R104",
        "departure_city": "Karachi",
        "destination_city": "Lahore",
        "departure_time": "07:00 PM",
        "ticket_price": 5000,
        "total_seats": 45,
        "available_seats": 45
    },
    {
        "route_id": "R105",
        "departure_city": "Sukkur",
        "destination_city": "Hyderabad",
        "departure_time": "02:00 PM",
        "ticket_price": 1500,
        "total_seats": 30,
        "available_seats": 30
    }
]

# Supported cities: fixed values that never change, so we use a tuple
cities = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")

# All bookings will be stored here (empty at the start)
bookings = []

# Booking IDs already issued (a set keeps every ID unique)
booking_ids = set()


# ===== STEP 3: VIEW AVAILABLE ROUTES =====

def view_routes():
    # Ask whether to show only routes that still have seats
    answer = input("Show only routes with available seats? (yes/no): ").strip().lower()
    only_available = answer == "yes" or answer == "y"

    print("\nAVAILABLE BUS ROUTES")
    print("No. | Route | Journey | Depart | Fare | Seats")
    print("------------------------------------------------------------")

    for number, route in enumerate(routes, start=1):
        # Skip fully booked routes when the filter is on
        if only_available and route["available_seats"] == 0:
            continue

        # Decide what to show in the seats column
        if route["available_seats"] == 0:
            seats_text = "Fully Booked"
        else:
            seats_text = f"{route['available_seats']}/{route['total_seats']}"

        # Join the two cities into one journey text
        journey = route["departure_city"] + " -> " + route["destination_city"]

        print(f"{number} | {route['route_id']} | {journey} | {route['departure_time']} | Rs.{route['ticket_price']} | {seats_text}")


# ===== STEP 4: SEARCH FOR A ROUTE =====

def search_route():
    # Read the search term in lowercase for case-insensitive matching
    term = input("Search by route ID or city: ").strip().lower()

    # Loop 1: search by route ID (IDs are unique, so stop at the first match)
    for route in routes:
        if route["route_id"].lower() == term:
            journey = route["departure_city"] + " -> " + route["destination_city"]
            print(f"{route['route_id']} | {journey} | Rs. {route['ticket_price']} | {route['available_seats']} seats available")
            break
    else:
        # Runs only if Loop 1 finished without break (no route ID matched)
        found = False  # Flag: becomes True when at least one city matches

        # Loop 2: search by departure or destination city (show all matches)
        for route in routes:
            if route["departure_city"].lower() == term or route["destination_city"].lower() == term:
                journey = route["departure_city"] + " -> " + route["destination_city"]
                print(f"{route['route_id']} | {journey} | Rs. {route['ticket_price']} | {route['available_seats']} seats available")
                found = True

        if not found:
            print("No matching routes found.")


# ===== STEP 5: BOOK A TICKET =====

def book_ticket():
    print("\nBOOK A TICKET")

    # Check 1: passenger name must not be empty
    name = input("Enter passenger name: ").strip()
    if name == "":
        print("Booking failed: Name cannot be empty.")
        return  # Stop here, nothing is changed

    # Check 2: age must be a whole number greater than zero
    try:
        age = int(input("Enter passenger age: "))
    except ValueError:
        print("Booking failed: Age must be a number.")
        return
    if age <= 0:
        print("Booking failed: Age must be greater than zero.")
        return

    # Check 3: route ID must exist
    route_id = input("Enter route ID (e.g. R101): ").strip().upper()
    for route in routes:
        if route["route_id"] == route_id:
            selected_route = route  # Remember the matching route
            break
    else:
        # Runs only if the loop finished without break (route not found)
        print("Booking failed: Route", route_id, "does not exist.")
        return

    # Check 4: number of seats must be a whole number greater than zero
    try:
        seats = int(input("Enter number of seats: "))
    except ValueError:
        print("Booking failed: Seats must be a number.")
        return
    if seats <= 0:
        print("Booking failed: Seats must be greater than zero.")
        return

    # Check 5: requested seats must not be more than available seats
    if seats > selected_route["available_seats"]:
        print(f"Booking failed: Only {selected_route['available_seats']} seats available on {route_id}.")
        return

    # All checks passed: create a unique booking ID
    id_number = 1001 + len(bookings)
    booking_id = "B" + str(id_number)
    while booking_id in booking_ids:  # If this ID already exists, try the next number
        id_number += 1
        booking_id = "B" + str(id_number)

    # Calculate the total fare
    total_fare = selected_route["ticket_price"] * seats

    # Create the booking record
    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route_id,
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed"
    }

    # Save the booking, save the ID, and reduce the available seats
    bookings.append(booking)
    booking_ids.add(booking_id)
    selected_route["available_seats"] -= seats

    # Show the confirmation
    journey = selected_route["departure_city"] + " -> " + selected_route["destination_city"]
    print("\nBooking confirmed!")
    print("Booking ID:", booking_id)
    print("Passenger:", name)
    print(f"Route: {route_id} ({journey})")
    print("Seats booked:", seats)
    print("Fare per seat: Rs.", selected_route["ticket_price"])
    print("Total fare: Rs.", total_fare)
    print("Status: Confirmed")


# ===== STEP 6: VIEW MY BOOKINGS =====

def view_bookings():
    # If there are no bookings yet, show a message and stop
    if len(bookings) == 0:
        print("No bookings found.")
        return

    print("\nMY BOOKINGS")
    print("No. | Booking ID | Passenger | Route | Seats | Fare | Status")
    print("------------------------------------------------------------")

    # Number each booking (cancelled bookings are shown too, for history)
    for number, booking in enumerate(bookings, start=1):
        print(f"{number} | {booking['booking_id']} | {booking['passenger_name']} | {booking['route_id']} | {booking['seats']} | Rs.{booking['total_fare']} | {booking['status']}")


# ===== STEP 7: CANCEL A BOOKING =====

def cancel_booking():
    # Nothing to cancel if there are no bookings
    if len(bookings) == 0:
        print("No bookings found.")
        return

    booking_id = input("Enter booking ID to cancel: ").strip().upper()

    for booking in bookings:
        if booking["booking_id"] == booking_id:
            # Booking found: only a Confirmed booking can be cancelled
            if booking["status"] == "Confirmed":
                # Find the route of this booking and give its seats back
                for route in routes:
                    if route["route_id"] == booking["route_id"]:
                        route["available_seats"] += booking["seats"]
                        break

                # Keep the record for history, only change its status
                booking["status"] = "Cancelled"

                print(f"Booking {booking_id} has been cancelled.")
                print("Seats restored:", booking["seats"])
                print(f"Route {route['route_id']} available seats: {route['available_seats']}")
            else:
                # Already cancelled: do not restore seats again
                print(f"Booking {booking_id} is already cancelled.")
            break  # Booking IDs are unique, so stop searching
    else:
        # Runs only if the loop finished without break (ID not found)
        print(f"Booking {booking_id} not found.")


# ===== STEP 8: VIEW SEAT AVAILABILITY =====

def seat_availability():
    # Ask whether to show only routes that still have seats
    answer = input("Show only routes with available seats? (yes/no): ").strip().lower()
    only_available = answer == "yes" or answer == "y"

    print("\nSEAT AVAILABILITY")
    print("Route | Journey | Available / Total | Status")
    print("------------------------------------------------------------")

    for route in routes:
        available = route["available_seats"]
        total = route["total_seats"]

        # Skip fully booked routes when the filter is on
        if only_available and available == 0:
            continue

        # Decide the seat status of this route
        if available == total:
            status = "Available"
        elif available > 0:
            status = "Partially Booked"
        else:
            status = "Fully Booked"

        journey = route["departure_city"] + " -> " + route["destination_city"]
        print(f"{route['route_id']} | {journey} | {available} / {total} | {status}")


# ===== STEP 9: GENERATE BOOKING REPORT =====

def booking_report():
    # Count every booking record, including cancelled ones
    total_bookings = len(bookings)

    # Count bookings by status
    confirmed_count = 0
    cancelled_count = 0
    for booking in bookings:
        if booking["status"] == "Confirmed":
            confirmed_count += 1
        elif booking["status"] == "Cancelled":
            cancelled_count += 1

    # Overall totals start at zero
    reserved_seats = 0
    confirmed_revenue = 0
    fully_booked_routes = 0

    print("\n========== BOOKING REPORT ==========")
    print("Confirmed bookings by route:")

    # Outer loop: visit every route
    for route in routes:
        route_seats = 0
        route_revenue = 0

        # Inner loop: find the confirmed bookings of this route
        for booking in bookings:
            if booking["route_id"] == route["route_id"] and booking["status"] == "Confirmed":
                route_seats += booking["seats"]
                route_revenue += booking["total_fare"]

        print(f"{route['route_id']} | Seats: {route_seats} | Revenue: Rs. {route_revenue:,}")

        # Add this route's numbers to the overall totals
        reserved_seats += route_seats
        confirmed_revenue += route_revenue

        # Count routes with no seats left
        if route["available_seats"] == 0:
            fully_booked_routes += 1

    print("\nSummary:")
    print("Total bookings created:", total_bookings)
    print("Confirmed bookings:", confirmed_count)
    print("Cancelled bookings:", cancelled_count)
    print("Seats currently reserved:", reserved_seats)
    print(f"Confirmed revenue: Rs. {confirmed_revenue:,}")
    print("Fully booked routes:", fully_booked_routes)


# ===== STEP 10: ROUTE SCHEDULE =====

def route_schedule():
    print("\nROUTE SCHEDULE BY DEPARTURE CITY")

    # Outer loop: visit every supported city
    for city in cities:
        print(city)
        found = False  # Flag: becomes True when a route departs from this city

        # Inner loop: find the routes that depart from this city
        for route in routes:
            if route["departure_city"] == city:
                print(f"  {route['route_id']} -> {route['destination_city']} | {route['departure_time']}")
                found = True

        # No route departs from this city
        if not found:
            print("  No scheduled departures.")


# ===== STEP 2: MAIN MENU LOOP (always at the bottom) =====

while True:
    # Show the main menu
    print("\n================================")
    print("  SMART BUS RESERVATION SYSTEM")
    print("================================")
    print("1. View Available Routes")
    print("2. Search for a Route")
    print("3. Book a Ticket")
    print("4. View My Bookings")
    print("5. Cancel a Booking")
    print("6. View Seat Availability")
    print("7. Generate Booking Report")
    print("8. View Route Schedule")
    print("9. Exit")
    print("================================")

    # Read the user's choice and convert it to a number
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        # Text like "abc" cannot be converted to a number
        print("Invalid input! Please enter a number from 1 to 9.")
        continue  # Skip the rest and show the menu again

    # Run the selected option
    if choice == 1:
        view_routes()
    elif choice == 2:
        search_route()
    elif choice == 3:
        book_ticket()
    elif choice == 4:
        view_bookings()
    elif choice == 5:
        cancel_booking()
    elif choice == 6:
        seat_availability()
    elif choice == 7:
        booking_report()
    elif choice == 8:
        route_schedule()
    elif choice == 9:
        print("Thank you for using Smart Bus Reservation System. Goodbye!")
        break  # Stop the loop and end the program
    else:
        # A number outside 1-9, like 0 or 15
        print("Invalid choice! Please choose a number from 1 to 9.")
