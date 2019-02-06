
REQ_EXE_FILES=__main__.py n_jointed_arm_ik.py arm_controller.py canvas.py path_controller.py input_section.py pages/display_frame.py pages/length_frame.py pages/pathing_frame.py

all: executable clean

install:
	sudo apt-get install python3-tk python-tk python3-pip
	sudo pip3 install --upgrade pyinstaller
test:
	@python3 test.py
run:
	@python3 __main__.py
executable:
	@pyinstaller -F $(REQ_EXE_FILES)
	@cp ./dist/__main__ ./N_Jointed_Arm_Controller
clean:
	@rm -rf ./dist
	@rm -rf ./build
	@rm -f ./*.spec
	@find . -type f \( -name '*~' -o -name '*.pyc' \) -delete
