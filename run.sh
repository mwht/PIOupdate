#!/bin/sh
TERMIN=1
NUMER_NA_LISCIE=120

export GOOGLE_APPLICATION_CREDENTIALS=$PWD/secret.json

pip install --user -r requirements.txt
reset
./PIOupdate.py $TERMIN $NUMER_NA_LISCIE