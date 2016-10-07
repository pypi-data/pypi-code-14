from collections import Counter
from mimo import Stream
from lhc.binf.sequence.reverse_complement import reverse_complement


class GetTriplets(Stream):

    IN = ['sequence']
    OUT = ['triplet']

    async def run(self, ins, outs):
        async for sequence in ins.sequence:
            triplets = Counter()
            for i in range(len(sequence) - 2):
                triplet = sequence[i:i + 3]
                if triplet[1] not in 'ctCT':
                    triplet = reverse_complement(triplet)
                triplets[triplet] += 1
            await outs.triplet.push(triplets)
        outs.triplet.close()
