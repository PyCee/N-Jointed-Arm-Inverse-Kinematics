def draw_circle(canvas, circle, **kwargs):
	origin = circle.get_origin()
	_draw_circle(canvas, origin[0], origin[1], circle.get_radius(), **kwargs)
					#
					#start=0,
					#extent=1,
def _draw_circle(canvas, x, y, r, **kwargs):
	return canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)