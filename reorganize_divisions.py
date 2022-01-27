from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from gurobipy import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd


def load_data(data_file, league):
    arenas_df = pd.read_excel(data_file, sheet_name=league)
    # make sure the teams are sorted in order of their division
    arenas_df = arenas_df.sort_values(by=['Division'])
    return arenas_df


def geocode_distances(arenas_df):
    """
    Geocode the coordinates of each arena location
    :param arenas_df: a dataframe containing the arena name for each team
    :return: a list containing the coordinates of each arena location
    """
    locator = Nominatim(user_agent="agent", timeout=None)
    print('Geocode the location of the arenas. This will take a few seconds')
    locs = [(locator.geocode(arenas_df.at[i, 'Arena Name']+', '+arenas_df.at[i, 'Arena Location']).latitude,
             locator.geocode(arenas_df.at[i, 'Arena Name']+', '+arenas_df.at[i, 'Arena Location']).longitude)
            for i in arenas_df.index]
    return locs


def create_model(dists, nr_of_teams, nr_of_teams_per_div):
    """
    Build a model that seeks to minimize the total distance between teams from the same division
    :param dists: a 2D-array containing the distances from all arenas to each other
    :param nr_of_teams: the total number of teams in the league
    :param nr_of_teams_per_div: the number of teams per division
    :return: the built model
    """
    # set up divisions such that the distances between division opponents are minimized
    print('Set up model')
    m = Model('Division Reorganization')
    x = m.addVars([(i, j) for i in range(nr_of_teams) for j in range(i + 1, nr_of_teams)], vtype=GRB.BINARY, name='x')
    m.setObjective(quicksum(dists[i][j] * x[(i, j)] for i in range(nr_of_teams) for j in range(i + 1, nr_of_teams)))

    # every team is in a division with nr_of_teams_per_div-1 other teams
    m.addConstrs(quicksum(x[(i, j)] for j in range(i + 1, nr_of_teams)) + quicksum(x[(j, i)] for j in range(i)) ==
                nr_of_teams_per_div - 1 for i in range(nr_of_teams))

    # transitivity constraint:
    # if a is in a division with b, and b is in a division with c, then a must be in a division with c as well
    m.addConstrs(x[(i, j)] + x[(j, k)] <= x[(i, k)] + 1
                 for i in range(nr_of_teams) for j in range(i + 1, nr_of_teams) for k in range(j + 1, nr_of_teams))
    m.addConstrs(x[(i, j)] + x[(i, k)] <= x[(j, k)] + 1
                 for i in range(nr_of_teams) for j in range(i + 1, nr_of_teams) for k in range(j + 1, nr_of_teams))
    m.addConstrs(x[(i, k)] + x[(j, k)] <= x[(i, j)] + 1
                 for i in range(nr_of_teams) for j in range(i + 1, nr_of_teams) for k in range(j + 1, nr_of_teams))

    return m


def optimize_divisions(m):
    """
    solve the model to obtain the optimal divisions
    :param m: the model to be solved
    :return: a list of lists containing the teams in each division;
        the total distance total distance between teams from the same division
    """
    print('Optimize model')
    m.optimize()

    divisions = []
    for i in range(nr_of_teams):
        for j in range(i + 1, nr_of_teams):
            var = m.getVarByName('x['+str(i)+','+str(j)+']')
            if var.x > 0.5:
                last_teams_per_div = [div[-1] for div in divisions]
                if i not in last_teams_per_div:
                    divisions.append([i, j])
                else:
                    divisions[last_teams_per_div.index(i)].append(j)
                break
    return divisions, round(m.objVal)


def compute_total_distance(divisions, dists):
    nr_of_teams_per_div = len(divisions[0])
    return round(sum(dists[div[i]][div[j]] for i in range(nr_of_teams_per_div) for j in range(i, nr_of_teams_per_div)
                     for div in divisions))


def display_divisions(fig, teams, locs, divisions, total_distance, optimal=True):
    """
    print out the teams in each division and visualize the results on a map
    :param fig: the figure where this subplot will be drawn
    :param teams: a list of teams
    :param locs: a list containing the location for each team's arena
    :param divisions: a list of lists containing the teams in each division
    :param total_distance: the total distance total distance between teams from the same division
    :param optimal: boolean specifying if the given divisions are the optimal (True) or the current divisions (False)
    """
    # draw a map of the united states in Mercator projection
    print()
    print('---------------------------------')
    if optimal:
        ax = fig.add_subplot(211)
        ax.set_title('Optimal divisions - ' + str(total_distance) + 'km')
        print('Optimal Divisions:')
    else:
        ax = fig.add_subplot(212)
        ax.set_title('Current divisions - ' + str(total_distance) + 'km')
        print('Current Divisions:')
    print('---------------------------------')
    map = Basemap(projection='merc', llcrnrlat=23, urcrnrlat=50, llcrnrlon=-128, urcrnrlon=-66, resolution='l')
    # draw coastlines, country boundaries, fill continents.
    map.drawcountries()
    map.fillcontinents(color='coral')

    # print the divisions and draw a line on the map for all new divisions rivals
    for div in divisions:
        print('Division:')
        for i in range(len(div)):
            print(teams[div[i]])
            for j in range(i + 1, len(div)):
                map.drawgreatcircle(locs[div[i]][1], locs[div[i]][0], locs[div[j]][1], locs[div[j]][0], linewidth=2,
                                    color='b')
        print()


if __name__ == "__main__":
    # input parameters
    data_file = '../US_stadiums.xlsx'
    league = 'NFL'  # 'NFL' or 'NBA'

    nr_of_divisions_dict = {'NFL': 8, 'NBA': 6}
    nr_of_divisions = nr_of_divisions_dict[league]
    arenas_df = load_data(data_file, league)
    teams = list(arenas_df['Team Name'])
    nr_of_teams = len(arenas_df)

    if nr_of_teams / nr_of_divisions == nr_of_teams // nr_of_divisions:
        nr_of_teams_per_div = nr_of_teams // nr_of_divisions
        locs = geocode_distances(arenas_df)
        dists = [[geodesic(loc1, loc2).km for loc2 in locs] for loc1 in locs]
        m = create_model(dists, nr_of_teams, nr_of_teams_per_div)
        optimal_divisions, optimal_total_distance = optimize_divisions(m)
        fig = plt.figure()
        display_divisions(fig, teams, locs, optimal_divisions, optimal_total_distance, True)
        current_divisions = [[i+nr_of_teams_per_div*j for i in range(nr_of_teams_per_div)]
                             for j in range(nr_of_divisions)]
        current_total_distance = compute_total_distance(current_divisions, dists)
        display_divisions(fig, teams, locs, current_divisions, current_total_distance, False)
        plt.show()
    else:
        print('The selected number of divisions has to be a divisor of the total number of teams, i.e. ' +
              str(nr_of_teams))

