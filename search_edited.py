import heapq
import math
import time
import utility
import predict_model.weights_to_prediction as predict
import copy

DIST_COEFF = 1.0
RouteDistance = []
Route = ()
TempStorage = ""



"""
1 degree latitude = 69 miles
1 degree longitude = 54.6 miles
"""




def time_at_location(locations,preferences,init_pref,prev_pref):
    day_n_preference = max((day_n-1_preference + initial_preference)/2 - day_n-1_visit_number**2, 0)
    pref_list = []
    for i in range(len(preferences)):
        pref_list.append(max( (init_pref+prev_pref)/2 - locations[preferences[i]] **2   ,0 )   )
    while (len(pref_list) < 10):
        pref_list.append(5)
    prediction = predict(prev_pref)
    prev_pref = pref_list
    return prediction

def distance(locationA, locationB):
    return (math.sqrt(((locationA.latitude - locationB.latitude) * 69) ** 2 \
                      + ((locationA.longitude - locationB.longitude) * 54.6) ** 2)) * DIST_COEFF

def total_preference(roadtrip, locations, edges):
	total_pref = 0.000

	# Add up the preferences of the locations
	for loc in roadtrip:
		total_pref += locations[loc].preference

	# Add up the preferences of the edges
	for i in range(len(roadtrip) - 1):
		current_loc, next_loc = roadtrip[i], roadtrip[i + 1]

		# Find the correct edge and add its preference
		for edge in edges[current_loc]:
			if edge.other_city(current_loc) == next_loc:
				total_pref += edge.preference
				break

	# Since this is a round-trip, the start location only have one preference value
	total_pref = total_pref - locations[roadtrip[0]].preference
	return total_pref


def time_estimate(roadtrip, locations, edges):
	total_time = 0
	# Iterate through the road trip, assuming roadtrip is a list of location names in order
	for i, location_name in enumerate(roadtrip):
		# Add time spent at each location
		total_time += time_at_location(locations[location_name].preference)

		# Add time spent on each edge, if it's not the last location
		if i < len(roadtrip) - 1:
			next_location = roadtrip[i + 1]

			# Finding the correct edge object
			edge_obj = None
			for edge in edges[location_name]:
				if edge.other_city(location_name) == next_location:
					edge_obj = edge
					break

			# Add base travel time
			total_time += edge_obj.length / 65
			# Add additional time due to edge preference
			total_time += time_at_location(edge_obj.preference)
	total_time = total_time - time_at_location(locations[roadtrip[0]].preference)
	return total_time




def route_search(startLoc, locations, edges, days, drivingHour, x_mph, preferences, resultFile):
    while (len(preferences) < 10):
        prefences.append(5)
    initial_preference = copy.deepcopy(preferences)
    prev_day_preference = preferences
    #start_time = time.time()
    file = open(resultFile, 'w')
    # check validity
    if not (startLoc in locations.keys()):
        print('ERROR: Start location not recognized')
        exit()
    
    # frontier: prioity queue of tuple (eval_score,list of list of locations traveled by day (duplicate location if in two days),
    #                                             list of distance_traveled by day,total preference score)
    # eval_score: total preference (location + edge) / time used 
    # miles_traveled need to be calculated manually from list of locations
    frontier = [(0, [[startLoc]], [0], 0)]
    heapq.heapify(frontier)
    # goalness: dictionary, key = city name, value = maximum eval_score
    # goalness = dict()

    Solution_Label = 0
    #sumUserTime = 0

    while len(frontier) > 0:
        # get info from first one in queue and remove it
        curr_visit = frontier[0][1]
        curr_loc = curr_visit[-1]
        curr_eval_score = frontier[0][0]
        curr_miles = frontier[0][2]
        curr_hours = frontier[0][3]


        heapq.heappop(frontier)
        #print(curr_visit,curr_hours)


        # TODO: check if a valid path is found and check user prompt for anytime search
        # TODO: Modify output!

        if curr_loc == startLoc and len(curr_visit) > 1:
            Solution_Label += 1

            # Do the standard format Output
            RouteDistance.append(curr_eval_score)

            tempEdgeName = []
            tempEdgeLength = []
            pathCost = 0

            file.write("Solution label: {}  ".format(Solution_Label) + "{}  ".format(curr_visit[0]) + "{:.1f}  ".format(maxTime) + "{:.1f}\n".format(x_mph))
            print("Solution label: {}  ".format(Solution_Label) + "{}  ".format(curr_visit[0]) + "{:.1f}  ".format(maxTime) + "{:.1f}".format(x_mph))
            i = 0
            while i < len(curr_visit) - 1:
                avail_edges = edges[curr_visit[i]]
                for a in avail_edges:
                    if curr_visit[i + 1] == (a.other_city(curr_visit[i])):


                        tempEdgeLength.append(a)
                        tempEdgeName.append(a)

                        pathCost += a.length
                        loc = distance(locations[curr_visit[i+1]],locations[curr_visit[-1]])

                        file.write("{}.".format(i + 1) + " {:<15}".format(curr_visit[i]) + " {:<15}".format(curr_visit[i+1]) + " {:<40}".format(
                            a.name) + " {:>5.3f}".format(
                            a.preference) + "{:>5.1f}hours".format((a.length/x_mph)+ time_at_location(a.preference))+
                            "  {:>5.3f}".format(locations[curr_visit[i+1]].preference) + " {:>5.1f}hours\n".format(time_at_location(locations[curr_visit[i+1]].preference)))
                        print("{}.".format(i + 1) + " {:<15}".format(curr_visit[i]) + " {:<15}".format(curr_visit[i+1]) + " {:<40}".format(
                            a.name) + " {:>5.3f}".format(
                            a.preference) + "{:>5.1f}hours".format((a.length/x_mph)+ time_at_location(a.preference))+
                            "  {:>5.3f}".format(locations[curr_visit[i+1]].preference) + " {:>5.1f}hours".format(time_at_location(locations[curr_visit[i+1]].preference)))
                i += 1
            totalPreference = total_preference(curr_visit, locations, edges)
            totalTimeCost = time_estimate(curr_visit, locations, edges)
            file.write("{}  ".format(curr_visit[0]) + "{:.3f}  ".format(totalPreference) + "{:.1f}miles  ".format(pathCost) + "{:.1f}hours".format(totalTimeCost) + "\n")
            print("{}  ".format(curr_visit[0]) + "{:.3f}  ".format(totalPreference) + "{:.1f}miles  ".format(pathCost) + "{:.1f}hours".format(totalTimeCost) + "\n")

            # *****WARNING***** FOR TEST PURPOSE ONLY, WILL EVENTUALLY BE
            # user_start_time = time.time()
            UserInput = input("Do you want to find a alternate route? Y/N \n")
            # user_end_time = time.time()
            # elapsed_time = user_end_time - user_start_time
            # sumUserTime += elapsed_time
            file.write("\n")

            if UserInput.lower() == "y" or UserInput.lower() == "yes":
                continue
            elif UserInput.lower() == "n" or UserInput.lower() == "no":
                break


        # check if a location is visited, if yes, stop further search 
        # *****************************************************************************
        # ** Here we choose to require a road trip visit any location at most once   **
        # *****************************************************************************
        if curr_visit.index(curr_loc) != len(curr_visit)-1:
            continue

        # see if we went too far and can't go home on time (to take the next AI class)
        # The restriant is lenient. It is possible to reduce branches furthermore,
        # but it need longer time to search a return route every time a branch is created
        # and probably would exceed the running time reduced from cutting branches
        if distance(locations[curr_loc],locations[startLoc]) / x_mph + curr_hours > maxTime:
            continue

        # get edges from the location
        if not (curr_loc in edges.keys()):
            print('WARNING: Visited a non-connected location')
            continue
        avail_edges = edges[curr_loc]

        # add new locations to the queue
        next_visits = []

        for edge in avail_edges:
            new_loc = edge.other_city(curr_loc)
            new_miles = curr_miles + edge.length
            new_edge_time = edge.length / x_mph + time_at_location(edge.preference)
            new_loc_time = time_at_location(locations[new_loc].preference)
            new_hours = curr_hours + new_edge_time + new_loc_time
            curr_preference = curr_eval_score * curr_hours
            new_preference = curr_preference + edge.preference + locations[new_loc].preference
            new_eval_score = new_preference / new_hours
            new_visit = curr_visit + [new_loc]
            heapq.heappush(frontier, (new_eval_score, new_visit, new_miles, new_hours))


    if len(RouteDistance) == 0:
        file.write("No route found!\n")
        # end_time = time.time()
        # elapsed_time = end_time - start_time - sumUserTime
        # file.write("\nElapsed search time: {:.4f} seconds".format(elapsed_time))
        return
    # Standard Output


    # ADD  a list of locations that were visited (checked for goalness) across the entirety of the anytime search (with duplicates removed).!!!!!!!!!!!!!!!!
    # file.write("Locations visited:\n")
    # for loc in goalness.keys():
        # file.write(loc+"  ")
    # end_time = time.time()
    # elapsed_time = end_time - start_time - sumUserTime
    # file.write("\nElapsed search time: {:.4f} seconds".format(elapsed_time))
