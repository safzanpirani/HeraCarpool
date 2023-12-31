# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tOzhMWCRkmSIBlyNYijiz420P4J7T2V_
"""

import hashlib
import geohash

# Initialize dictionaries to store user data and available rides
users = {}
rides = {}

# Function to create a user account
def register_user(user_id, username, latitude, longitude):
    users[user_id] = {
        'username': username,
        'latitude': latitude,
        'longitude': longitude,
        'geohash': geohash.encode(latitude, longitude, precision=5)  # Precision can be adjusted
    }
    print(f"User {username} registered.")

# Function to create a ride offer
def create_ride(ride_id, driver_id, origin_lat, origin_lon, destination_lat, destination_lon, available_seats):
    rides[ride_id] = {
        'driver_id': driver_id,
        'origin_lat': origin_lat,
        'origin_lon': origin_lon,
        'destination_lat': destination_lat,
        'destination_lon': destination_lon,
        'available_seats': available_seats,
        'geohash': geohash.encode(origin_lat, origin_lon, precision=5)  # Precision can be adjusted
    }
    print(f"Ride {ride_id} created by user {users[driver_id]['username']}.")

# Function to find rides for a user based on geohash
def find_rides(user_id):
    user = users[user_id]
    user_geohash = user['geohash']
    matching_rides = []

    for ride_id, ride in rides.items():
        if (
            ride['geohash'] == user_geohash  # Rides with the same geohash
            and ride['driver_id'] != user_id  # Exclude user's own rides
            and ride['available_seats'] > 0     # Check for available seats
        ):
            matching_rides.append(ride_id)

    return matching_rides

# Function to join a ride
def join_ride(user_id, ride_id):
    if ride_id in rides:
        ride = rides[ride_id]
        if ride['available_seats'] > 0:
            ride['available_seats'] -= 1
            print(f"User {users[user_id]['username']} joined ride {ride_id}.")
        else:
            print(f"Ride {ride_id} is full.")
    else:
        print(f"Ride {ride_id} not found.")

# Example usage:
if __name__ == "__main__":
    # Register users
    register_user(1, 'Alice', 37.7749, -122.4194)
    register_user(2, 'Bob', 37.8049, -122.4054)
    register_user(3, 'Charlie', 37.7849, -122.4144)

    # Create ride offers
    create_ride(101, 1, 37.7749, -122.4194, 37.7049, -122.3054, 3)
    create_ride(102, 2, 37.8049, -122.4054, 37.7449, -122.3654, 2)
    create_ride(103, 3, 37.7849, -122.4144, 37.7149, -122.3244, 1)

    # Find and join rides for users
    for user_id in [1, 2, 3]:
        matching_rides = find_rides(user_id)
        if matching_rides:
            print(f"Matching rides for {users[user_id]['username']}: {matching_rides}")
            join_ride(user_id, matching_rides[0])
        else:
            print(f"No matching rides for {users[user_id]['username']}.")

    # Check the updated ride information
    print("\nUpdated ride information:")
    for ride_id, ride in rides.items():
        print(f"Ride {ride_id}: {ride}")

pip install python-geohash

from geopy.geocoders import Nominatim
import geohash

# Initialize dictionaries to store user and driver data
users = {}
drivers = {}
rides = {}

geolocator = Nominatim(user_agent="carpooling_app")

# Function to register a user
def register_user(user_id):
    username = input("Enter your username: ")
    address = input("Enter your address: ")
    location = geolocator.geocode(address)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        users[user_id] = {
            'username': username,
            'latitude': latitude,
            'longitude': longitude,
            'geohash': geohash.encode(latitude, longitude, precision=5)  # Precision can be adjusted
        }
        print(f"User {username} registered.")
    else:
        print("Location not found. Please check the address.")

# Function to register a driver
def register_driver(driver_id):
    drivername = input("Enter your driver name: ")
    address = input("Enter your driver's address: ")
    available_seats = int(input("Enter the number of available seats: "))
    location = geolocator.geocode(address)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        drivers[driver_id] = {
            'drivername': drivername,
            'latitude': latitude,
            'longitude': longitude,
            'available_seats': available_seats,
            'geohash': geohash.encode(latitude, longitude, precision=5)  # Precision can be adjusted
        }
        print(f"Driver {drivername} registered with {available_seats} available seats.")
    else:
        print("Location not found. Please check the address.")

# Function to create a ride offer
def create_ride(ride_id, driver_id):
    if driver_id in drivers:
        print("Enter ride details:")
        origin_address = input("Origin address: ")
        destination_address = input("Destination address: ")
        origin_location = geolocator.geocode(origin_address)
        destination_location = geolocator.geocode(destination_address)
        if origin_location and destination_location:
            origin_lat = origin_location.latitude
            origin_lon = origin_location.longitude
            destination_lat = destination_location.latitude
            destination_lon = destination_location.longitude
            rides[ride_id] = {
                'driver_id': driver_id,
                'origin_lat': origin_lat,
                'origin_lon': origin_lon,
                'destination_lat': destination_lat,
                'destination_lon': destination_lon,
            }
            print(f"Ride {ride_id} created by driver {drivers[driver_id]['drivername']} from {origin_address} to {destination_address}.")
        else:
            print("Location not found. Please check the addresses.")
    else:
        print(f"Driver with ID {driver_id} not found.")

# Function to find rides for a user based on geohash
def find_rides(user_id):
    if user_id in users:
        user = users[user_id]
        user_geohash = user['geohash']
        matching_rides = []

        for ride_id, ride in rides.items():
            if (
                ride['origin_lat'] == user['latitude']  # Same origin location
                and ride['driver_id'] not in user.get('joined_rides', [])  # Exclude rides user has already joined
            ):
                matching_rides.append(ride_id)

        return matching_rides
    else:
        print(f"User {user_id} not found.")

# Function to join a ride
def join_ride(user_id, ride_id):
    if user_id in users and ride_id in rides:
        user = users[user_id]
        ride = rides[ride_id]
        if ride['driver_id'] not in user.get('joined_rides', []):
            user.setdefault('joined_rides', []).append(ride['driver_id'])
            print(f"User {user['username']} joined ride {ride_id}.")
        else:
            print(f"User {user['username']} has already joined this ride.")
    else:
        print(f"User {user_id} or ride {ride_id} not found.")

# Example usage:
if __name__ == "__main__":
    # Register users and drivers
    register_user(1)
    register_user(2)
    register_driver(101)
    register_driver(102)

    # Create ride offers
    create_ride(201, 101)
    create_ride(202, 102)

    # Find and join rides for users
    for user_id in [1, 2]:
        matching_rides = find_rides(user_id)
        if matching_rides:
            print(f"Matching rides for {users[user_id]['username']}: {matching_rides}")
            join_ride(user_id, matching_rides[0])
        else:
            print(f"No matching rides for {users[user_id]['username']}.")

    # Check the updated ride information
    print("\nUpdated ride information:")
    for ride_id, ride in rides.items():
        print(f"Ride {ride_id}: {ride}")

pip install geopy

import geohash

# Initialize dictionaries to store user and driver data
users = {}
drivers = {}
rides = {}

# Function to register a user
def register_user(user_id, username):
    latitude = float(input(f"Enter latitude for user {username}: "))
    longitude = float(input(f"Enter longitude for user {username}: "))
    users[user_id] = {
        'username': username,
        'latitude': latitude,
        'longitude': longitude,
        'geohash': geohash.encode(latitude, longitude, precision=5)  # Precision can be adjusted
    }
    print(f"User {username} registered.")

# Function to register a driver
def register_driver(driver_id, drivername):
    latitude = float(input(f"Enter latitude for driver {drivername}: "))
    longitude = float(input(f"Enter longitude for driver {drivername}: "))
    available_seats = int(input(f"Enter available seats for driver {drivername}: "))
    drivers[driver_id] = {
        'drivername': drivername,
        'latitude': latitude,
        'longitude': longitude,
        'available_seats': available_seats,
        'geohash': geohash.encode(latitude, longitude, precision=5)  # Precision can be adjusted
    }
    print(f"Driver {drivername} registered with {available_seats} available seats.")

# Function to create a ride offer
def create_ride(ride_id, driver_id):
    if driver_id in drivers:
        origin_lat = float(input("Enter origin latitude: "))
        origin_lon = float(input("Enter origin longitude: "))
        destination_lat = float(input("Enter destination latitude: "))
        destination_lon = float(input("Enter destination longitude: "))
        rides[ride_id] = {
            'driver_id': driver_id,
            'origin_lat': origin_lat,
            'origin_lon': origin_lon,
            'destination_lat': destination_lat,
            'destination_lon': destination_lon,
        }
        print(f"Ride {ride_id} created by driver {drivers[driver_id]['drivername']}.")

# Example usage:
if __name__ == "__main__":
    # Register users and drivers
    register_user(1, 'Alice')
    register_user(2, 'Bob')
    register_driver(101, 'Charlie')
    register_driver(102, 'David')

    # Create ride offers
    create_ride(201, 101)
    create_ride(202, 102)

    # Check the updated user, driver, and ride information
    print("\nUpdated user information:")
    for user_id, user in users.items():
        print(f"User {user_id}: {user}")

    print("\nUpdated driver information:")
    for driver_id, driver in drivers.items():
        print(f"Driver {driver_id}: {driver}")

    print("\nUpdated ride information:")
    for ride_id, ride in rides.items():
        print(f"Ride {ride_id}: {ride}")

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Your Python backend code for user registration, driver registration, and ride creation should be here.

from geopy.geocoders import Nominatim
import geohash

# Initialize dictionaries to store user and driver data
users = {}
drivers = {}
rides = {}

geolocator = Nominatim(user_agent="carpooling_app")

# Function to register a user
def register_user(user_id):
    username = input("Enter your username: ")
    address = input("Enter your address: ")
    location = geolocator.geocode(address)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        users[user_id] = {
            'username': username,
            'latitude': latitude,
            'longitude': longitude,
            'geohash': geohash.encode(latitude, longitude, precision=5)  # Precision can be adjusted
        }
        print(f"User {username} registered.")
    else:
        print("Location not found. Please check the address.")

# Function to register a driver
def register_driver(driver_id):
    drivername = input("Enter your driver name: ")
    address = input("Enter your driver's address: ")
    available_seats = int(input("Enter the number of available seats: "))
    location = geolocator.geocode(address)
    if location:
        latitude = location.latitude
        longitude = location.longitude
        drivers[driver_id] = {
            'drivername': drivername,
            'latitude': latitude,
            'longitude': longitude,
            'available_seats': available_seats,
            'geohash': geohash.encode(latitude, longitude, precision=5)  # Precision can be adjusted
        }
        print(f"Driver {drivername} registered with {available_seats} available seats.")
    else:
        print("Location not found. Please check the address.")

# Function to create a ride offer
def create_ride(ride_id, driver_id):
    if driver_id in drivers:
        print("Enter ride details:")
        origin_address = input("Origin address: ")
        destination_address = input("Destination address: ")
        origin_location = geolocator.geocode(origin_address)
        destination_location = geolocator.geocode(destination_address)
        if origin_location and destination_location:
            origin_lat = origin_location.latitude
            origin_lon = origin_location.longitude
            destination_lat = destination_location.latitude
            destination_lon = destination_location.longitude
            rides[ride_id] = {
                'driver_id': driver_id,
                'origin_lat': origin_lat,
                'origin_lon': origin_lon,
                'destination_lat': destination_lat,
                'destination_lon': destination_lon,
            }
            print(f"Ride {ride_id} created by driver {drivers[driver_id]['drivername']} from {origin_address} to {destination_address}.")
        else:
            print("Location not found. Please check the addresses.")
    else:
        print(f"Driver with ID {driver_id} not found.")

# Function to find rides for a user based on geohash
def find_rides(user_id):
    if user_id in users:
        user = users[user_id]
        user_geohash = user['geohash']
        matching_rides = []

        for ride_id, ride in rides.items():
            if (
                ride['origin_lat'] == user['latitude']  # Same origin location
                and ride['driver_id'] not in user.get('joined_rides', [])  # Exclude rides user has already joined
            ):
                matching_rides.append(ride_id)

        return matching_rides
    else:
        print(f"User {user_id} not found.")

# Function to join a ride
def join_ride(user_id, ride_id):
    if user_id in users and ride_id in rides:
        user = users[user_id]
        ride = rides[ride_id]
        if ride['driver_id'] not in user.get('joined_rides', []):
            user.setdefault('joined_rides', []).append(ride['driver_id'])
            print(f"User {user['username']} joined ride {ride_id}.")
        else:
            print(f"User {user['username']} has already joined this ride.")
    else:
        print(f"User {user_id} or ride {ride_id} not found.")
# Example usage:
if __name__ == "__main__":
    # Register users and drivers
    register_user(1)
    register_user(2)
    register_driver(101)
    register_driver(102)

    # Create ride offers
    create_ride(201, 101)
    create_ride(202, 102)

    # Find and join rides for users
    for user_id in [1, 2]:
        matching_rides = find_rides(user_id)
        if matching_rides:
            print(f"Matching rides for {users[user_id]['username']}: {matching_rides}")
            join_ride(user_id, matching_rides[0])
        else:
            print(f"No matching rides for {users[user_id]['username']}.")

    # Check the updated ride information
    print("\nUpdated ride information:")
    for ride_id, ride in rides.items():
        print(f"Ride {ride_id}: {ride}")


# Example route for rendering the HTML page
@app.route("/")
def index():
    return render_template("ui.html")

# Example route for user registration
@app.route("/register_user", methods=["POST"])
def register_user():
    # Implement user registration logic here
    data = request.get_json()
    # Your user registration logic here
    response = {"status": "success"}
    return jsonify(response)

# Example route for driver registration
@app.route("/register_driver", methods=["POST"])
def register_driver():
    # Implement driver registration logic here
    data = request.get_json()
    # Your driver registration logic here
    response = {"status": "success"}
    return jsonify(response)

# Example route for ride creation
@app.route("/create_ride", methods=["POST"])
def create_ride():
    # Implement ride creation logic here
    data = request.get_json()
    # Your ride creation logic here
    response = {"status": "success"}
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)

def calculate_fare(distance_traveled, occupancy):
    BASE_FARE = 25.0  # Replace with your base fare
    DISTANCE_RATE = 5.0  # Replace with your rate per kilometer or mile
    OCCUPANCY_MULTIPLIER = 1.0  # Replace with your occupancy multiplier

    # Calculate the fare based on the formula
    if occupancy>0:
      distance_fare = distance_traveled * DISTANCE_RATE
      fare = (BASE_FARE + distance_fare) * OCCUPANCY_MULTIPLIER / occupancy
    else:
      print("Enter valid occupancy")
    return fare

# Example usage:
distance_traveled = int(input("Enter the distance(in KM)"))  # Example distance in kilometers
occupancy =  int(input("Enter the occupancy")) # Example occupancy

fare = calculate_fare(distance_traveled, occupancy)
print(f"Total Fare: ₹{fare:.2f}")

