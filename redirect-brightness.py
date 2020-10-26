#!/usr/bin/python3

import pyinotify
import math

class Backlight(pyinotify.ProcessEvent):
	def __init__(self, source, dest):
		self.source = source
		self.dest = dest

		self.source_max = float(open(self.source + '/max_brightness', 'r').read())
		self.dest_max = float(open(self.dest + '/max_brightness', 'r').read())

		self.wm = pyinotify.WatchManager()
		self.notifier = pyinotify.Notifier(self.wm, self)
		self.wm.add_watch(self.source + '/brightness', pyinotify.IN_CLOSE_WRITE)


	def loop(self):
		self.notifier.loop()


	def process_IN_CLOSE_WRITE(self, event):
		source_brightness_p = float(open(self.source + '/actual_brightness', 'r').read()) / self.source_max

		#dest_brightness_p = source_brightness_p
		dest_brightness_p = source_brightness_p ** 2 

		dest_brightness = max(1, int(dest_brightness_p * self.dest_max))

		print(source_brightness_p, dest_brightness_p, dest_brightness)

		open(self.dest + '/brightness', 'w').write(str(dest_brightness))
	


if __name__ == '__main__':
	handler = Backlight(
		source="/sys/class/backlight/panasonic",
		dest="/sys/class/backlight/intel_backlight",
	)

	handler.loop()

