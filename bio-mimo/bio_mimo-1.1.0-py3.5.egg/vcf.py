import gzip

from collections import deque
from itertools import islice
from lhc.io.vcf import VcfIterator
from mimo import Stream


class StreamVcf(Stream):

    IN = ['vcf_file']
    OUT = ['vcf_header', 'variant']

    async def run(self, ins, outs):
        async for vcf_file in ins.vcf_file:
            with gzip.open(vcf_file, 'rt', encoding='utf-8') if vcf_file.endswith('.gz') else \
                    open(vcf_file, encoding='utf-8') as fileobj:
                iterator = VcfIterator(fileobj)
                await outs.vcf_header.push(iterator.header)
                for variant in iterator:
                    await outs.variant.push(variant)
        outs.vcf_header.close()
        outs.variant.close()


class GetVariantByInterval(Stream):

    IN = ['chromosome_interval', 'variant']
    OUT = ['variant']

    async def run(self, ins, outs):
        variants = deque()
        while ins.chromosome_interval.is_open():
            interval = await ins.chromosome_interval.pop()
            while len(variants) > 0 and variants[0].pos < interval.start:
                variants.popleft()

            if ins.variant.is_open():
                if len(variants) == 0:
                    variants.append(await ins.variant.pop())
                while ins.variant.is_open() and variants[-1].pos < interval.stop:
                    variants.append(await ins.variant.pop())

            if variants[-1].pos < interval.stop:
                await outs.variant.push(list(variants))
            else:
                await outs.variant.push(list(islice(variants, 0, len(variants) - 1)))

        outs.variant.close()
