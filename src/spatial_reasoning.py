from mapplanner.grounding.semnet import Sign


class MapReasoning:
    def __init__(self):
        pass

    def initialize(self, cell_map, cell_coords, world_model):
        self.cell_map = cell_map
        self.cell_coords = cell_coords
        self.world_model = world_model

    def closure_function(self):
        cell_map = self.get_cells(self.additions[1], self.additions[0])
        #cell_map = self.cell_map
        # cell_coords = self.cell_coords
        # signs = self.signs
        dummy = []
        for key in cell_map:
            dummy.append(cell_map[key])
        dummy_set = set()

        for i in range(len(dummy)):
            dummy_set.update(dummy[i])

        items = list(dummy_set - {0, 'agent', 'border-1', 'border-2', 'border-3', 'border-4'})

        closure_sign = Sign('closure')
        closure_meaning = closure_sign.add_meaning()
        for i in items:
            new_event = self.direction_reas(i)
            self.add_to_closure(closure_sign, closure_meaning, new_event)

        return closure_sign

    def add_to_closure(self, closure_sign, closure_meaning, new_event):
        signs = self.world_model
        if isinstance(new_event, list):
            result = new_event
            for item in result:
                if item == result[0]:
                    item_cm = signs[item].add_meaning()
                    connector = closure_meaning.add_feature(item_cm, zero_out=True)
                    closure_sign.add_out_meaning(connector)
                    connector_copy = connector
                else:
                    item_cm = signs[item].add_meaning()
                    connector_next = closure_meaning.add_feature(item_cm, connector_copy.in_order, zero_out=True)
                    closure_sign.add_out_meaning(connector_next)
                    connector_copy = connector_next

    def get_cells(self, obj_info, cells):

        objects = obj_info[0]['objects']
        sit_cells = cells[0]
        obj_in_cells = {}

        for cell in sit_cells:
            obj_in_cells[cell] = set()

        for cell in sit_cells:
            x1 = sit_cells[cell][0]
            y1 = sit_cells[cell][1]
            x2 = sit_cells[cell][2]
            y2 = sit_cells[cell][3]

            for obj in objects:
                obj_x = objects[obj]['x']
                obj_y = objects[obj]['y']

                if (x1 < obj_x) & (obj_x < x2) & (y1 < obj_y) & (obj_y < y2):
                    obj_in_cells[cell].add(obj)
                else:
                    obj_in_cells[cell].add(0)
        for key in obj_in_cells:
            if len(obj_in_cells[key]) != 1:
                obj_in_cells[key] -= {0}
        return obj_in_cells

    def direction_reas(self, item):
        cell_map = self.get_cells(self.additions[1], self.additions[0])
        #cell_map = self.cell_map
        cell_coords = self.cell_coords

        item_location = None

        for key in cell_map:
            if item in cell_map[key]:
                item_location = key

        item_x1, item_y1, item_x2, item_y2 = cell_coords[item_location]
        cell_size = item_x2 - item_x1

        new_cell_0_x1 = item_x1 - cell_size
        new_cell_0_y1 = item_y1 - cell_size

        item_focus = {}

        cell_number = 0
        # Create 9 cells around an item
        # x1, y1 - coordinates of a left-up corner
        # x2, y2 - coordinates of a right-down corner
        for i in range(3):
            for j in range(3):
                x1 = new_cell_0_x1 + i * cell_size
                y1 = new_cell_0_y1 + j * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                item_focus[item + '_cell-' + str(cell_number)] = [x1, y1, x2, y2]
                cell_number += 1

        equal_cells = {}
        focus_intersec = []
        for key1 in cell_coords:
            for key2 in item_focus:
                if self.cells_equal(cell_coords[key1], item_focus[key2]):
                    equal_cells[key1 + ', ' + key2] = 'equal'
                    focus_intersec.append(key1)

        spatial_information = []
        for i in focus_intersec:
            spatial_information.append(self.spatial_direction(i))

        direction = self.absorb(self.exclude(spatial_information))
        if len(direction) == 1:
            print(item + ' ' + direction[0] + ' agent')
            return [item, 'agent', direction[0]]

        # Return item_focus, equal_cells, focus_intersec

    def cells_equal(self, cell_1, cell_2):
        cell_1_x1, cell_1_y1, cell_1_x2, cell_1_y2 = cell_1
        cell_2_x1, cell_2_y1, cell_2_x2, cell_2_y2 = cell_2

        if cell_2_x1 >= cell_1_x1 and cell_2_y1 >= cell_1_y1 and cell_2_x2 <= cell_1_x2 and cell_2_y2 <= cell_1_y2:
            return True
        else:
            return False

    def spatial_direction(self, cell):
        # Keeps structure of a focus
        cell_struct = {'cell-0': 'above-left', 'cell-1': 'left', 'cell-2': 'below-left', 'cell-3': 'above',
                       'cell-4': 'center', 'cell-5': 'below', 'cell-6': 'above-right', 'cell-7': 'right',
                       'cell-8': 'below-right'}
        return cell_struct[cell]

    def exclude(self, spatial_information):
        # In: spat = ['above', 'center', 'above-right', 'right']
        # Out: ['above', 'above-right', 'right']
        # In: spat = ['above', 'center', 'above-right', 'right', 'below', 'below-right']
        # Out: ['right']
        if 'center' in spatial_information:
            spatial_information.remove('center')

        answer = spatial_information.copy()

        if ('above' in answer) and ('below' in answer):
            answer.remove('above')
            answer.remove('below')
        if ('left' in answer) and ('right' in answer):
            answer.remove('left')
            answer.remove('right')
        if ('above-left' in answer) and ('below-left' in answer):
            answer.remove('above-left')
            answer.remove('below-left')
        if ('above-right' in answer) and ('below-right' in answer):
            answer.remove('above-right')
            answer.remove('below-right')
        if ('above-left' in answer) and ('above-right' in answer):
            answer.remove('above-left')
            answer.remove('above-right')
        if ('below-left' in answer) and ('below-right' in answer):
            answer.remove('below-left')
            answer.remove('below-right')
        return answer

    def absorb(self, spatial_information):
        # In: spat = ['above', 'center', 'above-right', 'right']
        # Out: ['center', 'above-right']
        # In: spat = ['above', 'center', 'above-right', 'right', 'below', 'below-right']
        # Out: ['center', 'above-right', 'below-right']
        answer = spatial_information.copy()

        if ('right' in answer) and (('above-right' in answer) or ('below-right' in answer)):
            answer.remove('right')
        if ('left' in answer) and (('above-left' in answer) or ('below-left' in answer)):
            answer.remove('left')
        if ('above' in answer) and (('above-right' in answer) or ('above-left' in answer)):
            answer.remove('above')
        if ('below' in answer) and (('below-right' in answer) or ('below-left' in answer)):
            answer.remove('below')
        return answer
