# histogram
set datafile separator ","
n=200 #number of intervals
max=540.0 #max value
min=470.0   #min value
width=(max-min)/n #interval width
#function used to map a value to the intervals
hist(x,width)=width*floor(x/width)+width/2.0
set boxwidth width*0.9
set style fill solid 0.5 # fill style

#count and plot
# Note: The column from the file is the first argument to hist(), beginning with a $. 
# 4,5,6:  lat, long (-118.259--118.258), height (470.0 to 540.0)
# 12: signal strength (-20.0 to -4.0 n=100)
plot "gpslog.csv" u (hist($6,width)):(1.0) smooth freq w boxes lc rgb"blue" notitle

