
import edit

path_transfo = '/home/julie/Documents/dm/etc/schema/new.json'
path = '/home/julie/Documents/dm/etc/schema/'

edit.create(path, 'new.json')
edit.add_entry(path_transfo, 'input', 'mongodb:///mongodb-default-eventslog?table=events_log')
edit.add_query(path_transfo, {
		"event_type":"check",
		"ticket": {"$exists": True},
		"ticket_declared_date": {"$exists": True},
		"ticket_date": {"$exists": True},
		"ticket_declared_author": {"$exists": True}
	})
edit.add_entry(path_transfo, 'output', 'mongodb:///mongodb-default-alarmtmpcheck')