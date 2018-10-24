
REQ_EXE_FILES=__main__.py n_jointed_arm_ik.py page_frames.py arm_controller.py canvas.py input_section.py

all: executable clean

install:
	sudo apt-get install python3-tk
test:
	@python3 test.py
run:
	@python3 __main__.py
executable:
	@pyinstaller -F $(REQ_EXE_FILES)
	@cp ./dist/__main__ ./N_Jointed_Arm_Controller
clean:
	rm -r ./dist
	rm -r ./build
	rm ./*.spec
