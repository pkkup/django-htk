# Python Standard Library Imports
import time

# Django Imports
from django.conf import settings

# HTK Imports
from htk.apps.accounts.emails import AccountActivationReminderEmails
from htk.constants.time import *
from htk.scripts.utils import job_runner
from htk.scripts.utils import slog

import script_config


DAEMON_MODE = True
#DAEMON_MODE = False

def main():
    def workhorse():
        AccountActivationReminderEmails().execute_batch()

    while True:
        job_runner(workhorse)

        if settings.TEST:
            # just make sure that it runs
            break

        if not DAEMON_MODE:
            # just run once, don't keep looping
            break

        slog('Done sending reminder emails, sleeping...')
        time.sleep(TIMEOUT_1_HOUR)

if __name__ == '__main__':
    job_runner(main)
