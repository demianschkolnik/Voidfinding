
class Void:
	def __init__(self, facets, boundary=None):
		self.facets = facets
		for facet in facets:
			facet.pvoid = self
		self.area = sum(map(lambda facet: facet.area, facets))
		if boundary == None:
			self.boundary = True in map(lambda facet: facet.isBoundary(), facets)
		else:
			self.boundary = boundary
		self.cx = sum(facet.centroid[0] * facet.area for facet in facets)
		self.cy = sum(facet.centroid[1] * facet.area for facet in facets)
	
	def addFacet(self, facet):
		self.facets.append(facet)
		facet.pvoid = self
		self.area += facet.area
		if facet.isBoundary():
			self.boundary = True
		self.cx += facet.centroid[0] * facet.area
		self.cy += facet.centroid[1] * facet.area
	
	def addVoid(self, void):
		self.facets += void.getFacets()
		for facet in void.getFacets():
			facet.pvoid = self
		self.area += void.getArea()
		if void.isBoundary():
			self.boundary = True
		self.cx += void.cx
		self.cy += void.cy
	
	def isBoundary(self):
		return self.boundary
	
	def getFacets(self):
		return self.facets
	
	def getArea(self):
		return self.area
	
	def getCentroid(self):
		return (self.cx/self.area, self.cy/self.area)
