import detection_logic as dl

cap = dl.init_detection()

while True:
	try:
		card = dl.detect_card(cap)
		print(f"card: {card}")
	except KeyboardInterrupt:
		dl.close_detection(cap)