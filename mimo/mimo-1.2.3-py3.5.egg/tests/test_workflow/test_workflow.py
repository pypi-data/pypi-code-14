import asyncio
import unittest

from mimo import Workflow, Stream
from mimo.io import Input, Output, IOSet


class TestWorkflow(unittest.TestCase):
    def test_start(self):
        workflow = Workflow()
        stream1 = Stream(outs=['item'], fn=iterator_stream)
        stream2 = Stream(ins=['item'], fn=collect_stream, state=[])
        step1 = workflow.add_stream(stream1)
        step2 = workflow.add_stream(stream2)
        step1.pipe(step2)

        workflow.start()

        self.assertEqual(list(range(100)), stream2.state)

    def test_add_stream(self):
        stream = Stream(['a'], ['b'])
        workflow = Workflow()
        node = workflow.add_stream(stream)

        self.assertEqual({node.stream_id: stream}, workflow.streams)
        self.assertEqual(stream.ins, list(conn.name for conn in workflow.inputs.values()))
        self.assertEqual(stream.outs, list(conn.name for conn in workflow.outputs.values()))
        self.assertEqual(workflow, node.workflow)
        self.assertIn(node.stream_id, workflow.streams)
        self.assertEqual(set(workflow.inputs), set(node.input_ids.values()))
        self.assertEqual(set(workflow.outputs), set(node.output_ids.values()))

    def test_nested_workflow(self):
        workflow = Workflow(ins=['item'], outs=['item'])
        stream = Stream(ins=['item'], outs=['item'], fn=process_stream)
        node = workflow.add_stream(stream)
        workflow.connect_workflow_input(node)
        workflow.connect_workflow_output(node)

        input = Input('item')
        input._queue.extend(range(10))
        input.close()
        output = Output('item')
        output2 = Input('item')
        output.pipe(output2)
        input_set = IOSet([input])
        output_set = IOSet([output])

        loop = asyncio.get_event_loop()
        loop.run_until_complete(workflow.run(input_set, output_set))

        self.assertEqual([0, 2, 4, 6, 8, 10, 12, 14, 16, 18], list(output2._queue))


async def iterator_stream(ins, outs, state):
    for item in iter(range(100)):
        await outs.item.push(item)
    outs.item.close()


async def collect_stream(ins, outs, state):
    async for item in ins.item:
        state.append(item)

async def process_stream(ins, outs, state):
    async for item in ins.item:
        await outs.item.push(2 * item)
    outs.item.close()


if __name__ == '__main__':
    unittest.main()
