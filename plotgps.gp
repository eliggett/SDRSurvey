# gps plot in 3d

set datafile separator ","

splot "gpslog.csv" using 4:5:6 with linespoints
