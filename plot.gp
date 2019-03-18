# Make a heatmap of the area GPS where intensity is signal strength
set datafile separator ","
set pm3d
#set pm3d interpolate 0.001, 0.001
#set pm3d at s

# set mesh, X, Y size as optional arguments X,Y
set dgrid3d 20,20
#unset key
#set tic scale 0

# set view map places the view point at the "top"
#set view map

# with image: colors
# with lines: grid
# without with: both
# with pm3d: errors!
set view map
#set cbrange [-50:-30]
#set xrange [:]
#set yrange [min:max]
set key top center title "test"

# Note, overlaping data is definitely possible.
# so what happens? Proably last read data dominates. 

set autoscale noextend # chop the image at the exact end of the data
splot "gpslog 2019-03-10.csv" using 4:5:12 with image
