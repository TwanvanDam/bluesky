These three files contain population data for the Netherlands in a grid with cells of 1 km x 1 km. IN total the grid ihas size of 1000 km x 1000 km.

It uses a flat earth projected Cartesian reference frame, so x and y.

The origin of the reference frame is lat,lon = 52.307 deg, 4.761 deg (Schiphol) 

The files contain:

x_1km 		= x-coordinates in meters
y_1km 		= y-coordinates in meters
population_1km 	= number of people living in a square

So if you read each of the files in an array x,y, pop, then the cell with center x[i],y[i] has a population of pop[i] people living there.

