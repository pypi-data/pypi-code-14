class Node:
    __slots__ = ('workflow', 'stream_id', 'input_ids', 'output_ids')

    def __init__(self, workflow, stream_id, input_ids, output_ids):
        self.workflow = workflow
        self.stream_id = stream_id
        self.input_ids = input_ids
        self.output_ids = output_ids

    def pipe(self, step, output=None, input=None):
        """
        Pipe the output of one stream to the input of another. If there are more than one outputs or inputs, the
        specific output/input must be specified.
        :param step: stream to connect to
        :param output: name of the output io (default: None)
        :param input: name of the input io (default: None)
        :return: stream connected to
        """
        if len(self.output_ids) == 0:
            raise ValueError('{} has no output to pipe from'.format(self.workflow.streams[self.stream_id]))
        elif len(step.input_ids) == 0:
            raise ValueError('{} has no input to pipe to'.format(self.workflow.streams[step.stream_id]))

        output_id = self.get_output(output)
        input_id = step.get_input(input)
        self.workflow.graph.add_edge(output_id, input_id)
        self.workflow.outputs[output_id].pipe(self.workflow.inputs[input_id])
        return step

    def push(self, item, input=None):
        input_id = self.get_input(input)
        self.workflow.inputs[input_id].put_nowait(item)

    def close(self, input=None):
        input_id = self.get_input(input)
        self.workflow.inputs[input_id].close()

    def get_input(self, name=None):
        return self._get_id(self.input_ids, name)

    def get_output(self, name=None):
        return self._get_id(self.output_ids, name)

    def _get_id(self, id_map, name=None):
        if name is None:
            if len(id_map) == 1:
                id_ = next(iter(id_map.values()))
            else:
                msg = '{} has {} possible connections; {} and {}'
                connections = list(id_map.keys())
                raise ValueError(msg.format(self.workflow.streams[self.stream_id].name, len(id_map), ', '.join(connections[:-1]), connections[-1]))
        else:
            id_ = id_map[name]
        return id_
