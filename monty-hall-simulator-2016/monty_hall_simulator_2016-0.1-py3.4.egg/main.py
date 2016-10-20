import click
from monty_hall_simulator_2016.simulator import simulate

@click.command()
@click.option('--trials', default=1000, help='Number of trials to simulate')
def run_simulation(trials):
    click.echo('Pick a door, any door....')
    return
    switch_rate, non_switch_rate = simulate(trials)
    click.echo('Trials run: %d' % trials)
    click.echo('Switch win rate: %f' % switch_rate)
    click.echo('Non-switch win rate: %f' % non_switch_rate)
