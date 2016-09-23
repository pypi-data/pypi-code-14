def get_fn_argnames(func):
	'''
	Given a function, find its argument and keyword argument names.
	'''
	arg_count = func.func_code.co_argcount
	kwarg_count = 0
	if func.func_defaults:
		kwarg_count = len(func.func_defaults)
		arg_count = arg_count - kwarg_count

	fn_args = func.func_code.co_varnames[:arg_count]
	fn_kwargs = func.func_code.co_varnames[arg_count:arg_count + kwarg_count]

	return fn_args, fn_kwargs
