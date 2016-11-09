from collections import defaultdict

import sf
from rv.api import Synth, m


def sin_generator(name):
    return m.Generator(waveform='sin', name=name, polyphony_ch=1)


class Synth(Synth):

    _forward_graph = None
    _reverse_graph = None
    _operator_names = None

    def __init__(self, algorithm=None, name='sf.fm.Synth', factories=None):
        super(Synth, self).__init__(module=m.MetaModule(name=name))
        self.algorithm = algorithm or sf.fm.PRESETS[1][0]
        if isinstance(factories, list):
            self.factories = factories
            while len(factories) < self.operator_count:
                factories.append(factories[-1])
        else:
            factories = sin_generator if not callable(factories) else factories
            self.factories = [factories] * self.operator_count
        self._build_note_input()
        self._build_operators()
        self._build_output_volume()
        self._connect_algorithm()
        self._connect_note_input()
        self.module.project.layout(factor=2)

    @property
    def forward_graph(self):
        if not self._forward_graph:
            graph = defaultdict(list)
            edges = [(src, dest) for src, dest in self.algorithm.split(' ')]
            for src, dest in edges:
                dest = src if dest == '-' else dest
                node = graph[src]
                if dest not in node:
                    graph[src].append(dest)
            self._forward_graph = graph
        return self._forward_graph

    @property
    def reverse_graph(self):
        if not self._reverse_graph:
            graph = defaultdict(list)
            edges = [(src, dest) for src, dest in self.algorithm.split(' ')]
            for src, dest in edges:
                dest = src if dest == '-' else dest
                node = graph[dest]
                if src not in node:
                    graph[dest].append(src)
            self._reverse_graph = graph
        return self._reverse_graph

    @property
    def operator_count(self):
        return len(self.forward_graph)

    @property
    def operator_names(self):
        if not self._operator_names:
            names = set(self.forward_graph).union(set(self.reverse_graph))
            self._operator_names = list(sorted(names))
            self._operator_names.remove('.')
        return self._operator_names

    def _build_note_input(self):
        p = self.module.project
        self._note_input = p.new_module(m.MultiSynth, name='note in')

    def _build_operators(self):
        self._operators = {}
        self._operator_c_amps = {}
        self._operator_m_amps = {}
        self._operator_mods = {}
        self._operator_multis = {}
        p = self.module.project
        for name, factory in zip(self.operator_names, self.factories):
            multi = m.MultiSynth(name='{} note'.format(name))
            oper = factory(name='{} oper'.format(name))
            c_amp = m.Amplifier(name='{} c amp'.format(name))
            m_amp = m.Amplifier(name='{} m amp'.format(name))
            mod = m.Modulator(modulation_type='phase',
                              name='{} mod'.format(name))
            p += [multi, oper, c_amp, m_amp, mod]
            multi >> oper >> c_amp >> mod
            m_amp >> mod
            self._operators[name] = oper
            self._operator_c_amps[name] = c_amp
            self._operator_m_amps[name] = m_amp
            self._operator_mods[name] = mod
            self._operator_multis[name] = multi

    def _build_output_volume(self):
        p = self.module.project
        self._volume_amp = p.new_module(m.Amplifier, name='vol')
        self._volume_amp >> p.output

    def _connect_algorithm(self):
        self._feedback_ctls = {}
        p = self.module.project
        for dest_key, src_keys in self.reverse_graph.items():
            if dest_key == '.':
                dest_amp = self._volume_amp
            else:
                dest_amp = self._operator_m_amps[dest_key]
            for src_key in src_keys:
                src_mod = self._operator_mods[src_key]
                if src_key == dest_key:
                    fb1 = p.new_module(m.Feedback, volume=0)
                    fb2 = p.new_module(m.Feedback, volume=0)
                    fb_ctl = p.new_module(
                        m.MultiCtl,
                        value=0,
                        name='{} fb'.format(src_key),
                        mappings=[
                            (0, 32768, fb1.controllers['volume'].number),
                            (0, 32768, fb2.controllers['volume'].number),
                        ]
                    )
                    src_m_amp = self._operator_m_amps[src_key]
                    src_mod >> fb1 >> fb2 >> src_m_amp
                    fb_ctl >> [fb1, fb2]
                    self._feedback_ctls[src_key] = fb_ctl
                else:
                    src_mod >> dest_amp

    def _connect_note_input(self):
        self._note_input >> list(self._operator_multis.values())
        self.module.input_module = self._note_input.index
