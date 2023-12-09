import time
import ping3
import RPi.GPIO as GPIO
import socket

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)

failed_pings_count = 0

# Edit the variables, below:

failure_threshold = 3
time_between_pings = 2 #In seconds
program_run_delay = 0 # Required so that the program doesn't start before there is a network connection.
router_off_time = 15 # In seconds, the time the router should remain off
restart_time = 10 # In seconds the time following a reset the pings should start again
poling_address = '8.8.8.8'

# File to save log details
log_file = '/home/pi/automation_project/log_file.txt'
time.sleep(1)
print ('''
This is a program that poles an IP address for a response. 
3 failed pings causes a relay to trigger (powers off and on a router).
 ''')
time.sleep(1)

# Program run delay
time.sleep(program_run_delay)

while True:
    try:
        # Attempt to ping Google. Address can be changed
        result = ping3.ping(poling_address)

        if result is None:
            # Ping failed
            failed_pings_count += 1
            print(f'Failed ping {failed_pings_count}')

            if failed_pings_count == failure_threshold:
                # Trigger relay when three consecutive failures occur
                print('Triggering relay...')
                GPIO.output(18, GPIO.HIGH)
                time.sleep(router_off_time)
                print('The router should now have rebooted. We will set the GPIO pin to low')
                GPIO.output(18, GPIO.LOW)
                time.sleep(restart_time)
                failed_pings_count = 0
                # Updates a log file
                with open(log_file, 'a') as log_file:
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    log_file.write(f'{timestamp}: Reset triggered\n')
        else:

            # Reset the counter if the ping is successful
            print(f'Ping time to poling adderess is {result}')
            failed_pings_count = 0

        time.sleep(time_between_pings)

    except Exception as e:
        # Catch any exception (including failed pings)
        failed_pings_count += 1
        print(f'Ping has failed {failed_pings_count} times')

        if failed_pings_count == failure_threshold:
            # Trigger relay when three consecutive failures occur
            print('Triggering relay...')

            GPIO.output(18, GPIO.HIGH)
            time.sleep(router_off_time)
            print('The router should now have rebooted. We will set the GPIO pin to low')
            GPIO.output(18, GPIO.LOW)
            time.sleep(restart_time)
            failed_pings_count = 0
            with open(log_file, 'a') as log_file:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                log_file.write(f'{timestamp}: Reset triggered\n')

        time.sleep(time_between_pings)
(END)

