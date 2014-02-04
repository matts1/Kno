#!/usr/bin/env python
import os
import sys

if sys.argv[1] == 'test':
    # when testing we want to be testing as if we're in production
    os.environ["DJANGO_SETTINGS_MODULE"] = "kno.production"

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kno.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
