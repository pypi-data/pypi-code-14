import itertools

from eth_abi import (
    decode_abi,
    decode_single,
    encode_single,
)

from .encoding import encode_hex
from .types import (
    is_array,
)
from .string import (
    coerce_return_to_text,
)
from .abi import (
    get_abi_input_types,
    get_abi_input_names,
    get_indexed_event_inputs,
    exclude_indexed_event_inputs,
    event_abi_to_log_topic,
    normalize_return_type,
)


@coerce_return_to_text
def construct_event_topic_set(event_abi, arguments=None):
    if arguments is None:
        arguments = {}
    if isinstance(arguments, (list, tuple)):
        if len(arguments) != len(event_abi['inputs']):
            raise ValueError(
                "When passing an argument list, the number of arguments must "
                "match the event constructor."
            )
        arguments = {
            arg['name']: [arg_value]
            for arg, arg_value
            in zip(event_abi['inputs'], arguments)
        }

    normalized_args = {
        key: value if is_array(value) else [value]
        for key, value in arguments.items()
    }

    event_topic = event_abi_to_log_topic(event_abi)
    indexed_args = get_indexed_event_inputs(event_abi)
    zipped_abi_and_args = [
        (arg, normalized_args.get(arg['name'], [None]))
        for arg in indexed_args
    ]
    encoded_args = [
        [
            None if option is None else encode_hex(encode_single(arg['type'], option))
            for option in arg_options]
        for arg, arg_options in zipped_abi_and_args
    ]

    topics = [
        [event_topic] + list(permutation)
        if any(value is not None for value in permutation)
        else [event_topic]
        for permutation in itertools.product(*encoded_args)
    ]
    return topics


@coerce_return_to_text
def construct_event_data_set(event_abi, arguments=None):
    if arguments is None:
        arguments = {}
    if isinstance(arguments, (list, tuple)):
        if len(arguments) != len(event_abi['inputs']):
            raise ValueError(
                "When passing an argument list, the number of arguments must "
                "match the event constructor."
            )
        arguments = {
            arg['name']: [arg_value]
            for arg, arg_value
            in zip(event_abi['inputs'], arguments)
        }

    normalized_args = {
        key: value if is_array(value) else [value]
        for key, value in arguments.items()
    }

    indexed_args = exclude_indexed_event_inputs(event_abi)
    zipped_abi_and_args = [
        (arg, normalized_args.get(arg['name'], [None]))
        for arg in indexed_args
    ]
    encoded_args = [
        [
            None if option is None else encode_hex(encode_single(arg['type'], option))
            for option in arg_options]
        for arg, arg_options in zipped_abi_and_args
    ]

    topics = [
        list(permutation)
        if any(value is not None for value in permutation)
        else []
        for permutation in itertools.product(*encoded_args)
    ]
    return topics


def coerce_event_abi_types_for_decoding(input_types):
    """
    Event logs use the `sha3(value)` for inputs of type `bytes` or `string`.
    Because of this we need to modify the types so that we can decode the log
    entries using the correct types.
    """
    return [
        'bytes32' if arg_type in {'bytes', 'string'} else arg_type
        for arg_type in input_types
    ]


@coerce_return_to_text
def get_event_data(event_abi, log_entry):
    """
    Given an event ABI and a log entry for that event, return the decoded
    """
    if event_abi['anonymous']:
        log_topics = log_entry['topics']
    else:
        log_topics = log_entry['topics'][1:]

    log_topics_abi = get_indexed_event_inputs(event_abi)
    log_topic_raw_types = get_abi_input_types({'inputs': log_topics_abi})
    log_topic_types = coerce_event_abi_types_for_decoding(log_topic_raw_types)
    log_topic_names = get_abi_input_names({'inputs': log_topics_abi})

    if len(log_topics) != len(log_topic_types):
        raise ValueError("Expected {0} log topics.  Got {1}".format(
            len(log_topic_types),
            len(log_topics),
        ))

    log_data = log_entry['data']
    log_data_abi = exclude_indexed_event_inputs(event_abi)
    log_data_raw_types = get_abi_input_types({'inputs': log_data_abi})
    log_data_types = coerce_event_abi_types_for_decoding(log_data_raw_types)
    log_data_names = get_abi_input_names({'inputs': log_data_abi})

    # sanity check that there are not name intersections between the topic
    # names and the data argument names.
    duplicate_names = set(log_topic_names).intersection(log_data_names)
    if duplicate_names:
        raise ValueError(
            "Invalid Event ABI:  The following argument names are duplicated "
            "between event inputs: '{0}'".format(', '.join(duplicate_names))
        )

    decoded_log_data = decode_abi(log_data_types, log_data)
    normalized_log_data = [
        normalize_return_type(data_type, data_value)
        for data_type, data_value
        in zip(log_data_types, decoded_log_data)
    ]

    decoded_topic_data = [
        decode_single(topic_type, topic_data)
        for topic_type, topic_data
        in zip(log_topic_types, log_topics)
    ]
    normalized_topic_data = [
        normalize_return_type(data_type, data_value)
        for data_type, data_value
        in zip(log_topic_types, decoded_topic_data)
    ]

    event_args = dict(itertools.chain(
        zip(log_topic_names, normalized_topic_data),
        zip(log_data_names, normalized_log_data),
    ))

    event_data = {
        'args': event_args,
        'event': event_abi['name'],
        'logIndex': log_entry['logIndex'],
        'transactionIndex': log_entry['transactionIndex'],
        'transactionHash': log_entry['transactionHash'],
        'address': log_entry['address'],
        'blockHash': log_entry['blockHash'],
        'blockNumber': log_entry['blockNumber'],
    }

    return event_data
