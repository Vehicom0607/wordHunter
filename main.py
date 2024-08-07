# Show the current camera and the detected red square on the calibration image
# Use a sample image to make sure that the camera is correctly calibrated

# Press the start button using the machine
# Reset the robot to 0, 0

# Detect letters and plug into the solver
# Get the combinations from the solver.
# Execute each word using a variant of a greedy algorithm

import cv2
import numpy as np
import pytesseract

import CalibrateCamera
import DetectLetters
import solver
import ControlCNC
import Algos

current_pos = [0, 0, 0]
current_pos = ControlCNC.reset(current_pos)

# Calibrate with red squares
CalibrateCamera.show_frame()
pts_src = False
while type(pts_src) == bool:
    pts_src = CalibrateCamera.calibrate()

while True:
    # Confirm with the test image that this works
    DetectLetters.view_sample(pts_src)

    # Click the Start button
    current_pos, start_time = ControlCNC.start_game(current_pos)

    # Get the letters
    grid = DetectLetters.get_letters(pts_src)

    # Solve the game
    word_list = solver.get_words(grid)
    ordered_word_list = Algos.greedy_biggest(word_list)
    claimed_words = ControlCNC.win(ordered_word_list, start_time, current_pos)

    # Expected words and score
    print(Algos.find_expected_score(claimed_words))
    print(len(claimed_words))