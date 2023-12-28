import rotate_logic as rl
import time

rl.init_rotate()

while True:
	rl.spin_clockwise(100)
	time.sleep(1)
	rl.spin_clockwise(100)
	time.sleep(1)
	rl.spin_anticlockwise(100)
	rl.spin_anticlockwise(100)
	#rl.spin_clockwise(100)
