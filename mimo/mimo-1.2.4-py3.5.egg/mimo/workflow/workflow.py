import asyncio

from collections import defaultdict
from uuid import uuid4
from lhc.graph import NPartiteGraph
from mimo.io import Input, Output, IOSet
from mimo.stream import Stream, StreamFromInput, StreamToOutput
from mimo.workflow.node import Node


class Workflow(Stream):
    def __init__(self, ins=tuple(), outs=tuple(), *, name=None, threshold=100, loop=None):
        super().__init__(ins, outs, name=name)
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop
        self.threshold = threshold

        self.graph = NPartiteGraph(n=3)
        self.streams = {}
        self.input_sets = {}
        self.output_sets = {}
        self.inputs = {}
        self.outputs = {}
        self.workflow_inputs = defaultdict(set)
        self.workflow_outputs = {}

    def __str__(self):
        visited = set()
        edge = '    "{}" -> "{}" [{}];'
        graph = self.graph
        res = ['digraph {} {{'.format(graph.name)]
        for id, stream in self.streams.items():
            res.append('    "{}" [label="{}"];'.format(id, stream.name))
            if isinstance(stream, Workflow):
                res.append(str(stream).replace('digraph', 'subgraph'))
        for fr in graph.partitions[0]:
            for output in graph.get_children(fr):
                for input in graph.get_children(output):
                    for to in graph.get_children(input):
                        parameters = ['sametail="{}"'.format(output), 'samehead="{}"'.format(input)]
                        if output not in visited:
                            parameters.append('taillabel="{}"'.format(self.outputs[output].name))
                            visited.add(output)
                        if input not in visited:
                            parameters.append('headlabel="{}"'.format(self.inputs[input].name))
                        res.append(edge.format(fr, to, ', '.join(parameters)))
        res.append('}')
        return '\n'.join(res)

    def start(self):
        self._loop.run_until_complete(self.run())

    async def run(self, ins=None, outs=None):
        if ins is not None:
            for workflow_input, input_node in self.workflow_inputs.items():
                self.streams[input_node.stream_id].input = ins[workflow_input]
        if outs is not None:
            for workflow_output, output_node in self.workflow_outputs.items():
                self.streams[output_node.stream_id].output = outs[workflow_output]
        tasks = [stream.run(self.input_sets[stream_id], self.output_sets[stream_id])
                 for stream_id, stream in self.streams.items()]
        await asyncio.gather(*tasks)
        if outs:
            for out in outs:
                out.close()

    def add_stream(self, stream):
        """
        Add a stream to the workflow and return a Node that can be connected to other nodes via `pipe`.
        :param stream: stream to be added to workflow
        :return: node that can be connected to other node
        :rtype: Node
        """
        stream_id, input_ids, output_ids = self._get_identifiers(stream)
        self._add_vertices(stream, stream_id, input_ids, output_ids)
        self._add_edges(stream_id, input_ids, output_ids)
        return Node(self, stream_id, input_ids, output_ids)

    def connect_workflow_input(self, node, *, workflow_input=None, node_input=None):
        """
        Connect a node (returned by `add_stream`) to a workflow input
        :param Node node: node to connect
        :param str workflow_input: name of workflow input
        :param str node_input: name of node input
        :return:
        """
        if workflow_input is None:
            if len(self.ins) == 1:
                workflow_input = self.ins[0]
            else:
                msg = 'Workflow has {} possible connections; {} and {}'
                raise ValueError(msg.format(len(self.ins), ', '.join(self.ins[:-1]), self.ins[-1]))

        if workflow_input in self.workflow_inputs:
            input_node = self.workflow_inputs[workflow_input]
        else:
            stream = StreamFromInput(None)
            input_node = self.add_stream(stream)
            self.workflow_inputs[workflow_input] = input_node
        input_node.pipe(node, input=node_input)

    def connect_workflow_output(self, node, *, workflow_output=None, node_output=None):
        """
        Connect a node (returned by `add_stream') to a workflow output
        :param node: node to connect
        :param workflow_output: name of workflow output
        :param node_output: name of node output
        :return:
        """
        if workflow_output is None:
            if len(self.outs) == 1:
                workflow_output = self.outs[0]
            else:
                msg = 'Workflow has {} possible connections; {} and {}'
                raise ValueError(msg.format(len(self.outs), ', '.join(self.outs[:-1]), self.outs[-1]))

        if workflow_output in self.workflow_outputs:
            output_node = self.workflow_outputs[workflow_output]
        else:
            stream = StreamToOutput(None)
            output_node = self.add_stream(stream)
            self.workflow_outputs[workflow_output] = output_node
        node.pipe(output_node, output=node_output)

    def _get_identifiers(self, stream):
        return str(uuid4())[:8],\
               {name: str(uuid4())[:8] for name in stream.ins},\
               {name: str(uuid4())[:8] for name in stream.outs}

    def _add_vertices(self, stream, stream_id, input_ids, output_ids):
        self.streams[stream_id] = stream
        self.input_sets[stream_id] = IOSet(Input(name, self.threshold, stream=stream_id) for name in stream.ins)
        self.output_sets[stream_id] = IOSet(Output(name, stream=stream_id) for name in stream.outs)

        self.graph.add_vertex(stream_id, 0)
        for input, input_id in input_ids.items():
            self.inputs[input_id] = self.input_sets[stream_id][input]
            self.graph.add_vertex(input_id, 1)
        for output, output_id in output_ids.items():
            self.outputs[output_id] = self.output_sets[stream_id][output]
            self.graph.add_vertex(output_id, 2)

    def _add_edges(self, stream_id, input_ids, output_ids):
        for input, in_id in input_ids.items():
            self.graph.add_edge(in_id, stream_id)
        for output, out_id in output_ids.items():
            self.graph.add_edge(stream_id, out_id)
