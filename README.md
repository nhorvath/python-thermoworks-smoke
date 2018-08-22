# python-thermoworks-smoke
Pull data for your thermoworks smoke thermometer (https://www.thermoworks.com/Smoke).
This requires a smoke wifi gateway (https://www.thermoworks.com/Smoke-Gateway) with an internet connection.

You will need to have previously registered your smoke to your account via the mobile app.
You will provide the email and password you used to this application to connect and pull your data.

Uses Pyrebase4 (https://github.com/nhorvath/Pyrebase4) for interacting with firebase where thermoworks puts the data.

# Installation
`pip install thermoworks_smoke`

# API
#### thermoworks_smoke.initialize_app(email, password, init=False, excluded_serials=[])
* email: the email registered in the thermoworks app
* password: the password registered in the thermoworks app
* init: (optional) set true to preload data for all devices
* excluded_serials: (optional) a list of device serial numbers to ignore

### The Data Manager returned by initialize_app
#### serials() - list
* Get all device serials registered to this user.
#### data(serial) - dict
* Get data for the specified serial number. Updates will be performed automatically and cached.
#### devices() - list
* Get the list of all devices registred to this user.
#### device(serial) - dict
* Get the device information for the specified serial.
#### name(serial) - string
* Get the device name for the specified serial.
#### units(serial, probe=PROBE_1) - string
* Get the unit for the specified serial and probe.
  * You can use `from thermoworks_smoke import TEMP_FAHRENHEIT, TEMP_CELSIUS` to compare to these.
  * You can use `from thermoworks_smoke import PROBE_1, PROBE_2` to get the constants for each probe name.
#### update(serial) - void
* Force update from server (do not call this too frequently). Calling this is unnecessary as calls to data() will
automatically update as needed.

# Usage Example
```python
import thermoworks_smoke

# init
smoke = thermoworks_smoke.initialize_app(email, password)

# get list of registered devices
serials = smoke.serials()

# print data for each serial
for serial in serials:
    values = smoke.data(serial)
    print(serial)
    print(values)

```