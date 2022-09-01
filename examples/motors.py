from ideaboard import IdeaBoard
from time import sleep_ms

ib = IdeaBoard()

# motor speed is from -1023 (reverse) to 1023 (forward)
# 0 is stopped
ib.motor_1(1023)
ib.motor_2(-1023)