from mapplanner.mapplanner import MapPlanner

if __name__ == '__main__':

    planner = MapPlanner('C:/Users/mi/PycharmProjects/mapplanner_test/src/benchmarks/spatial/', '1', gazebo=False,
                         LogicalSearch=True, agpath='mapplanner.agent.agent_search', agtype='Agent',
                         searchpath='mapreasoner.logical_search', searchtype='LogicalMapSearch')

    # planner = MapPlanner('C:/Users/mi/PycharmProjects/mapplanner_test/src/benchmarks/spatial/', '1', gazebo=False,
    #                      agpath='mapplanner.agent.agent_search', agtype='Agent',
    #                      searchpath='mapplanner.search.mapsearch', searchtype='MapSearch')

    solution = planner.searcher()