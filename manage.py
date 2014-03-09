#!/usr/bin/env python
import os
import sys

if sys.argv[1] == 'test':
    os.environ["DJANGO_SETTINGS_MODULE"] = "kno.test_settings"

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kno.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
