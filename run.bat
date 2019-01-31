@echo off

set TERMIN=1
set NUMER_NA_LISCIE=120

set GOOGLE_APPLICATION_CREDENTIALS=%CD%\secret.json
set PATH=%PATH%;C:\Python37

pip install -r requirements.txt
cls
title Nasluchiwanie oceny z PIO
python PIOupdate.py %TERMIN% %NUMER_NA_LISCIE%