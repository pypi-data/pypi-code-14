from SeasObjects.common.PROPERTY import PROPERTY
from SeasObjects.common.RESOURCE import RESOURCE
from SeasObjects.common.Tools import Tools

from SeasObjects.model.Controllability import Controllability
from SeasObjects.model.Availability import Availability

from SeasObjects.model.Obj import Obj
from SeasObjects.rdf.Resource import Resource

import traceback


class Condition(Obj):

	def __init__(self, uri = None):
		Obj.__init__(self, uri)
		self.regexes = []
		self.ors = []
		self.ands = []
		self.setType(RESOURCE.SEAS_CONDITION)

	def serialize(self, model):
		resource = super(Condition, self).serialize(model)

		# regexes
		regexProp = model.createProperty( PROPERTY.SEAS_REGEX )
		for regex in self.regexes:
			resource.addProperty( regexProp, model.createLiteral(regex) )

		# ors
		orProp = model.createProperty( PROPERTY.SEAS_OR )
		for o in self.ors:
			resource.addProperty( orProp, o.serialize(model) )

		# ands
		andProp = model.createProperty( PROPERTY.SEAS_AND )
		for a in self.ands:
			resource.addProperty( andProp, a.serialize(model) )

		return resource


	def parse(self, resource):
		if isinstance(resource, Resource):
			if not resource.isAnon():
				condition = Condition(resource.toString())
			else:
				condition = Condition()
			condition.clearTypes()
	
			for i in resource.findProperties():
				# parse statement
				condition.parse(i)
	
			return condition
		
		else:
			statement = resource
			# get predicate
			predicate = str(statement.getPredicate())
	
			# regex
			if predicate.equals(PROPERTY.SEAS_REGEX):
				try:
					self.addRegex(statement.getString())
				except:
					print "Unable to interpret seas:regex value as literal string."
					traceback.print_exc()
				return
	
			# or
			if predicate.equals(PROPERTY.SEAS_OR):
				types = None
				try:
					types = Tools().getResourceTypes(statement.getResource())
				except:
					print "Unable to interpret seas:or value as resource."
					traceback.print_exc()
	
				# controllability
				if types.contains(RESOURCE.SEAS_CONTROLLABILITY):
					try:
						self.addOr(Controllability().parse(statement.getResource()))
					except:
						print "Unable to interpret seas:or value (of type seas:Controllability) as resource."
						traceback.print_exc()
					return
	
				# availability
				if types.contains(RESOURCE.SEAS_AVAILABILITY):
					try:
						self.addOr(Availability().parse(statement.getResource()))
					except:
						print "Unable to interpret seas:or value (of type seas:Availability) as resource."
						traceback.print_exc()
					return
	
				# condition
				if types.contains(RESOURCE.SEAS_CONDITION):
					try:
						self.addOr(Condition().parse(statement.getResource()))
					except:
						print "Unable to interpret seas:or value (of type seas:AndCondition) as resource."
						traceback.print_exc()
					return
	
				# could not parse into any entity !!
				# losing data !
				print "Condition: Could not match actor " + statement.getResource().toString() + \
						" to any concrete type. Type might not be described or parsing functionality for " + \
						" the type might be missing. Found types: " + str(types)
				try:
					self.addOr(Obj().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:or value as resource."
					traceback.print_exc()
	
				return

			# and
			if predicate.equals(PROPERTY.SEAS_AND):
				types = None
				try:
					types = Tools().getResourceTypes(statement.getResource())
				except:
					print "Unable to interpret seas:and value as resource."
					traceback.print_exc()
	
				# controllability
				if types.contains(RESOURCE.SEAS_CONTROLLABILITY):
					try:
						self.addAnd(Controllability().parse(statement.getResource()))
					except:
						print "Unable to interpret seas:and value (of type seas:Controllability) as resource."
						traceback.print_exc()
					return
	
				# availability
				if types.contains(RESOURCE.SEAS_AVAILABILITY):
					try:
						self.addAnd(Availability().parse(statement.getResource()))
					except:
						print "Unable to interpret seas:and value (of type seas:Availability) as resource."
						traceback.print_exc()
					return
	
				# condition
				if types.contains(RESOURCE.SEAS_CONDITION):
					try:
						self.addAnd(Condition().parse(statement.getResource()))
					except:
						print "Unable to interpret seas:and value (of type seas:AndCondition) as resource."
						traceback.print_exc()
					return
	
				# could not parse into any entity !!
				# losing data !
				print "Condition: Could not match actor " + statement.getResource().toString() + \
						" to any concrete type. Type might not be described or parsing functionality for " + \
						" the type might be missing. Found types: " + str(types)
				try:
					self.addAnd(Obj().parse(statement.getResource()))
				except:
					print "Unable to interpret seas:and value as resource."
					traceback.print_exc()
	
				return
	
			# pass on to Obj
			super(Condition, self).parse(statement)

	def hasOr(self):
		return len(self.ors) > 0

	def getOrs(self):
		return self.ors

	def addOr(self, o):
		self.ors.append(o)

	def hasAnd(self):
		return len(self.ands) > 0

	def getAnds(self):
		return self.ands

	def addAnd(self, a):
		self.ands.append(a)

	def hasRegex(self):
		return len(self.regexes) > 0

	def getRegexes(self):
		return self.regexes

	def addRegex(self, regex):
		self.regexes.append(regex)
