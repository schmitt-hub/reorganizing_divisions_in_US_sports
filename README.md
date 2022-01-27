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
The distances between divison foes can be reduced by at least 2.7% in all Big 4 leagues. The current setups of divisions for the NBA and NHL are decently close the optimal setups as the total distances are 2.7% and 6.4% larger than the optimal total distances, respectively. The MLB and NFL, however, exhibit huge potential for improvement (31.6% and 36.2%, respectively). As it turns out, putting a team Dallas (the Cowboys) in an *East* division or a team from Houston (the Astros) in a *West* division is not conducive to minimizing distances within divisions!


<img src="https://user-images.githubusercontent.com/92627184/151376439-c563cf5a-8c44-4161-b07f-84614ecb45a7.png" width="500"/> <img src="https://user-images.githubusercontent.com/92627184/151376425-934df1fe-eaff-4ec9-84cd-63c84d88715f.png" width="500"/> <img src="https://user-images.githubusercontent.com/92627184/151375700-67d8e487-8221-48b6-980a-2b35b59f6518.png" width="500"/> <img src="https://user-images.githubusercontent.com/92627184/151376526-03ac3db0-b367-429f-b1e8-8089f12c2dc0.png" width="500"/>

![MLB_division_reorganization](https://user-images.githubusercontent.com/92627184/151381556-42211042-531e-478f-ba5e-2cd20a4b5dff.png)
![NBA_division_reorganization](https://user-images.githubusercontent.com/92627184/151381560-17fb1399-3da4-47c0-bead-f52656ac9fb9.png)
![NFL_division_reorganization](https://user-images.githubusercontent.com/92627184/151381562-22d4bae8-7b45-4304-be2e-c3b462972f0a.png)
![NHL_division_reorganization](https://user-images.githubusercontent.com/92627184/151381565-9fef4a07-3935-45b0-8fa6-7844e84e1cd4.png)


<img src="https://user-images.githubusercontent.com/92627184/151384628-ccdaee2e-2346-42e9-bbe8-282f6529a3ec.png" width="220"/> <img src="https://user-images.githubusercontent.com/92627184/151384634-0e94f705-9b1b-42ab-90af-67cee8b7f408.png" width="220"/>

<img src="https://user-images.githubusercontent.com/92627184/151384624-fdb04769-f9d0-403c-b042-f5c377c685e7.png" width="220"/> <img src="https://user-images.githubusercontent.com/92627184/151384631-4959fd60-9818-4309-aed9-6b9eb877b8f7.png" width="220"/>




