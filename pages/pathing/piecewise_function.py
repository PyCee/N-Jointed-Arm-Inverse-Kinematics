from vector import Vector
from math import *

class Piecewise_Function:
	def __init__(self, start_t, end_t, x_eval, y_eval):
		try:
			self.__start_t = float(start_t)
		except:
			pass
		try:
			self.__end_t = float(end_t)
		except:
			pass
		self.__x_eval = x_eval
		self.__y_eval = y_eval
	def contains_t(self, t):
		return self.__start_t <= t and t <= self.__end_t
	def get_start_t(self):
		return self.__start_t
	def get_end_t(self):
		return self.__end_t
	def evaluate_x(self, t):
		return eval(self.__x_eval)
	def evaluate_y(self, t):
		return eval(self.__y_eval)
	def has_x_evaluation(self):
		return self.__x_eval != ""
	def has_y_evaluation(self):
		return self.__y_eval != ""
	def get_start_point(self):
		return self.get_point(self.__start_t)
	def get_end_point(self):
		return self.get_point(self.__end_t)
	def get_point(self, t):
		point = Vector(None, None)
		if self.has_x_evaluation():
			point.x = self.evaluate_x(t)
		if self.has_y_evaluation():
			point.y = self.evaluate_y(t)
		return point
