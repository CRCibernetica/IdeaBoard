from ideaboard import IdeaBoard
from time import sleep_ms

ib = IdeaBoard()

# Create servo1 on Pin 4
servo1 = ib.Servo(4)

while True:
    # Set servo angle to 10 degrees
    servo1.angle(10)
    sleep_ms(2000)
    # Set servo angle to 170 degrees
    servo1.angle(170)
    sleep_ms(2000)