import numpy as np

class Facet:
	def __init__(self,a,b):
		self.id = a			# Triangle's id
		self.pvoid = None	# Parent void
		self.ccw = True		# Are vertices arranged in counter-clockwise order?
		self.vertices = b	# List of numpy arrays each representing a vertex
		self.vecinos = {}	# This facet's neighbours and its shared border
		self.boundary = False	# Is this facet in the edge of the convex hull?
		self.used = False	# Does this facet belong to a void?
		self.edges = self.__sorted_edges__()	# Edge lengths
		self.area = self.__area__()
		self.centroid = self.__centroid__()
		self.children = []	# Facets sharing their longest edge with this facet
		self.slml = None	# Neighbour which the second longest edge is shared with
		self.lsl = {}		# Neighbour dictionary containing those with which an edge longer than threshold is shared
	def isUsed(self):
		return self.used
	def setUsed(self):
		self.used = True
	def isBoundary(self):
		return self.boundary
	def setBoundary(self):
		self.boundary = True
	def __sorted_edges__(self):
		v = self.vertices
		edges = map(np.linalg.norm, [v[0] - v[1], v[1] - v[2], v[2] - v[0]])
		edges.sort()
		return edges
	def __area__(self):
		v = self.vertices
		ans = np.cross(v[1] - v[0], v[2] - v[0])
		self.ccw = ans >= 0
		if self.ccw:
			return 0.5 * ans
		else:
			return -0.5 * ans
	def __centroid__(self):
		v = self.vertices
		return np.sum(v, axis=0) / 3.0
