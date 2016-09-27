import gzip
import heapq

from itertools import islice
from mimo import Stream
from lhc.io.fasta.wrapper import FastaWrapper


class StreamFasta(Stream):

    IN = ['fasta_file']
    OUT = ['sequence_fragment']

    async def run(self, ins, outs):
        async for fasta_file in ins.fasta_file:
            with gzip.open(fasta_file, 'rt', encoding='utf-8') if fasta_file.endswith('.gz') else \
                    open(fasta_file, encoding='utf-8') as fileobj:
                iterator = FastaWrapper(fileobj)
                for item in iterator:
                    await outs.sequence_fragment.push(item)
        outs.sequence_fragment.close()


class GetChromosomeSequenceByInterval(Stream):

    IN = ['interval', 'sequence_fragment']
    OUT = ['sequence']

    async def run(self, ins, outs):
        fragments = []
        while ins.interval.is_open():
            interval = await ins.interval.pop()
            while len(fragments) > 0 and fragments[0] < interval.start:
                heapq.heappop(fragments)

            if ins.variant.is_open():
                if len(fragments) == 0:
                    fragment = await ins.variant.pop()
                    heapq.heappush(fragments, (fragment.stop, fragment))
                while ins.sequence_fragment.is_open() and fragments[-1].pos < interval.stop:
                    fragments.append(await ins.variant.pop())

            if fragments[-1].pos < interval.stop:
                await outs.variant.push(list(fragments))
            else:
                await outs.variant.push(list(islice(fragments, 0, len(fragments) - 1)))

        outs.variant.close()
