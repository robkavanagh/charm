from dataclasses import dataclass


@dataclass
class Param:

	range:   tuple
	wrapped: bool = False


class ParamCollection(dict):

	@property
	def names(self):
		return list(self.keys())

	@property
	def wrapped(self):
		return [p.wrapped for p in self.values()]

	@property
	def ranges(self):
		return [p.range for p in self.values()]