
all: zip

install:
	sudo apt-get install python3-tk
test:
	@python3 test.py
run:
	@python3 __main__.py
zip:
	@mkdir -p N-Joint_Inverse_Kinematics/
	@cp __main__.py N-Joint_Inverse_Kinematics/
	@cp n_jointed_arm_ik.py N-Joint_Inverse_Kinematics/
	@cp page_frames.py N-Joint_Inverse_Kinematics/
	@cp arm_controller.py N-Joint_Inverse_Kinematics/
	@cp canvas.py N-Joint_Inverse_Kinematics/
	@cp input_section.py N-Joint_Inverse_Kinematics/

	@zip -r N-Joint_Inverse_Kinematics.zip \
		N-Joint_Inverse_Kinematics/
	@rm N-Joint_Inverse_Kinematics/*.py
	@rmdir N-Joint_Inverse_Kinematics/
