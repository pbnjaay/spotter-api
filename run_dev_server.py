#!/usr/bin/env python
import os
import subprocess
import sys

os.environ['SECRET_KEY'] = 'django-insecure-a7d+vts38jz5olou!p=oc9%@05k(wta$b#p#5%uedp&!0td1jr'
os.environ['DEBUG'] = 'True'
os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1'
os.environ['CORS_ALLOW_ALL_ORIGINS'] = 'True'
os.environ['CORS_ALLOWED_ORIGINS'] = 'http://localhost:3000'

print("Environment variables set for development.")
print("Starting Django development server...")

cmd = [sys.executable, 'manage.py', 'runserver']
if len(sys.argv) > 1:
    cmd.extend(sys.argv[1:])

subprocess.run(cmd)
