#!/usr/bin/env python3

import sys
import argparse
import thermoworks_smoke
from requests.exceptions import HTTPError

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pull Smoke Gateway Temperatures")
    parser.add_argument('-e', '--email',
                        metavar='email',
                        required=True,
                        help="Account email address")
    parser.add_argument('-p', '--password',
                        metavar='password',
                        required=True,
                        help="Account password")

    args = parser.parse_args()

    email = args.email
    password = args.password

    # init
    mgr = None
    try:
        mgr = thermoworks_smoke.initialize_app(email, password, True)
    except HTTPError as error:
        msg = "{}".format(error.strerror)
        if 'EMAIL_NOT_FOUND' in msg or \
                "INVALID_PASSWORD" in msg:
            print("Invalid email and password combination")
        else:
            print(msg)
        return 1

    # get list of registered devices
    serials = mgr.serials()

    # print data for each serial
    for serial in serials:
        values = mgr.data(serial)
        values['serial'] = serial

        print(values)

    return 0


if __name__ == "__main__":
    sys.exit(main())