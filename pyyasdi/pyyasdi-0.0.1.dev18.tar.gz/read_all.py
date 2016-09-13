import pyYASDI
sma = pyYASDI.pyYASDI()

devices = sma.get_devices()

def print_device(device):
    print("Device %s:"%(device.get_name()))
    for n,i in enumerate(device.channels):
        print("({handle}) {no}: {name} = {value}{unit}".format(
                handle=i.channel_handle,
                no=n,
                name=i.update_name(),
                value=i.update_value(),
                unit=i.update_unit()
            ))

for d in devices:
    print_device(d)
