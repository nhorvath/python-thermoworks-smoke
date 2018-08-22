# python-thermoworks-smoke
Pull data for your thermoworks smoke thermometer (https://www.thermoworks.com/Smoke).
This requires a smoke wifi gateway (https://www.thermoworks.com/Smoke-Gateway) with an internet connection.

You will need to have previously registered your smoke to your account via the mobile app.
You will provide the email and password you used to this application to connect and pull your data.

Uses Pyrebase4 (https://github.com/nhorvath/Pyrebase4) for interacting with firebase where thermoworks puts the data.

# Installation
`pip install thermoworks_smoke`

# API
#### thermoworks_smoke.initialize_app(email, password, excluded_serials=[])
* email: the email registered in the thermoworks app
* password: the password registered in the thermoworks app
* excluded_serials: (optional) a list of device serial numbers to ignore


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