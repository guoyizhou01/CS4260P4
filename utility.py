
import csv

class Location:
	def __init__(self,city,latitude,longitude):
		self.city = city
		self.latitude = latitude
		self.longitude = longitude
		self.preference = 0.00
		self.themes = dict()

	def __eq__(self,other):
		if self.city != other.city:
			return False
		if abs(self.latitude-other.latitude) > 0.0001:
			return False
		if abs(self.longitude-other.longitude) > 0.0001:
			return False
		return True

	def __str__(self):
		return "City: %s, Latitude: %.4f, Longitude: %.4f" % (self.city,self.latitude,self.longitude) + '\n      {}'.format(self.themes)

	def assign_preference(self, pref):
		self.preference = pref

	def add_theme(self,theme):
		if not (theme in self.themes.keys()):
			self.themes[theme] = 0
		self.themes[theme] = self.themes[theme] + 1

	def get_theme(self,theme):
		if not (theme in self.themes.keys()):
			return 0
		return self.themes[theme]


class Edge:
	def __init__(self,name,cityA,cityB,length):
		self.name = name
		self.cityA = cityA
		self.cityB = cityB
		self.length = length
		self.preference = 0.00

	def __eq__(self,other):
		if not ( self.name == other.name and self.cityA == other.cityA and self.cityB == other.cityB ):
			return False
		if abs(self.length-other.length) > 0.0001:
			return False
		return True

	def __str__(self):
		return "Edge: %s, From: %s, To: %s, Length: %.1f" % (self.name,self.cityA,self.cityB,self.length)

	def assign_preference(self, pref):
		self.preference = pref

	def other_city(self,cityName):
		if cityName == self.cityA:
			return self.cityB
		if cityName == self.cityB:
			return self.cityA
		print('ERROR: input city not in edge')
		return 'ERROR'






def read_attr(AttrFile,all_locations):

	with open(AttrFile, mode ='r') as file:
	
	# reading the CSV file
		csvFile = csv.reader(file)
		first_line = True
	# reading the contents of the CSV file
		for lines in csvFile:
			# check for non-related infomation
			# print(lines)
			if not (lines[1].strip() in all_locations.keys()):
				continue
			for theme in lines[3].strip().split(','):
				all_locations[lines[1].strip()].add_theme(theme.strip().lower().replace(" ",""))
	return all_locations


def read_locations(LocFile):

	all_locations = dict()

	# source for reading CSV file: https://www.geeksforgeeks.org/reading-csv-files-in-python/

	# opening the CSV file
	with open(LocFile, mode ='r') as file:
	
	# reading the CSV file
		csvFile = csv.reader(file)
		first_line = True
	# reading the contents of the CSV file
		for lines in csvFile:
			# check for non-related infomation
			if lines[0] == 'Location Label' or lines[0] == '' or first_line:
				first_line = False
				continue
			curr_location = Location(lines[0], float(lines[1]), float(lines[2]))

			# check for duplicate and add to dictionary
			if all_locations.get(curr_location.city) == None:
				all_locations[curr_location.city] = curr_location
			else:
				print('ERROR: Duplicate City')

	return all_locations


def read_edges(EdgeFile):

	all_edges = dict()

	# source for reading CSV file: https://www.geeksforgeeks.org/reading-csv-files-in-python/

	# opening the CSV file
	with open(EdgeFile, mode ='r') as file:
	
	# reading the CSV file
		csvFile = csv.reader(file)
		first_line = True
	# reading the contents of the CSV file
		for lines in csvFile:
			# check for non-related infomation
			if lines[0] == 'edgeLabel' or lines[0] == '' or first_line:
				first_line = False
				continue
			curr_edge_1 = Edge(lines[0], lines[1], lines[2], float(lines[3]))
			curr_edge_2 = Edge(lines[0], lines[1], lines[2], float(lines[3]))
			# add edge for both cities

			if all_edges.get(curr_edge_1.cityA) == None:
				all_edges[curr_edge_1.cityA] = []
			if curr_edge_1 in all_edges[curr_edge_1.cityA]:
				print('ERROR: Duplicate Edge')
			else:
				all_edges[curr_edge_1.cityA].append(curr_edge_1)

			if all_edges.get(curr_edge_2.cityB) == None:
				all_edges[curr_edge_2.cityB] = []
			if curr_edge_2 in all_edges[curr_edge_2.cityB]:
				print('ERROR: Duplicate Edge')
			else:
				all_edges[curr_edge_2.cityB].append(curr_edge_2)
			if curr_edge_2.length > 200:
				print('WARNING: Edge %s (%.1f miles) longer than 200 miles!'\
					%(curr_edge_2.name,curr_edge_2.length))

	return all_edges

if __name__ == '__main__':
	all_locations = read_locations('Locations_small.csv')
	all_edges = read_edges('Edges_small.csv')
	read_attr('attractions.csv',all_locations)
	print('Locations:')
	for key in all_locations.keys():
		print('    ',all_locations[key])
	print()
	print('Edges:')
	for key in all_edges.keys():
		print('    ',key)
		for edge in all_edges[key]:
			print('        %s'%edge)
		

