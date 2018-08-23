"""
Support for getting the state of a Thermoworks Smoke Thermometer
Requires Smoke Gateway Wifi
"""

REQUIREMENTS = ['pyrebase4>=4.1.0']

# Temperature units
TEMP_CELSIUS = '°C'
TEMP_FAHRENHEIT = '°F'

PROBE_1 = 'probe1'
PROBE_2 = 'probe2'
PROBE_1_MIN = 'probe1Min'
PROBE_1_MAX = 'probe1Max'
PROBE_2_MIN = 'probe2Min'
PROBE_2_MAX = 'probe2Max'


def initialize_app(email, password, init=False, exclude_serials=None):
    if exclude_serials is None:
        exclude_serials = []
    return ThermoworksDataMgr(email, password, init, exclude_serials)


class ThermoworksDataMgr:
    """Manage the connection to firebase"""

    def __init__(self, email, password, init, excluded):
        """Set up the connection"""
        import pyrebase

        # semi-contstants

        # seconds before expiration that we should refresh firebase session
        self._SESSION_REFRESH = 600
        self._SHORT_INTERVAL = 60  # seconds
        self._LONG_INTERVAL = 180  # seconds
        # seconds old temp reading must be before switching to long interval
        self._INTERVAL_THRESHOLD = 3600

        # these were mined from the android APK... hopefully they don't mind too much
        config = {
            "apiKey": "AIzaSyCfCUKlG5-VPsqta-9M92XBSFLHYsbSqLk",
            "authDomain": "smoke-cloud.firebaseapp.com",
            "databaseURL": "https://smoke-cloud.firebaseio.com",
            "storageBucket": "smoke-cloud.appspot.com",
            "projectId": "smoke-cloud",
            "messagingSenderId": "74663406178"
        }

        # init firebase connection
        firebase = pyrebase.initialize_app(config)

        # get auth service
        self.auth = firebase.auth()

        # login
        self._email = email
        self._password = password
        self.user = ""
        self.uid = ""
        self.token = ""
        self.expires = 0
        self.login()

        # get db service
        self.db = firebase.database()

        # data vars
        self._serials = []
        self._devices = {}
        self._units = {}
        self._data = {}
        self._updated = {}

        # get list of registered devices
        results = self.db.child("users").child(self.uid).child("devices")\
            .child("smoke").get(token=self.token)
        for smoke in results.each():
            smoke = smoke.val()
            serial = smoke["device"]
            if serial not in excluded:
                self._serials.append(serial)
                self._devices[serial] = smoke
                self._units[serial] = {}

                # load data for this device
                if init:
                    self.update(serial)

    def serials(self):
        """Return the list of device serials."""
        return self._serials

    def devices(self):
        """Return the list of all devices."""
        return self._devices

    def device(self, serial):
        """Return a specific device."""
        return self._devices.get(serial, {})

    def name(self, serial):
        """Return a device's name"""
        return self.device(serial).get("name", "")

    def data(self, serial):
        """Return device data"""
        if self.should_update(serial):
            self.update(serial)
        return self._data.get(serial, {})

    def units(self, serial, probe=PROBE_1):
        """Return probe units"""
        return self._units.get(serial, {}).get(probe, TEMP_FAHRENHEIT)

    def login(self):
        """Perform login from scratch"""
        from time import time
        self.user = self.auth.sign_in_with_email_and_password(
            self._email, self._password)
        self.uid = self.user["localId"]
        self.token = self.user["idToken"]
        self.expires = time() + int(self.user["expiresIn"])

    def maintain_conn(self):
        """Check if we need to login or refresh session"""
        from time import time
        if time() > self.expires:
            self.login()
        elif time() > self.expires - self._SESSION_REFRESH:
            self.user = self.auth.refresh(self.user['refreshToken'])
            self.expires = time() + int(self.user["expiresIn"])

    def should_update(self, serial):
        """Check if data is stale"""
        from time import time
        now = time()
        updated = self._updated.get(serial, 0)
        last_data = self._data.get(serial, {}).get("time", 0)
        if updated == 0 or last_data == 0:
            return True
        elif now - last_data > self._INTERVAL_THRESHOLD:
            if now - updated < self._LONG_INTERVAL:
                return False
        elif now - updated < self._SHORT_INTERVAL:
            return False
        return True

    def update(self, serial):
        """Refresh data from firebase"""
        from time import time, strftime, localtime
        self._updated[serial] = time()
        self.maintain_conn()

        # get temp data from firebase
        results = self.db.child("smokeTemp").child(serial)\
            .order_by_key().limit_to_last(1).get(token=self.token)
        latest = 0
        values = {}
        # find latest value
        for key, temp in results.val().items():
            time = int(temp["time"])
            if time > latest:
                latest = time
                values = temp
        values["time"] = latest
        values["localtime"] = strftime(
            "%a, %d %b %Y %H:%M:%S", localtime(latest))

        # get extra data
        results = self.db.child("smoke").child(serial).get(token=self.token)
        for key, val in results.val().items():
            if key in ["data", "minMax", "probeNames"]:
                for k, v in val.items():
                    if key == "probeNames":
                        k += "Name"
                    values[k] = v

            elif key == "unit":
                for k, v in val.items():
                    if v == "f":
                        self._units[serial][k] = TEMP_FAHRENHEIT
                    else:
                        self._units[serial][k] = TEMP_CELSIUS

        # we need to calculate min/max since that's the app's job on the phone
        min_max = {
            PROBE_1_MIN: values.get(PROBE_1_MIN, ""),
            PROBE_1_MAX: values.get(PROBE_1_MAX, ""),
            PROBE_2_MIN: values.get(PROBE_2_MIN, ""),
            PROBE_2_MAX: values.get(PROBE_2_MAX, "")
        }
        min_max_changed = False

        for key, val in min_max.items():
            temp_str = ""

            try:
                val = float(val)
            except ValueError:
                val = 0.0

            try:
                if PROBE_1 in key:
                    temp_str = values[PROBE_1]
                    temp = float(temp_str)
                else:
                    temp_str = values[PROBE_2]
                    temp = float(temp_str)
            except ValueError:
                temp = 0.0

            if not val or ("Min" in key and temp < val)\
                    or ("Max" in key and temp > val):
                min_max[key] = temp_str
                min_max_changed = True
                values[key] = temp_str

        # update firebase if we changed anything
        if min_max_changed:
            self.db.child("smoke").child(serial).child("minMax")\
                .set(min_max, token=self.token)

        # store data
        self._data[serial] = values
