import todoist
from base import dlog
import elo
import os
import argparse
import sys
from datetime import datetime
from planner import PriorityPlanner
import time
import yaml


def get_config(args):
    fs = open(args.config)
    cfg = yaml.load(fs)
    fs.close()
    return cfg

def get_app(cfg):

    app = todoist.Todoist()
    app.init(cfg)

    return app

def show(app, args, cfg):
    if args.show_cmd == "api_token":
        print app.user.api_token
    elif args.show_cmd == "stats":
        print app.get_stats()
    elif args.show_cmd == "config":
        print yaml.dump(cfg)

def rank(app, args, cfg):
    projects = app.get_projects()

    for p in projects:
        if p.name in cfg["rank_skip_projects"]:
            dlog("Skip project: " + p.name)
            continue
        if args.project is not None and p.name != args.project:
            dlog("Skip project: " + p.name)
            continue
        print p.name, "[", len(p.tasks), "]"
        tasks = elo.sort(p.tasks)
        p.tasks = tasks
        #app.update_project(p)

        i = 0
        for t in p.tasks:
            app.update_task(t, "item_order", i)
            i += 1
        app.update()

    print("OK")

def choose_func(planner_item):
    tasks = planner_item.item.tasks
    if len(tasks) > 0:
        r = tasks[0]
        planner_item.item.tasks = tasks[1:]
        return r
    else:
        return None

def schedule(app, res, offset=0):
    """ offset is the position that we should start plan for today's taks. That
        means if today we've finished n tasks, we skip the first n finished
        tasks and start to plan the n+1 task.
    """
    tasks_per_day = 10
    if offset > 10:
        print("offset too large: ", offset)
        offset = 7 # 10 - 7 = 3, plan 3 tasks for today if we've already done more than 10 today

    j = offset
    #print("offset is %d" % offset)
    for task in res:
        # schedule t for today
        #print "schedule for today: %d" % j
        seq = j
        #tp.schedule_for(t.id, j)
        day = seq / tasks_per_day
        minute = seq % tasks_per_day
        app.update_task(task, "date_string", "{day} days at 22:{minute:02}".format(day=day, minute=minute))
        #t: Pytodoist Task
        app.mark_as_planned(task)
        j += 1

def plan(app, args, cfg):
    def adjust_for_completed_tasks(stats):
        total = 0
        done = 0
        # completed tasks are sorted from new to old
        tasks = app.get_completed_tasks()
        now = datetime.now()
        for t in tasks:
            if (now - t.ts_done).total_seconds() > 3 * 24 * 3600:
                # larger than 3 days
                break
            pid = t.pid
            if stats.has_key(pid):
                stats[pid] += 1
            else:
                stats[pid] = 1
            total += 1

            if t.done:
                done += 1
        stats['total'] = total
        stats['done'] = done

    projects = app.get_projects()
    project_blacklist = cfg["plan_skip_projects"]
    for p in projects[:]:
        if p.name in project_blacklist:
            print("discard project:", p.name)
            projects.remove(p)
    planner = PriorityPlanner(cfg, preprocess=adjust_for_completed_tasks)

    n = 0
    res = []
    for t in planner.plan(projects, choose_func):
        res.append(t)
        n += 1
        if n >= args.limit:
            break
    offset = app.num_tasks_completed_today()
    print(res)
    #planner.run(projects)
    schedule(app, res, offset=offset)
    app.update()


def check_positive_int(val):
    ival = int(val)
    if ival <= 0:
        raise argparse.ArgumentTypeError("%s is not a positive integer" % val)
    return ival

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help="config file path")
    parser.set_defaults(config=os.path.expanduser("~") + "/.taski.yaml")
    subparsers = parser.add_subparsers(help='available commands')

    plan_parser = subparsers.add_parser('plan', help='plan tasks')
    plan_parser.add_argument('--limit', type=check_positive_int, default=30)
    plan_parser.set_defaults(func=plan)

    rank_parser = subparsers.add_parser('rank', help='rank tasks')
    rank_parser.add_argument('--project')
    rank_parser.set_defaults(func=rank)

    show_parser = subparsers.add_parser('show', help='show things')
    show_parser.add_argument('show_cmd', help='show [api_token|stats]')
    show_parser.set_defaults(func=show)

    args = parser.parse_args()
    cfg = get_config(args)
    app = get_app(cfg)
    args.func(app, args, cfg)
