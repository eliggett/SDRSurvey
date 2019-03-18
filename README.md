# SDRSurvey
scan.py will record GPS and RF data to a CSV file at regular intervals. The data include:

GPS: Lat, Long, Height, Speed, Track, Climb
RTL-SDR: Signal Streng, center frequency, gain setting, and full-bandwidth PSD
UNIX epoch time, human readable local time, human readable local date

Be suer and adjust the bandwidth and gain properly. Take a few measurements first to determine how much gain is needed. 
