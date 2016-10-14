from lhc.binf.genomic_coordinate import GenomicInterval as Interval
from mimo import Stream, azip


class StreamChromosomeWindows(Stream):

    IN = ['chromosome_id', 'chromosome_length']
    OUT = ['chromosome_interval']

    def __init__(self, window_length):
        super().__init__()
        self.window_length = window_length

    async def run(self, ins, outs):
        length = self.window_length
        async for chromosome_id, chromosome_length in azip(ins.chromosome_id, ins.chromosome_length):
            for fr in range(0, chromosome_length, length):
                await outs.chromosome_interval.push(Interval(fr, fr + length, chromosome=chromosome_id))
        outs.chromosome_interval.close()
