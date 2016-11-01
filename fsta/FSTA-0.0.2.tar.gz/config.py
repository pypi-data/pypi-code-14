#!/usr/bin/env python
# -*- coding:utf-8 -*

from FSTA.installation import *
from FSTA.action import *
from FSTA.group import *
from FSTA.scenario import *

from FUTIL.my_logging import *
import json

def get_installation():
	return installation(
		groups = [
			group(name = "Maison",
				hotword = "./resources/maison.pmdl",
				scenarios = [
							scenario(text = "LUMIERE ON",
									phrases = [u"Allume la lumière",
												u"lumière s'il te plaît",
												u"lumière"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/LUMIERES",
											payload = "ON",
											text = "ON")),
							scenario(text = "LUMIERE OFF",
									phrases = [u"éteins la lumière",
												u"coupe la lumière"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/LUMIERES",
											payload = "OFF",
											text = "OFF")),
							scenario(text = "MUSIQUE ON",
									phrases = [u"musique",
												u"allume la musique"],
									actions = action_mqtt(
											topic = "T-HOME/SQUEEZE/PISQUEEZE",
											payload = "play",
											text = "Musique")),
							scenario(text = "MUSIQUE OFF",
									phrases = [u"stop la musique",
												u"éteins la musique"],
									actions = action_mqtt(
											topic = "T-HOME/SQUEEZE/PISQUEEZE",
											payload = "stop",
											text = "STOP")),
							scenario(text = "MUSIQUE NEXT",
									phrases = [u"musique suivante",
												u"change la musique"],
									actions = action_mqtt(
											topic = "T-HOME/SQUEEZE/PISQUEEZE",
											payload = "button,jump_fwd",
											text = "Next")),
							scenario(text="VOLUME +",
									phrases = [u"augmente le volume",
												u"plus fort"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/DENON",
											payload = "MVUP",
											text = "+")),
							scenario(text = "VOLUME -",
									phrases = [u"baisse le volume",
												u"moins fort"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/DENON",
											payload = "MVDOWN",
											text = "-")),
							scenario(text = "TV OFF",
									phrases = [u"éteins la télé",
												u"coupe la télé"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/TV",
											payload = "KEY_POWEROFF",
											text = "+")),
							scenario(text="REBOOT KODI",
									phrases = u"reboot Kodi",
									actions = action_mqtt(
											topic = "T-HOME/SALON/KODI",
											payload = "REBOOT",
											text = "Reboot Kodi"))
								]),
			group(name = "KODI",
				hotword = "./resources/Ok Kodi.pmdl",
				scenarios = [
							scenario(text = "REBOOT",
									phrases = u"reboot",
									actions = action_mqtt(
											topic = "T-HOME/SALON/KODI",
											payload = "REBOOT",
											text = "Reboot Kodi")),
							scenario(text="PLAY-PAUSE",
									phrases = [u"pause",
												u"enleve pause"],
									actions = action_mqtt(
											topic = "T-HOME/SALON/KODI",
											payload = json.dumps({
													"cmd": "Player.PlayPause",
													"args" :{
														"playerid": 1
														}
													}),
											text = "Pause"))
								])],
		mqtt_host='192.168.10.155',
		led = led.matrix())