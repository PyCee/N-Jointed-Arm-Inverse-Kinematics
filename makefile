
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
	@zip -r N-Joint_Inverse_Kinematics.zip \
		N-Joint_Inverse_Kinematics/
	@cd N-Joint_Inverse_Kinematics/; \
		rm __main__.py; rm n_jointed_arm_ik.py
	@rmdir N-Joint_Inverse_Kinematics/
