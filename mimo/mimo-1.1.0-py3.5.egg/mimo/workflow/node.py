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
        :param output: name of the output connection (default: None)
        :param input: name of the input connection (default: None)
        :return: stream connected to
        """
        if len(self.output_ids) == 0:
            raise ValueError('{} has no output to pipe from'.format(self.workflow.streams[self.stream_id]))
        elif len(step.input_ids) == 0:
            raise ValueError('{} has no input to pipe to'.format(self.workflow.streams[step.stream_id]))

        output_id = self._get_id(self.output_ids, self.stream_id, output)
        input_id = self._get_id(step.input_ids, step.stream_id, input)
        self.workflow.graph.add_edge(output_id, input_id)
        self.workflow.outputs[output_id].pipe(self.workflow.inputs[input_id])
        return step

    def push(self, item, input=None):
        input_id = self._get_id(self.input_ids, self.stream_id, input)
        self.workflow.inputs[input_id].put_nowait(item)

    def close(self, input=None):
        input_id = self._get_id(self.input_ids, self.stream_id, input)
        self.workflow.inputs[input_id].close()

    def _get_id(self, id_map, stream_id, name=None):
        if name is None:
            if len(id_map) == 1:
                id_ = next(iter(id_map.values()))
            else:
                msg = '{} has multiple connections'
                raise ValueError(msg.format(self.workflow.streams[stream_id]))
        else:
            id_ = id_map[name]
        return id_
