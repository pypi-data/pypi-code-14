CODE_BUCKET = 'tiros-lambda'
CODE_KEY = 'tiros-lambda.zip'
FUN_NAME = 'TirosLambda'
FUN_RUNTIME = 'python2.7'
FUN_HANDLER = 'tiros_lambda.lambda_handler'
FUN_DESCRIPTION = 'Tiros Lambda'
FUN_TIMEOUT = 300


def functions(client):
    res = client.list_functions()
    funs = [d['FunctionName'] for d in res['Functions']]
    m = res.get('NextMarker')
    while m:
        res = client.list_functions(Marker=m)
        funs += [d['FunctionName'] for d in res['Functions']]
        m = res.get('NextMarker')
    return funs


def make_lambda(session, role):
    client = session.client('lambda')
    funs = functions(client)
    if FUN_NAME not in funs:
        client.create_function(
            FunctionName=FUN_NAME,
            Runtime=FUN_RUNTIME,
            Role=role,
            Handler=FUN_HANDLER,
            Code={
                'S3Bucket': CODE_BUCKET,
                'S3Key': CODE_KEY
            },
            Description=FUN_DESCRIPTION,
            Timeout=FUN_TIMEOUT)
    else:
        client.update_function_code(
            FunctionName=FUN_NAME,
            S3Bucket=CODE_BUCKET,
            S3Key=CODE_KEY)
