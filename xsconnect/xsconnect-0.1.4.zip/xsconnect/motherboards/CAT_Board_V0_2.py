brd = {
    'name': ('CAT Board V0.2'),
    'port': {
        'pmod': {
            'pm2': {
                'd0': 'pm2-a1',
                'd1': 'pm2-b1',
                'd2': 'pm2-a2',
                'd3': 'pm2-b2',
                'd4': 'pm2-a3',
                'd5': 'pm2-b3',
                'd6': 'pm2-a4',
                'd7': 'pm2-b4'
            },
            'pm3': {
                'd0': 'pm3-a1',
                'd1': 'pm3-b1',
                'd2': 'pm3-a2',
                'd3': 'pm3-b2',
                'd4': 'pm3-a3',
                'd5': 'pm3-b3',
                'd6': 'pm3-a4',
                'd7': 'pm3-b4'
            }
        },
        'dualpmod': {
            'pm2+pm3': {
                'd0' : 'pm2-a1',
                'd1' : 'pm2-b1',
                'd2' : 'pm2-a2',
                'd3' : 'pm2-b2',
                'd4' : 'pm2-a3',
                'd5' : 'pm2-b3',
                'd6' : 'pm2-a4',
                'd7' : 'pm2-b4',
                'd8' : 'pm3-a1',
                'd9' : 'pm3-b1',
                'd10': 'pm3-a2',
                'd11': 'pm3-b2',
                'd12': 'pm3-a3',
                'd13': 'pm3-b3',
                'd14': 'pm3-a4',
                'd15': 'pm3-b4'
            }
        },
        'hdr_10x2': {
            'hdr1': {
                'd0' : 'hdr1-1',
                'd1' : 'hdr1-2',
                'd2' : 'hdr1-3',
                'd3' : 'hdr1-4',
                'd4' : 'hdr1-6',
                'd5' : 'hdr1-7',
                'd6' : 'hdr1-8',
                'd7' : 'hdr1-9',
                'd8' : 'hdr1-10',
                'd9' : 'hdr1-11',
                'd10': 'hdr1-12',
                'd11': 'hdr1-13',
                'd12': 'hdr1-14',
                'd13': 'hdr1-16',
                'd14': 'hdr1-17',
                'd15': 'hdr1-18',
                'd16': 'hdr1-19',
                'd17': 'hdr1-20'
            }
        },
        'grove': {
            'gr1': {
                'd0': 'gr1-io1',
                'd1': 'gr1-io2'
            },
            'gr2': {
                'd0': 'gr2-io1',
                'd1': 'gr2-io2'
            },
            'gr3': {
                'd0': 'gr3-io1',
                'd1': 'gr3-io2'
            },
            'gr4': {
                'd0': 'pm2-b1',
                'd1': 'pm2-b2'
            },
            'gr5': {
                'd0': 'pm3-b1',
                'd1': 'pm3-b2'
            }
        },
        'sata': {
            'sata1': {
                'dap': 'sata1_a+',
                'dan': 'sata1_a-',
                'dbp': 'sata1_b+',
                'dbn': 'sata1_b-'
            },
            'sata2': {
                'dap': 'sata2_a+',
                'dan': 'sata2_a-',
                'dbp': 'sata2_b+',
                'dbn': 'sata2_b-'
            },
        },
        'rpigpio': {
            'gpio': {
                '3' : 'bcm2_sda',
                '5' : 'bcm3_scl',
                '7' : 'bcm4_gpclk0',
                '11': 'bcm17',
                '13': 'bcm27_pcm_0',
                '15': 'bcm22',
                '19': 'bcm10_mosi',
                '21': 'bcm9_miso',
                '23': 'bcm11_sclk',
                '27': 'bcm0_id_sd',
                '29': 'bcm5',
                '31': 'bcm6',
                '33': 'bcm13',
                '35': 'bcm19_miso',
                '37': 'bcm26',
                '40': 'bcm21_sclk',
                '38': 'bcm20_mosi',
                '36': 'bcm16',
                '32': 'bcm12',
                '28': 'bcm1_id_sc',
                '26': 'bcm7_ce1',
                '24': 'bcm8_ce0',
                '22': 'bcm25',
                '18': 'bcm24',
                '16': 'bcm23',
                '12': 'bcm18_pcm_c',
                '10': 'bcm15_rxd',
                '8' : 'bcm14_txd'
            }
        },
        'ice40hx' : {
            'default' : {
                'pm2-a1':      'pm2-a1',
                'pm2-b1':      'pm2-b1',
                'pm2-a2':      'pm2-a2',
                'pm2-b2':      'pm2-b2',
                'pm2-a3':      'pm2-a3',
                'pm2-b3':      'pm2-b3',
                'pm2-a4':      'pm2-a4',
                'pm2-b4':      'pm2-b4',
                'pm3-a1':      'pm3-a1',
                'pm3-b1':      'pm3-b1',
                'pm3-a2':      'pm3-a2',
                'pm3-b2':      'pm3-b2',
                'pm3-a3':      'pm3-a3',
                'pm3-b3':      'pm3-b3',
                'pm3-a4':      'pm3-a4',
                'pm3-b4':      'pm3-b4',
                'hdr1-1':      'hdr1-1',
                'hdr1-2':      'hdr1-2',
                'hdr1-3':      'hdr1-3',
                'hdr1-4':      'hdr1-4',
                'hdr1-6':      'hdr1-6',
                'hdr1-7':      'hdr1-7',
                'hdr1-8':      'hdr1-8',
                'hdr1-9':      'hdr1-9',
                'hdr1-10':     'hdr1-10',
                'hdr1-11':     'hdr1-11',
                'hdr1-12':     'hdr1-12',
                'hdr1-13':     'hdr1-13',
                'hdr1-14':     'hdr1-14',
                'hdr1-16':     'hdr1-16',
                'hdr1-17':     'hdr1-17',
                'hdr1-18':     'hdr1-18',
                'hdr1-19':     'hdr1-19',
                'hdr1-20':     'hdr1-20',
                'gr1-io1':     'gr1-io1',
                'gr1-io2':     'gr1-io2',
                'gr2-io1':     'gr2-io1',
                'gr2-io2':     'gr2-io2',
                'gr3-io1':     'gr3-io1',
                'gr3-io2':     'gr3-io2',
                'sata1_a+':    'sata1_a+',
                'sata1_a-':    'sata1_a-',
                'sata1_b+':    'sata1_b+',
                'sata1_b-':    'sata1_b-',
                'sata2_a+':    'sata2_a+',
                'sata2_a-':    'sata2_a-',
                'sata2_b+':    'sata2_b+',
                'sata2_b-':    'sata2_b-',
                'bcm2_sda':    'bcm2_sda',
                'bcm3_scl':    'bcm3_scl',
                'bcm4_gpclk0': 'bcm4_gpclk0',
                'bcm17':       'bcm17',
                'bcm27_pcm_0': 'bcm27_pcm_0',
                'bcm22':       'bcm22',
                'bcm10_mosi':  'bcm10_mosi',
                'bcm9_miso':   'bcm9_miso',
                'bcm11_sclk':  'bcm11_sclk',
                'bcm5':        'bcm5',
                'bcm6':        'bcm6',
                'bcm13':       'bcm13',
                'bcm19_miso':  'bcm19_miso',
                'bcm26':       'bcm26',
                'bcm21_sclk':  'bcm21_sclk',
                'bcm20_mosi':  'bcm20_mosi',
                'bcm16':       'bcm16',
                'bcm12':       'bcm12',
                'bcm7_ce1':    'bcm7_ce1',
                'bcm8_ce0':    'bcm8_ce0',
                'bcm25':       'bcm25',
                'bcm24':       'bcm24',
                'bcm23':       'bcm23',
                'bcm18_pcm_c': 'bcm18_pcm_c',
                'bcm15_rxd':   'bcm15_rxd',
                'bcm14_txd':   'bcm14_txd'
            }
        }
    }
}