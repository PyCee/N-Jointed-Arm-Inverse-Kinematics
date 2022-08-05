import math
from draw.draw_circle import draw_circle
from draw.draw_length import draw_length
from two_jointed_arm.circle import Circle
from vector import Vector


def draw_arm(canvas, arm_controller, offset):
	position = Vector(0.0, 0.0)
	for i in range(len(arm_controller.lengths)):
		radian = arm_controller.angles[i]
		angle = round(radian * 180 / 3.14159, 3)
		absolute_angle = sum(arm_controller.angles[:i+1])
		draw_length(canvas, position, arm_controller.lengths[i],
						absolute_angle, radian, offset)
		position = position + Vector(arm_controller.lengths[i] *
										math.cos(absolute_angle),
										arm_controller.lengths[i] *
										math.sin(absolute_angle))
	
		# Draw circles that represent origin and endpoint
		r = 4.0 / canvas.scale_value
		canvas.create_oval(-r + offset, -r + offset,
							r + offset, r + offset, 
							fill="#11f", width=0.0)
		if arm_controller.can_reach_point:
			end_point = Circle((arm_controller.point.x + offset, arm_controller.point.y + offset), r)
			draw_circle(canvas, end_point, fill="#f11", width=0.0)
		else:
			bounds_point = Circle((arm_controller.point.x + offset, arm_controller.point.y + offset), r)
			draw_circle(canvas, bounds_point, fill="#888", width=0.0)
			mouse_point = Circle((arm_controller.attempted_reach_point.x + offset, arm_controller.attempted_reach_point.y + offset), r)
			draw_circle(canvas, mouse_point, fill="#f11", width=0.0)