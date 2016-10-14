import gzip

from collections import deque
from mimo import Stream
from lhc.io.fasta.iterator import FastaFragmentIterator


class StreamFasta(Stream):

    IN = ['fasta_file']
    OUT = ['sequence_fragment']

    async def run(self, ins, outs):
        async for fasta_file in ins.fasta_file:
            with gzip.open(fasta_file, 'rt', encoding='utf-8') if fasta_file.endswith('.gz') else \
                    open(fasta_file, encoding='utf-8') as fileobj:
                iterator = FastaFragmentIterator(fileobj)
                for item in iterator:
                    await outs.sequence_fragment.push(item)
        outs.sequence_fragment.close()


class GetChromosomeSequenceByInterval(Stream):

    IN = ['interval', 'sequence_fragment']
    OUT = ['sequence']

    def __init__(self):
        super().__init__()
        self._fragments = deque()

    async def run(self, ins, outs):
        fragments = self._fragments
        async for interval in ins.interval:
            while len(fragments) > 0 and fragments[0].stop < interval.start:
                fragments.popleft()

            while ins.sequence_fragment.is_open() and (len(fragments) == 0 or fragments[-1].start < interval.stop):
                fragment = await ins.sequence_fragment.pop()
                if interval.start < fragment.stop:
                    fragments.append(fragment)

            sequence = ''.join(fragment.data for fragment in fragments)
            fr = interval.start.get_distance_to(fragments[0].start)
            to = interval.stop.get_distance_to(fragments[0].start)
            await outs.sequence.push(sequence[fr:to])
        outs.sequence.close()
