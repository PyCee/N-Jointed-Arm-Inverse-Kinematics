
from draw.draw_circle import draw_circle
from two_jointed_arm.circle import Circle


def draw_arm_bounds(canvas, bounds, offset):
	'''
	Draw arm bounds
	'''
	BOUNDS_COLOR = "#888"
	circle_origin = (offset, offset)
	for i in range(0, 2):
		draw_circle(canvas, Circle(circle_origin, bounds[i]), outline=BOUNDS_COLOR, width=3)