import shoot_logic as sl
from time import sleep

sl.init_shoot()

while True:
	sl.shoot()
	sleep(1)