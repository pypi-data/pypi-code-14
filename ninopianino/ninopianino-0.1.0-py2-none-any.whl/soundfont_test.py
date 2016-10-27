import generator, template_utils

def generate_blocks():
    blocks = []
    for i in range(1, 90):
        new_block = {
            'program_number' : i, 
            'play_at' : [(i-1) * 8], 
            'number_of_bars' : 2, 
            'number_of_beats_per_bar' : 4,
        }
        blocks.append(new_block)
        print 'Program number ', i, 'between ', (i-1)*4, 'and', i*4
    return blocks

def main():
    base_block = template_utils.create_base_block()
    base_block['channel'] = 1
    base_block['root_note'] = 'C'
    base_block['scale'] = 'major'
    base_block['blocks'] = generate_blocks()
    base_block['low_end'] = 'C2'
    base_block['high_end'] = 'C3'
    mid = generator.generate(base_block)
    song_path = generator.write_mid(mid, 'soundfont_test', 'soundfonts/FluidR3_GM.sf2')


main()
