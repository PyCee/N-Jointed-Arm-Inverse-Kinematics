import display_settings

def draw_grid_lines(canvas, offset):
	'''
	Draw grid lines
	'''
	grid_line_offset = canvas.get_grid_offset()
	half_line_width = 0.75 / canvas.scale_value
	GRID_COLOR = "#CCC"
	text_color = "#888"
	for i in range(-6, 7):
		line_value = grid_line_offset * i
		upper_line_value = line_value + half_line_width
		lower_line_value = line_value - half_line_width
		vert_points = [upper_line_value, -canvas.get_effective_size(),
					upper_line_value, canvas.get_effective_size(),
					lower_line_value, canvas.get_effective_size(),
					lower_line_value, -canvas.get_effective_size()]
		horiz_points = [-canvas.get_effective_size(), upper_line_value,
						canvas.get_effective_size(), upper_line_value,
						canvas.get_effective_size(), lower_line_value,
						-canvas.get_effective_size(), lower_line_value]
		for j in range(8):
			vert_points[j] += offset
			horiz_points[j] += offset
			
			
		canvas.create_polygon(vert_points, fill=GRID_COLOR)
		canvas.create_polygon(horiz_points, fill=GRID_COLOR)

		line_position = offset + lower_line_value
		displayed_line_value = str(line_value).rstrip('0').rstrip('.')
		if display_settings.ShowGridNumbers.get():
			if i != 0:
				# If this is the center line, don't draw the line value
				#   (it looksbad if draw alongside the value for the
				#   horizontal center line)
				
				# Display vertical line values
				canvas.create_text(line_position, offset,
									font=("Times", 10, "bold"),
									fill=text_color, anchor="se",
									text=displayed_line_value)
				
			# Display horizontal line values
			canvas.create_text(offset, line_position,
								font=("Times", 10, "bold"), 
								fill=text_color,
								anchor="sw", 
								text=displayed_line_value)