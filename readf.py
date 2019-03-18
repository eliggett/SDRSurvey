from pylab import var, log10, psd, xlabel, ylabel, show, plot, clf, xlim, ylim
from math import sqrt
from rtlsdr import *

center_freq = 162.550E6; 
totalbw = 0.012; # MHz
halfbw = totalbw/2;
cfm = center_freq / 1.0E6;

sdr = RtlSdr()
sdr.center_freq = 446.100E6
sdr.center_freq = center_freq # NOAA Weather Station
#sdr.gain = 30
#sdr.gain = 0;
sdr.gain = 0;
sdr.set_agc_mode(False)
sdr.sample_rate = 2.048e6
#sdr.sample_rate = 1.8e6
print("Gain: " + str(sdr.gain) + ", center freq: " + str(sdr.center_freq/1.0e6) + "MHz, sample rate: " + str(sdr.sample_rate/1.0e6) + " MHz")
s = sdr.read_samples(sdr.sample_rate * 1); # simple way to get 1 second

# remove DC offset:
m = s.mean();
for samp in range(0, len(s)):
    s[samp] = s[samp] - m

# Verify gain did not change during collection:
print("Gain: " + str(sdr.gain) + ", center freq: " + str(sdr.center_freq/1.0e6) + "MHz, sample rate: " + str(sdr.sample_rate/1.0e6) + " MHz")

print("Variance of s: " + str(var(s)) + ", " + str(20*log10(var(s))) + "dBfs");

[power,freq] = psd(s, NFFT=4096*2, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
# Note: Freq is now in MHz
#xlabel("Frequency, MHz");
#ylabel("Power, dBfs");
#show();

clf();

plot(freq, 10*log10(power) , 'b')
xlim(  [cfm - halfbw, cfm + halfbw ])
#ylim([-60,20])


# Trim:
stepsize = freq[1] - freq[0]; # 250 Hz
# if we are interested in +/- 6 khz, we need to step how many steps?
stepsout = int(halfbw/stepsize); 

sdr.close()


pwrsum = sum(power[ int(power.size/2)-stepsout : int(power.size/2)+stepsout ] )

totalpower = pwrsum * sqrt(totalbw);

print("Power sum: " + str(10*log10(totalpower)))
show()

# Notes:

# It may be this simple:
# rtl_power -f 93.1M:93.2M:50k /tmp/fm_stations.csv -1 -i 1
# perhaps adding a time limit other than 10 seconds, say 2 seconds. 




