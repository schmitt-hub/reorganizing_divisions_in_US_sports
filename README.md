# Reorganizing divisions in US sports
The big 4 US sport leagues (NFL, NBA, MLB & NHL) are arranged in divisions, i.e. teams in the same division play each other more often throughout a season. Thus, a well thought out organization of divisions is crucial for keeping travel distances small -- not only for team members but also for away fans willing to travel to the enemy's territory to support their team.
So how would divisions look like that are arranged in such a way that the distances between division foes are minimized? We will turn to Mathematical Optimization to answer this.

# Repository content
- For each of the 4 leagues we obtain data regarding the stadium name and city for each team from `geojango.com`. This builds the basis for the input data table `US_stadiums.xlsx`, where for each team we also map the division that the team currently plays in. 
- `reorganize_divisions.py` contains all the code.

   First we geocode the exact coordinates of each team's stadium from their respective names and cities using Python's `Geopy` client. Geopy also provides a function to compute the geodesic distance (i.e. shortest distance on the surface of the earth) between each of these locations, which we will gladly make use of.
