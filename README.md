# Reorganizing divisions in US sports
The big 4 US sport leagues (NFL, NBA, MLB & NHL) are arranged in divisions, i.e. teams in the same division play each other more often throughout a season. Thus, a well thought out organization of divisions is crucial for keeping travel distances small -- not only for team members but also for away fans willing to travel to the enemy's territory to support their team.
So how would divisions look like that are arranged in such a way that the distances between division foes are minimized? We will turn to Mathematical Optimization to answer this.

## Repository content
- For each of the 4 leagues we obtain data regarding the stadium name and city for each team from *geojango.com*. This builds the basis for the input data table `US_stadiums.xlsx`, where for each team we also map the division that the team currently plays in. 
- `reorganize_divisions.py` contains all the code.

   First, the user is asked to specify which Big 4 league should be examined. Next, we geocode the exact coordinates of each team's stadium from their respective names and cities using Python's *Geopy* client. Geopy also provides a function to compute the geodesic distance (i.e. shortest distance on the surface of the earth) between each of these locations, which we will gladly make use of.
   
   After calculating the distances, we build a model that seeks to minimize the total distance between division opponents. It looks like this:
   
   Finally, we let the solver *Gurobi* solve this model and obtain the optimal organization of divisions, and visualize the results on a map using Matplotlib's *Basemap* toolkit.
   
## Requirements to run code
The code uses some open-source Python packages. The ones that the reader may be most unfamiliar with are:
- *Geopy*, which allowed geocoding the exact locations of the arenas as well as calculating the geodesic distances between these locations.
- *Gurobi*, a software well-equiped for solving (and building) optimization models.
- *Basemap*, a Matplotlib toolkit that was used for plotting the results on a map.

## Results
The distances between divison foes can be reduced by at least 2.7% in all Big 4 leagues. The current setups of divisions for the NBA and NHL are decently close the optimal setups as the total distances are 2.7% and 6.4% larger than the optimal total distances, respectively. The MLB and NFL, however, exhibit huge potential for improvement (31.6% and 36.2%, respectively). This comes to no surprise, considering that the NFL has a team from Dallas play in an *East*, while the MLB puts a team from Houston in a *West* division.
![NBA_division_reorganization](https://user-images.githubusercontent.com/92627184/151372886-17e72716-270f-49ac-b010-333c1b19f4e7.png)|![NHL_division_reorganization](https://user-images.githubusercontent.com/92627184/151372889-75c4e4ae-77a0-451a-9cd8-a18236bb2ad5.png)|![MLB_division_reorg](https://user-images.githubusercontent.com/92627184/151375700-67d8e487-8221-48b6-980a-2b35b59f6518.png)|![NFL_division_reorganization](https://user-images.githubusercontent.com/92627184/151372887-7e7450e8-aa7b-419d-9f69-cdf0e888f7a8.png)
-----|-----|-----|-----

<img src="https://user-images.githubusercontent.com/92627184/151376439-c563cf5a-8c44-4161-b07f-84614ecb45a7.png" width="300"/> <img src="https://user-images.githubusercontent.com/92627184/151376425-934df1fe-eaff-4ec9-84cd-63c84d88715f.png" width="300"/> <img src="https://user-images.githubusercontent.com/92627184/151375700-67d8e487-8221-48b6-980a-2b35b59f6518.png" width="300"/> <img src="https://user-images.githubusercontent.com/92627184/151376526-03ac3db0-b367-429f-b1e8-8089f12c2dc0.png" width="300"/>

![NHL_division_reorg](https://user-images.githubusercontent.com/92627184/151376425-934df1fe-eaff-4ec9-84cd-63c84d88715f.png)
![MLB_division_reorg](https://user-images.githubusercontent.com/92627184/151376432-d6ceba7b-ff56-4b2c-9aa8-5871378e6b9b.png)
![NBA_division_reorg](https://user-images.githubusercontent.com/92627184/151376439-c563cf5a-8c44-4161-b07f-84614ecb45a7.png)
![NFL_division_reorg](https://user-images.githubusercontent.com/92627184/151376526-03ac3db0-b367-429f-b1e8-8089f12c2dc0.png)

