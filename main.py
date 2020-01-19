import sys
import django
import os
if __name__=='__main__':
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")
    if django.VERSION[0] < 3:
        raise Exception("Must be using Django 3")
    os.system("python interface_recommandation/manage.py runserver")


