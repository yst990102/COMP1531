"""Given two Latitude/Longitude coordinates, find out what time I would
arrive at my destination if I left now. Assume I travel at the local country's highway speed"""

from geopy.distance import geodesic 
  
latNow = input("Please enter your current latitude: ")
lngNow = input("Please enter your current longitude: ")

latDest = input("Please enter your destination latitude: ")
lngDest = input("Please enter your destination longitude: ")

def findDistanceBetween(latA, lngA, latB, lngB):
	return geodesic((latA, lngA), (latB, lngB)).km

# Seconds taken
def timeTaken(latA, lngA, latB, lngB):
	distance = findDistanceBetween(latA, lngA, latB, lngB)
	speed = 100
	return distance / 100 * 60 * 60;

tt = timeTaken(latNow, lngNow, latDest, lngDest)
print(f"Time taken is {tt} seconds")

