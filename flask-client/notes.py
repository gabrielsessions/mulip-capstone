##### Initial research/ attempt at implementing an 'optimized' path calculator #####
### Goal: Establish a pathfinding algorithm that can be used to navigate Cozmo in an optimized manner ###

''' 
* use Realsense depth to figure optimized path for Cozmo to get around the AR track without colliding
*****   project optimizaed 2d path representation of the AR track   *****
* use Cozmo internal AI to figure out the best path to take to get around the track
***** run pathfinding algorithm on the Cozmo robot; map path taken *****
***** challenges: Cozmo AI communicaition w/ AR track -or- 2D track overlay *****
* implement path tracking for user trials *
* implement program to show path overlays; compares time, # of obstacles, etc. *
* implement 'return home' function for Cozmo to return to charging station *
'''