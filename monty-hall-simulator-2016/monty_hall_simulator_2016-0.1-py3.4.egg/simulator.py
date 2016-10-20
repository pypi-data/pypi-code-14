from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from game import play_game

def simulate(trials):
    pool = ThreadPool()

    half_trials = trials // 2
    switch_wins = 0
    non_switch_wins = 0

    switch_results = pool.map(play_game, [True] * half_trials)
    non_switch_results = pool.map(play_game, [False] * half_trials)
    switch_wins = switch_results.count(True)
    non_switch_wins = non_switch_results.count(True)

    return (switch_wins / half_trials, non_switch_wins / half_trials)
