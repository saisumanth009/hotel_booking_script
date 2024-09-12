import json

# Provided input dictionary
input_data = {
    "assignment_results": [
        {
            "deep_link": "https://www.booking.com/searchresults.en-US.html?dest_type=hotel&dest_id=4480704&checkin=2021-2-1;checkout=2021-2-2&selected_currency=USD;",
            "hotel_name": "Home2 Suites By Hilton San Francisco Airport North",
            "hotel_id": "4480704",
            "ext_data": {
                "scan_longitude": -122.3992458,
                "scan_latitude": 37.65710296,
                "scan_occupancy_from_scan": 4,
                "scan_checkin_from_scan": None,
                "scan_checkout_from_scan": None,
                "taxes": '{ "TAX":"14.70", "City tax":"4.01"}'
            },
            "cancellation_policy": "Guests:",
            "number_of_guests": 4,
            "breakfast": "included",
            "shown_price": {
                "King Studio Suite - Hearing Accessible/Non-Smoking": "113.05",
                "King Studio Suite - Non Smoking": "90",
                "King Room - Mobility/Hearing Accessible - Non-Smoking": "115.05",
                "Queen Suite with Two Queen Beds - Non-Smoking": "112.05"
            },
            "currency": "USD",
            "net_price": {
                "King Studio Suite - Hearing Accessible/Non-Smoking": "113.05",
                "King Studio Suite - Non Smoking": "90",
                "King Room - Mobility/Hearing Accessible - Non-Smoking": "115.05",
                "Queen Suite with Two Queen Beds - Non-Smoking": "112.05"
            },
            "availability": "",
            "ci_date": "2021-02-01",
            "co_date": "2021-02-02",
            "los": 1,
            "site_name": "booking",
            "site_type": "ota",
            "shown_currency": "USD",
            "pos": "US",
            "snapshot_url": [
                "https://storage.googleapis.com/prod-public-snapshots.gcphosts.net/booking_hotel/202101/60041b12fef076f02f58a8a5%253A%253A27-968117.png"
            ]
        }
    ]
}

# Extract the required details from the input data
assignment = input_data["assignment_results"][0]
prices = assignment["shown_price"]
net_prices = assignment["net_price"]
taxes_data = json.loads(assignment["ext_data"]["taxes"])

# Variables to store the cheapest price and corresponding room
cheapest_room = None
cheapest_price = float('inf')

# Loop through each room and its price to find the cheapest one
for room_type, price in prices.items():
    price_float = float(price)
    if price_float < cheapest_price:
        cheapest_price = price_float
        cheapest_room = room_type

# Calculate total taxes
total_taxes = float(taxes_data["TAX"]) + float(taxes_data["City tax"])

# Generate total price for each room (Net price + taxes)
total_prices = {}
for room_type, net_price in net_prices.items():
    total_net_price = float(net_price)
    total_price = total_net_price + total_taxes
    total_prices[room_type] = total_price

# Prepare the output
output_data = {
    "cheapest_room": cheapest_room,
    "cheapest_price": cheapest_price,
    "number_of_guests": assignment["number_of_guests"],
    "total_prices": total_prices
}

# Write the output to a file
with open('hotel_booking_output.txt', 'w') as file:
    file.write(f"Cheapest Room: {cheapest_room}\n")
    file.write(f"Cheapest Price: ${cheapest_price}\n")
    file.write(f"Number of Guests: {assignment['number_of_guests']}\n\n")
    file.write("Total Price for All Rooms:\n")
    for room_type, total_price in total_prices.items():
        file.write(f"{room_type}: ${total_price:.2f}\n")

# Print statements to verify results
print(f"Cheapest Room: {cheapest_room}")
print(f"Cheapest Price: ${cheapest_price}")
print(f"Total Prices (Net + Taxes):")
for room_type, total_price in total_prices.items():
    print(f"{room_type}: ${total_price:.2f}")
