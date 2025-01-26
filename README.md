# ha-remoteNow
HA integration for devices controlable via the RemoteNow app

Might break components that rely on paho-mqtt, because this integration uses paho-mqtt 2.1.0, which isnt supported yet by home-assistant. \

Config flow still needs some work. \
Please restart instance after setting up TV.

# Working
Volume \
Buttons (Atleast the ones i know about atm) \
Source select \
Channel select

# Underlying Api
https://github.com/Tabisch/remoteNowApi
