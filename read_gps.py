import gpsd
import time;

# Connect to the local gpsd
gpsd.connect()

# Connect somewhere else
#gpsd.connect(host="127.0.0.1", port=123456)

# Could loop here:

# Get gps position
packet = gpsd.get_current()

# See the inline docs for GpsResponse for the available data
print(packet.position())

x = packet.position()

latitude = x[0]
longitude = x[1]
altitude = packet.alt # measured in meters
now = time.time()
#speed = gpsd.speed()
movement = packet.movement()
speed = movement['speed']
track = movement['track']
climb = movement['track']

datestr = time.strftime("%Y-%m-%d", time.localtime() )
timestr = time.strftime("%H:%M:%S", time.localtime() )

logstr = str(time.time()) + "," + datestr + "," + timestr;
logstr += "," + str(latitude) + "," + str(longitude);
logstr += "," + str(altitude) + "," + str(speed);
logstr += "," + str(track) + "," + str(climb);
logstr += "\n";

logfile = open("/tmp/gpslog.txt", "a+")
logfile.write(logstr)
logfile.close()











