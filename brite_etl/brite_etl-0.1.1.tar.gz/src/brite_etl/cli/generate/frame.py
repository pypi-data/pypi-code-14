import click
import os
import brite_etl
import pkg_resources
from string import Template


@click.command('frame')
@click.option(
    '--name',
    prompt='Name of the DataFrame (Must be same name as the CSV file (sans ".csv") ' +
    'for auto sourcing to work). EX - accounting, revision_items'
)
@click.option(
    '--classname',
    prompt='Class name of the DataFrame (Usually the same as name, but capitialized and without underscores). ' +
    'EX - Accounting, RevisionItems'
)
@click.option('--prepared/--not-prepared', default=False, prompt='Is this a prepared DataFrame')
@click.option('--force', is_flag=True, default=False)
def generate_frame(**params):

    def _write_file(filepath, filename, content):
        with open(os.path.join(filepath, filename), 'w') as output_file:
            # Run string.Template substitution on data_template
            # using data from 'row' as source and write to
            # 'output_file'.
            output_file.write(result)

    template = Template(pkg_resources.resource_string(__name__, 'templates/frame_template.py'))
    result = template.substitute(**params)

    filepath = os.path.join(os.path.dirname(brite_etl.__file__), 'frames')
    filepath = os.path.join(filepath, 'prepared') if params['prepared'] else filepath
    # filepath = os.path.dirname(filepath.__file__)
    filename = params['name'] + '.py'

    if os.path.isfile(os.path.join(filepath, filename)):
        if params['force']:
            click.secho('Overwriting {0}...'.format(params['name']),
                        fg='yellow'
                        )
            _write_file(filepath, filename, result)
        else:
            click.secho('{0} already exists... use --force to overwrite'.format(params['name']),
                        fg='red'
                        )
    else:
        _write_file(filepath, filename, result)


@click.command('regenerate_all_frames')
@click.confirmation_option(help='Are you sure you want to regenerate all frames? This will overwrite them all, and ' +
                           'cannot be undone.')
def regenerate_all_frames():
    import os
    import pydash

    _FRAMES = [
        'account_history',
        'additional_interests',
        'addresses',
        'agencies',
        'builder_obj',
        'builder_obj_parsed',
        'catastrophes',
        'claim_items',
        'claims',
        'claims_changes',
        'claims_contacts',
        'claims_payments',
        'claims_payments_item_amounts',
        'claims_perils',
        'claims_recoveries',
        'commission_accounting',
        'commission_payments',
        'committed_revisions',
        'committed_revisions_all',
        'credit_reports',
        'custom_data',
        'emails',
        'files',
        'inactive_claims',
        'inspectors',
        'item_questions',
        'lines',
        'losses_incurred',
        'losses_incurred_items',
        'mortgagees',
        'phones',
        'policies',
        'policy_change_log',
        'policy_payments',
        'policy_terms',
        'policy_types',
        'policyholders',
        'premium_records',
        'properties',
        'property_items',
        'quotes',
        'quoting_revisions',
        'recovery_history',
        'recovery_history_snapshot',
        'return_premiums',
        'revision_items',
        'revisions',
        'x_report_locations'
    ]

    _PREPARED_FRAMES = [
        'accounting',
        'additional_interests',
        'agencies',
        'claim_payments',
        'claims',
        'commission_accounting',
        'commission_payments',
        'credit_reports',
        'item_changes',
        'item_range',
        'item_state',
        'item_transactions',
        'items',
        'lines',
        'mortgagees',
        'policies',
        'policy_changes',
        'policy_earned',
        'policy_range',
        'policy_state',
        'policy_types',
        'policyholders',
        'premium_records',
        'primary_policyholders',
        'properties',
        'quotes',
        'return_premiums',
        'revisions',
        'written_premium'
    ]

    def _call_generate(frame, prepared):
        _prepared = '--prepared' if prepared else '--not-prepared'
        # Turns 'recovery_history_snapshot' into 'RecoveryHistorySnapshot'
        _classname = pydash.title_case(frame.replace('_', ' ')).replace(' ', '')
        # This should be redone to call generate_frame directly. But it's rarely used so not a high priority.
        os.system('python -m brite_etl generate frame --name {0} --classname {1} {2} --force'.format(frame, _classname, _prepared))

    for frame in _FRAMES:
        _call_generate(frame, False)

    for frame in _PREPARED_FRAMES:
        _call_generate(frame, True)
