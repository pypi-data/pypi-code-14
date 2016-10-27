from parse_data import parse_data
from console_printer import ConsolePrinter
from restipy.cli.local_store import LocalStore
from restipy.execution import CookbookExecutor

def do(args):
    printer = ConsolePrinter(
        quiet=args.quiet,
        format_type=args.format_type,
        verbose=args.verbose)

    input_data = {}
    local_store = LocalStore(args.save_path, args.save_filename)
    input_data['vars'] = local_store.get_data()

    cli_input_data = parse_data(args.data)
    input_data['vars'].update(cli_input_data)

    filter_func = None
    if args.recipe_name:
        filter_func = lambda x: x['id'] == args.recipe_name

    cookbook_executor = CookbookExecutor(
        filter_func=filter_func
        )
    try:
        result_generator = cookbook_executor.execute(
            cookbook_file=args.cookbook_file,
            input_data=input_data)

        for result in result_generator:
            printer.out(result)
    finally:
        local_store.dump();
