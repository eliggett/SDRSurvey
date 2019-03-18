from pylab import var, log10, psd, xlabel, ylabel, show, plot, clf, xlim, ylim
from math import sqrt
from rtlsdr import *
import gpsd
import time;

# Connect to the local gpsd
gpsd.connect()

center_freq = 162.550E6; # Don't forget to include E6 for MHz 
totalbw = 0.012; # MHz
halfbw = totalbw/2;
cfm = center_freq / 1.0E6;

sdr = RtlSdr()

sdr.center_freq = center_freq
#sdr.gain = 30
#sdr.gain = 0;
sdr.gain = 15;
sdr.set_agc_mode(False)
sdr.sample_rate = 2.048e6


while True:
    # Get gps position
    packet = gpsd.get_current()

    # See the inline docs for GpsResponse for the available data


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
    #human readable time

    print("Position: Longitude: " + str(longitude) + ", Latitude: " + str(latitude) + ", Altitude: " + str(altitude) + "m, Speed: " + str(speed));

    logstr = str(time.time()) + "," + datestr + "," + timestr;
    logstr += "," + str(latitude) + "," + str(longitude);
    logstr += "," + str(altitude) + "," + str(speed);
    logstr += "," + str(track) + "," + str(climb);
    #logstr += "\n";


    # sample the (other) RF:

    
    s = sdr.read_samples(sdr.sample_rate * 1); # simple way to get 1 second

    # remove DC offset:
    #m = s.mean();
    #for samp in range(0, len(s)):
    #    s[samp] = s[samp] - m
    # could we just do this:
    # which is what demean() does.. only without extra allocations:
    s = s-s.mean(); 

    # Verify gain did not change during collection:
    print("Gain: " + str(sdr.gain) + ", center freq: " + str(sdr.center_freq/1.0e6) + "MHz, sample rate: " + str(sdr.sample_rate/1.0e6) + " MHz")

    #print("Variance of s: " + str(var(s)) + ", " + str(20*log10(var(s))) + "dBfs");

    [power,freq] = psd(s, NFFT=4096*2, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
    # can add demean as a function inside the psd() call to automatically take out the DC. Doesn't seem optimized though.  
    # Note: Freq is now in MHz
    #xlabel("Frequency, MHz");
    #ylabel("Power, dBfs");
    #show();

    #clf();

    #plot(freq, 10*log10(power) , 'b')
    #xlim(  [cfm - halfbw, cfm + halfbw ])
    #ylim([-60,20])


    # Trim:
    stepsize = freq[1] - freq[0]; # 250 Hz
    # if we are interested in +/- 6 khz, we need to step how many steps?
    stepsout = int(halfbw/stepsize); 

    pwrsum = sum(power[ int(power.size/2)-stepsout : int(power.size/2)+stepsout ] )
    totalpower = pwrsum * sqrt(totalbw);

    print("Power sum: " + str(10*log10(totalpower)))

    # Not sure about this array to str conversion

    temppwr = ','.join(map(str, 10*log10(power[ int(power.size/2)-stepsout : int(power.size/2)+stepsout ])));
    tempfreq = ','.join(map(str, freq[ int(power.size/2)-stepsout : int(power.size/2)+stepsout ]));

    #logstr += "," + str(totalpower) + str(power[ int(power.size/2)-stepsout : int(power.size/2)+stepsout ]) + "," + str( freq[ int(power.size/2)-stepsout : int(power.size/2)+stepsout ]);

    logstr += "," + str(sdr.gain) + "," + str(sdr.center_freq/1.0e6) +","+ str(10*log10(totalpower)) + "," + temppwr + "," + tempfreq;
    logstr += "\n";


    logfile = open("/home/eliggett/Documents/projects/sdr/log/gpslog.csv", "a+")
    logfile.write(logstr)
    logfile.close()

    print("Delaying for 60 seconds until next scan...");
    time.sleep(60)
    #choice = input("Press Enter! to continue or X, then enter to exit: ")
    #if choice=="X":
    #    break;
    
sdr.close()

