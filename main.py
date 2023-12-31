import utility
import search_edited as search
import numpy
import sys

"""
*******************************************************************************************
** total_preference(roadtrip) and time_estimate(roadtrip,x) are implemented in search.py **
*******************************************************************************************

1 degree latitude = 69 miles
1 degree longitude = 54.6 miles
locations: Dictionary, where key = city name, value = Location class object
Location class object: city name, longitude, latitude
edges: Dictionary, key = city name, value = list of connected Edge class object
Edge class object: edge name, city A, city B, length


"""




# Start out road trip!
def RoadTrip(startLoc, LocFile, EdgeFile, AttrFile, days, drivingHour, x_mph, preferences, resultFile):
	locations = utility.read_locations(LocFile)
	edges =	utility.read_edges(EdgeFile)
	utility.read_attr(AttrFile,locations)
	search.route_search(startLoc, locations, edges, days, drivingHour, x_mph, preferences, resultFile)

if __name__ == '__main__':
	if (len(sys.argv) < 5):
		print('Usage: main.py LocationFile EdgeFile OutputFile StartLocation')
		exit(1)

	LocFile = sys.argv[1].strip()
	EdgeFile = sys.argv[2].strip()
	resultFile = sys.argv[3].strip()
	startLoc = sys.argv[4].strip()
	AttrFile = 'attractions.csv'
	days = int(input('Please enter days of road trip: \n').strip())
	print(days)
	drivingHour = int(input('Please enter maximum hours per day: \n').strip())
	print(drivingHour)
	x_mph = int(input('Please enter your expected driving speed: \n').strip())
	print(x_mph)

	preferences = []
	while len(preferences) < 10:
		curr_pref = input('Please enter your theme preference from most preferred first (%d/10 entered), enter stop to auto-fill the rest: \n'%len(preferences))
		print(curr_pref)
		curr_pref = curr_pref.strip().split()
		stopLoop = False
		i = 0
		for single in curr_pref:
			if single.strip().lower() == 'stop':
				stopLoop = True
				break
			preferences.append([single.strip().lower(),10-i//2]) 
		if stopLoop:
			break
	# print(preferences)

	RoadTrip(startLoc, LocFile, EdgeFile, AttrFile, days, drivingHour, x_mph, preferences, resultFile)


