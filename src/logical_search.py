import logging

from mapplanner.search.mapsearch import MapSearch
from mapreasoner.spatial_reasoning import MapReasoning


class LogicalMapSearch(MapSearch, MapReasoning):
    def __init__(self):
        pass

    def initialize(self, task, logical_search):
        self.world_model = task.signs
        self.check_pm = task.goal_situation.meanings[1]
        self.active_pm = task.start_situation.meanings[1]
        self.constraints = task.constraints
        self.logic = task.logic
        self.active_map = task.map_precisions
        self.additions = task.additions
        self.exp_actions = []
        self.agents = set()
        self.I_sign = None
        self.I_obj = None
        self.LogicalSearch = logical_search
        # New attributes
        self.cell_map = task.additions[3][0]
        self.cell_coords = task.additions[0][0]
        #
        if task.goal_map:
            self.check_map = task.goal_map.meanings[1]
        else:
            self.check_map = None
        self.MAX_ITERATION = 30
        logging.debug('Start: {0}'.format(self.check_pm.longstr()))
        logging.debug('Finish: {0}'.format(self.active_pm.longstr()))

    def _logic_expand(self):
        closure_sign = self.closure_function()
        return closure_sign
