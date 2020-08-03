# piEinkClock
Raspberry PI Clock to use with the Waveshare 2.7 e-ink HAT

Install:

pip3 install epd2in7 PIL gpiozero
python3 clock.py


Notes:
The clock relies on another server for temperature/humidity. So far, I'm using another pi with a DHT22 to collect temperature/humidity data and serve. If you do not have such option, temperature/humidity will be NUL (for now).
