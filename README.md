# router_restart
A program designed to restart and device (by powering off and on), using a relay, if a ping fails.

I use this program on a Raspberry Pi. It utilises the GPIO ports. If a ping to Google (IP address can be changed in the variable section) fails, then, a relay is triggered. 

For example, if a router loses connection to the internet, it is turned off and on.

Varaibales include:

Address to be pinged
Frequency off pings
How many failed pings before the relay is trigged 
How long the relay stays high/low
