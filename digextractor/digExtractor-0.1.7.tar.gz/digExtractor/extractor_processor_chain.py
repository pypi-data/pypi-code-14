

def execute_processor_chain(doc, processors):
    t = reduce(processor_chain_reducer, iter(processors), doc)
    return t


def processor_chain_reducer(doc, processor):
    return processor.extract(doc)
