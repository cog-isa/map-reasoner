import argparse
import json

from mapplanner.grounding.json_grounding import Problem
from mapplanner.grounding.json_grounding import spatial_ground
from logical_search import LogicalMapSearch


def get_problem(args):
    domain = 'domain.json'
    task = 'task' + args.task_number + '.json'
    path = args.benchmark

    domain_file = path + domain
    problem_file = path + task

    with open(problem_file) as data_file1:
        problem_parsed = json.load(data_file1)
    with open(domain_file) as data_file2:
        signs_structure = json.load(data_file2)

    problem = Problem(signs_structure, problem_parsed, None)
    return problem


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    argparser.add_argument(dest='benchmark')
    argparser.add_argument(dest='task_number')
    args = argparser.parse_args()

    problem = get_problem(args)
    task = spatial_ground(problem, 'agent', 'spatial')

    log_search = LogicalMapSearch(task, logical_search=True)
    closure = log_search._logic_expand()



