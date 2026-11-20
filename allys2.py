def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Error: Value must be greater than 0. Try again.")
                continue
            return value
        except ValueError:
            print("Error: Invalid number! Please enter a number.")

def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 2:
                print("Error: Route must have at least 2 stops.")
                continue
            return value
        except ValueError:
            print("Error: Invalid number! Please enter a whole number.")

def get_route():
    stops = []
    distances = []
    n = get_positive_int("How many stops on the route? ")
    
    for i in range(n):
        while True:
            name = input(f"Enter name of stop {i+1}: ").strip()
            if name == "":
                print("Error: Stop name cannot be empty!")
                continue
            # ERROR 1: REPETITION - same stop name twice
            if name.lower() in [s.lower() for s in stops]:
                print(f"Error: Stop '{name}' already exists! No repetition allowed.")
                continue
            stops.append(name)
            break
    
    print("\n--- Enter distances between stops ---")
    for i in range(n-1):
        d = get_positive_float(f"Distance from {stops[i]} to {stops[i+1]} (km): ")
        distances.append(d)
    
    return stops, distances

def get_passengers_for_legs(stops, distances):
    passengers_in_legs = []
    print("\n--- Who is in the car for each leg? ---")
    print("RULE: Names must be separated by comma. Example: Tapiwa,Rue")
    
    for i in range(len(distances)):
        while True:
            print(f"\nLeg {i+1}: {stops[i]} -> {stops[i+1]} ({distances[i]} km)")
            names_input = input("Who is in car? ").strip()
            
            if names_input == "":
                print("Error: Car cannot be empty for a leg! Enter at least one person.")
                continue

            # ERROR 2: COMMA CHECK
            # If user typed space but no comma, e.g., "Tapiwa Rue" -> error
            if "," not in names_input and " " in names_input:
                print("Error: Names must be separated by COMMA, not space! Example: Tapiwa,Rue")
                continue

            people = [p.strip() for p in names_input.split(",") if p.strip() != ""]
            
            if len(people) == 0:
                print("Error: Invalid format! Use: Name1,Name2")
                continue

            # Check for empty names caused by double comma e.g. "Tapiwa,,Rue"
            if names_input.count(",") + 1 != len(people):
                print("Error: Invalid comma usage! Check for double commas like 'Tapiwa,,Rue'")
                continue

            # ERROR 3: REPETITION - same person twice in same leg
            lower_people = [p.lower() for p in people]
            if len(lower_people) != len(set(lower_people)):
                print(f"Error: Repetition! Same person entered twice in same leg: {names_input}")
                continue

            # Check each name is valid (only letters)
            invalid = False
            for p in people:
                if not p.replace(" ", "").isalpha():
                    print(f"Error: Invalid name '{p}'! Names should contain only letters.")
                    invalid = True
                    break
            if invalid:
                continue

            passengers_in_legs.append(people)
            break
            
    return passengers_in_legs

def calculate_shares(distances, passengers_in_legs, total_cost):
    shares = {}
    leg_costs = []
    total_distance = sum(distances)
    for i in range(len(distances)):
        leg_cost = (distances[i] / total_distance) * total_cost
        leg_costs.append(leg_cost)
        split = leg_cost / len(passengers_in_legs[i])
        for person in passengers_in_legs[i]:
            # Use original case for key but keep case-insensitive sum
            # Find existing key with same lower case
            found_key = None
            for k in shares:
                if k.lower() == person.lower():
                    found_key = k
                    break
            if found_key:
                shares[found_key] += split
            else:
                shares[person] = split
    return shares, leg_costs

def show_summary(stops, distances, passengers_in_legs, leg_costs, shares, total_cost):
    print("\n======== TRIP SUMMARY FOR DRIVER ========")
    print(f"Total Distance: {sum(distances)} km | Total Cost: ${total_cost:.2f}\n")
    for i in range(len(distances)):
        print(f"  {stops[i]} -> {stops[i+1]} | {distances[i]} km | ${leg_costs[i]:.2f} | {', '.join(passengers_in_legs[i])}")
    print("\nFair Share Per Person:")
    for person, amount in shares.items():
        print(f"  {person}: ${amount:.2f}")
    print(f"\nCheck: Sum = ${sum(shares.values()):.2f} (Should be ${total_cost:.2f})")

def save_to_file(stops, distances, passengers_in_legs, leg_costs, shares, total_cost):
    try:
        with open("trip_summary.txt", "w") as f:
            f.write(f"Total Cost: ${total_cost:.2f}\n")
            for i in range(len(distances)):
                f.write(f"Leg {i+1}: {stops[i]} -> {stops[i+1]} | {leg_costs[i]:.2f} | {', '.join(passengers_in_legs[i])}\n")
            for p,a in shares.items():
                f.write(f"{p}: ${a:.2f}\n")
        print("\nSaved to trip_summary.txt")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    print("Case 12: Ride-Share Trip Cost Splitter\n")
    while True:
        choice = input("Do you want to (1) Enter total fare or (2) Estimate from fuel? Enter 1 or 2: ").strip()
        if choice in ["1","2"]:
            break
        print("Error: Invalid choice! Enter 1 or 2.")

    stops, distances = get_route()
    passengers_in_legs = get_passengers_for_legs(stops, distances)

    if choice == "2":
        consumption = get_positive_float("\nCar consumption (L/100km): ")
        fuel_price = get_positive_float("Fuel price per litre: $")
        total_cost = (sum(distances)/100) * consumption * fuel_price
        print(f"Estimated Cost: ${total_cost:.2f}")
    else:
        total_cost = get_positive_float("\nEnter total fare to split: $")

    shares, leg_costs = calculate_shares(distances, passengers_in_legs, total_cost)
    show_summary(stops, distances, passengers_in_legs, leg_costs, shares, total_cost)
    save_to_file(stops, distances, passengers_in_legs, leg_costs, shares, total_cost)

main()