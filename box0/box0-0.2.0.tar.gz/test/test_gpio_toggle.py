import box0
import time

dev = box0.usb.open_supported()

dio0 = dev.dio(0)

dio0.static_prepare()

pin0 = dio0.pin(0)

pin0.output()
pin0.low()
pin0.hiz = dio0.DISABLE

try:
	while True:
		pin0.toggle()
		time.sleep(0.5)
except KeyboardInterrupt:
	print("Bye bye")

pin0.low()
pin0.hiz = dio0.ENABLE
dio0.close()

dev.close()
