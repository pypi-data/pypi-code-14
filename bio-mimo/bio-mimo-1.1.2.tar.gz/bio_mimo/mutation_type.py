from lhc.binf.sequence.reverse_complement import reverse_complement
from mimo import Stream


class GetMutationType(Stream):

    IN = ['variant']
    OUT = ['mutation_type']

    async def run(self, ins, outs):
        async for variant in ins.variant:
            if variant.ref in 'CTct':
                await outs.mutation_type.push((variant.ref, variant.alt[0]))
            else:
                await outs.mutation_type.push((reverse_complement(variant.ref), reverse_complement(variant.alt[0])))
        outs.mutation_type.close()
