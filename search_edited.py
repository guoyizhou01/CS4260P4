import heapq
import math
import time
import utility
import predict_model
import copy
import random

DIST_COEFF = 1.0
RouteDistance = []
Route = ()
TempStorage = ""



"""
1 degree latitude = 69 miles
1 degree longitude = 54.6 miles
"""


def convert_scale(number):
    if number == 0:
        return 1+3*random.random()
    elif number == 1:
        return 5
    else:
        return min(10,number+5)


def time_at_location(location,init_pref,prev_pref):
    # day_n_preference = max((day_n-1_preference + initial_preference)/2 - day_n-1_visit_number**2, 0)
    new_pref_list = []
    calculate_pref = []
    for i in range(len(init_pref)):
        # print(init_pref[i][1],prev_pref[i][1])
        new_pref_list.append([init_pref[i][0], max( (init_pref[i][1]+prev_pref[i][1])/2 - (location.get_theme(init_pref[i][0]) ** 1.5)   ,0 )  ] )
        calculate_pref.append(math.sqrt(prev_pref[i][1] * convert_scale(location.get_theme(prev_pref[i][0])) ))
    while (len(new_pref_list) < 10):
        new_pref_list.append(3)

    prediction = predict_model.weights_to_prediction(calculate_pref)
    # print(calculate_pref,prediction)
    prev_pref = new_pref_list
    return (prediction ** 2)*2


def distance(locationA, locationB):
    return (math.sqrt(((locationA.latitude - locationB.latitude) * 69) ** 2 \
                      + ((locationA.longitude - locationB.longitude) * 54.6) ** 2)) * DIST_COEFF


def is_in_matrix(matrix,a):
    count = 0
    for vec in matrix:
        for loc in vec:
            if a == loc:
                ++count
    return count > 1


def route_search(startLoc, locations, edges, days, drivingHour, x_mph, preferences, resultFile):
    while (len(preferences) < 10):
        prefences.append(5)
    init_pref = copy.deepcopy(preferences)
    prev_day_preference = copy.deepcopy(preferences)
    #start_time = time.time()
    file = open(resultFile, 'w')
    # check validity
    if not (startLoc in locations.keys()):
        print('ERROR: Start location not recognized')
        exit()
    time_at_loc_dict = dict()
    
    # frontier: prioity queue of tuple (eval_score,list of list of locations traveled by day (duplicate location if in two days),
    #                                             list of hours by day,total preference score)
    # eval_score: total preference (location + edge) / time used 
    # miles_traveled need to be calculated manually from list of locations
    frontier = [(0, [[startLoc]], [0], [0],prev_day_preference,[startLoc])]
    heapq.heapify(frontier)
    # goalness: dictionary, key = city name, value = maximum eval_score
    # goalness = dict()

    Solution_Label = 0
    #sumUserTime = 0

    while len(frontier) > 0:
        # print(frontier[0][1])
        # get info from first one in queue and remove it
        curr_visit = copy.deepcopy(frontier[0][1])
        curr_day = copy.deepcopy(curr_visit[-1])
        curr_loc = copy.deepcopy(curr_day[-1])
        curr_eval_score = copy.deepcopy(frontier[0][0])
        curr_miles = copy.deepcopy(frontier[0][2][-1])
        all_miles = copy.deepcopy(frontier[0][2])
        curr_hours = copy.deepcopy(frontier[0][3][-1])
        all_hours = copy.deepcopy(frontier[0][3])
        prev_pref = copy.deepcopy(frontier[0][4])
        visited = copy.deepcopy(frontier[0][5])


        heapq.heappop(frontier)
        if len(curr_visit) > days:
            continue

        if distance(locations[curr_loc],locations[startLoc])/x_mph*1.3+sum(all_hours) >days*drivingHour:
            continue 

        # TODO: check if a valid path is found and check user prompt for anytime search
        # TODO: Modify output!

        if curr_loc == startLoc and len(curr_visit[0]) > 1:
            if len(curr_visit) < max(days*0.7,days-2) or sum(all_hours) < len(curr_visit)*drivingHour*0.6:
                continue
            Solution_Label += 1
            prev_pref = init_pref
            # Do the standard format Output
            RouteDistance.append(curr_eval_score)

            tempEdgeName = []
            tempEdgeLength = []
            pathCost = 0

            totalTimeCost = 0
            totalThemes = 0

            file.write("Solution label: {}  {}  max_days:{}  max_hours_per_day:{}  mph:{}\n".format(Solution_Label,curr_visit[0][0],days,drivingHour,x_mph))
            print("Solution label: {}  {}  max_days:{}  max_hours_per_day:{}  mph:{}".format(Solution_Label,curr_visit[0][0],days,drivingHour,x_mph))
            day = 0
            while day < len(curr_visit):
                day = day + 1
                i = 0
                file.write("  Day %d:\n"%day)
                print("  Day %d:"%day)
                while i < len(curr_visit[day-1]) - 1:
                    avail_edges = edges[curr_visit[day-1][i]]
                    for a in avail_edges:
                        if curr_visit[day-1][i + 1] == (a.other_city(curr_visit[day-1][i])):


                            tempEdgeLength.append(a)
                            tempEdgeName.append(a)
                            for pair in init_pref:
                                totalThemes += locations[curr_visit[day-1][i+1]].get_theme(pair[0])

                            pathCost += a.length
                            # loc = distance(locations[curr_visit[day-1][i+1]],locations[curr_visit[day-1][-1]])
                            loc_time = time_at_location(locations[curr_visit[day-1][i+1]],init_pref,prev_pref)
                            file.write("    {}  {:<18} {:<18} {:<60}   {:>5.2f}hours  {:>5.2f}hours\n".format(i+1,curr_visit[day-1][i],curr_visit[day-1][i+1],a.name,\
                                (a.length/x_mph),loc_time))
                            print("    {}  {:<18} {:<18} {:<60}   {:>5.2f}hours  {:>5.2f}hours".format(i+1,curr_visit[day-1][i],curr_visit[day-1][i+1],a.name,\
                                (a.length/x_mph),loc_time))
                            totalTimeCost += (a.length/x_mph)+loc_time
                            break
                    i += 1
            
            # totalPreference = total_preference(curr_visit, locations, edges)
            # totalTimeCost = time_estimate(curr_visit, locations, edges)
            file.write("{:.1f} total miles  {} days  {:.2f} total hours  Total Themes satisfied: {} \n".format(pathCost,len(curr_visit),totalTimeCost,totalThemes))
            print("{:.1f} total miles  {} days  {:.2f} total hours  Total Themes satisfied: {} ".format(pathCost,len(curr_visit),totalTimeCost,totalThemes))

            # user_start_time = time.time()
            UserInput = input("Do you want to find a alternate route? Y/N \n")
            print(UserInput)
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
        # if is_in_matrix(curr_visit,curr_loc):
        #     continue
        if visited.index(curr_loc) != len(visited)-1:
            continue

        # see if we went too far and can't go home on time
        # The restriant is lenient. It is possible to reduce branches furthermore,
        # but it need longer time to search a return route every time a branch is created
        # and probably would exceed the running time reduced from cutting branches
        

        # get edges from the location
        if not (curr_loc in edges.keys()):
            print('WARNING: Visited a non-connected location')
            continue
        avail_edges = edges[curr_loc]

        # add new locations to the queue
        next_visits = []

        for edge in avail_edges:
            new_prev_pref = copy.deepcopy(prev_pref)
            new_loc = edge.other_city(curr_loc)
            # if new_loc in visited:
            #     continue
            new_edge_time = edge.length / x_mph
            new_loc_time = time_at_location(locations[new_loc],init_pref,new_prev_pref)
            new_all_hours = copy.deepcopy(all_hours)
            new_all_miles = copy.deepcopy(all_miles)
            new_all_visit = copy.deepcopy(curr_visit)
            new_visited = copy.deepcopy(visited)
            new_visited.append(new_loc)
            if new_edge_time + new_loc_time + curr_hours > drivingHour:
                new_all_visit.append([curr_loc])
                new_all_miles.append(0)
                new_all_hours.append(0)
            new_all_miles[-1] = new_all_miles[-1] + edge.length
            new_all_hours[-1] = new_all_hours[-1] + new_edge_time + new_loc_time 
            new_all_visit[-1].append(new_loc)
            new_hours = sum(all_hours) + new_edge_time + new_loc_time
            curr_preference = curr_eval_score * sum(all_hours)
            new_preference = curr_preference + edge.preference + locations[new_loc].preference
            new_eval_score = curr_eval_score - (new_loc_time/2)**2

            heapq.heappush(frontier, (new_eval_score, new_all_visit, new_all_miles, new_all_hours,prev_pref,new_visited))


    if len(RouteDistance) == 0:
        file.write("No route found!\n")
        return

