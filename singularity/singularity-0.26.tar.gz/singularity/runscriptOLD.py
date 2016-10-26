def get_runscript_parameters(runscript,name,version,description=None):
    '''get_parameters is a general wrapper for language-specific methods to
    extract acceptable input arguments from a script
    :param runscript: the path to the runscript
    :param name: the name for the container
    :param version: a unique ID for the container, should be a unique hash
    :param description: a description of the container, if none provided, name is used
    '''
    language = detect_language(runscript)

    params = None
    json_spec = None

    if language == 'python':
        params = get_parameters_python(runscript)

    # Finally, make a boutiques json object with the parameters
    if params != None:
        json_spec = get_boutiques_json(name=name,
                                       version=version,
                                       inputs=params,
                                       command=name,
                                       description=description)

    return json_spec


def get_parameters_python(runscript):
    '''get_parameters_python returns parameters for a python script
    :param runscript: the path to the runscript, or a string of the runscript
    '''
    tmpdir = tempfile.mkdtemp()
    # Move runscript to a temporary directory, as python for import
    tmp_module = "%s/chickenfingers.py" %(tmpdir)

    # If the runscript exists as a file, copy it, else write it
    if os.path.exists(runscript):
       shutil.copy(runscript,tmp_module)
    else:
       write_file(tmp_module,runscript)

    try:
        rs = imp.load_source('get_parser',tmp_module)
        parser = rs.get_parser()
        inputs = get_inputs_python(parser)
        return inputs        
    except:
        print("Cannot find get_parser function in runscript, make sure to use singularity template (shub --runscript py) for your runscript template!")


def get_inputs_python(parser,include_help=False):
    '''get_inputs_python parses an argparse object to return container inputs
    :param parser: an argparse parser.
    :param include_help: include -h and --help, default False
    '''
    # We will save a list of {'flags':[...],
    #                         'required':True/False,
    #                         'name':''...
    #                         'default': ..,
    #                         'type':bool,
    #                         'choices':OPTIONAL,
    #                         'description':'This is...']}

    inputs = []
    actions = parser.__dict__['_option_string_actions']

    for command_arg, opts in actions.iteritems():
        if include_help == False and command_arg in ["-h","--help"]:
            pass
        else:
            print("Adding %s input to spec..." %(command_arg))
            opt = {"flags":opts.option_strings,
                   "required":opts.required,
                   "name":opts.dest,
                   "default":opts.default,
                   "type":opts.type,
                   "choices":opts.choices,
                   "description":opts.help}
            inputs.append(opt)
    return inputs
