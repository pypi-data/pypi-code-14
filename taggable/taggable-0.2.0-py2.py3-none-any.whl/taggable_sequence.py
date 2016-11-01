class TaggedSegment(object):
    def __init__(self, start, end, name, tag):
        self.start_ = start
        self.end_ = end
        self.name_ = name
        self.tag_ = tag

    @property
    def start(self):
        """Starting offset of the segment"""
        return self.start_

    @property
    def end(self):
        """End offset of the segment"""
        return self.end_

    @property
    def name(self):
        """Name of the tag"""
        return self.name_

    @property
    def tag(self):
        """Value of the tag"""
        return self.tag_

    def __contains__(self, offset):
        return offset <= self.end_ and offset >= self.start_

    def __eq__(self, other):
        return (other.start_ == self.start_ and other.end_ == self.end_
                and other.tag_ == self.tag_ and other.name == self.name)

    def __hash__(self):
        return hash((self.start_, self.end_))


class TaggableSequence(object):
    def __init__(self, sequence):
        self.sequence_ = sequence
        self.tags_ = {}

    def __len__(self):
        return len(self.sequence)

    def __getitem__(self, item):
        return self.sequence[item]

    @property
    def sequence(self):
        """Sequence being tagged"""
        return self.sequence_

    def tag_names(self):
        return self.tags_.keys()

    def tag(self, name, tag):
        last_position = len(self.sequence_) - 1 if len(self.sequence_) > 0 else 0
        self.tag_at(0, last_position, name, tag)

    def tag_at(self, start, end, name, tag):
        current = self.tags_.get(name, [])
        current.append(TaggedSegment(start, end, name, tag))
        self.tags_[name] = current

    def tags(self, name):
        return self.tags_.get(name)

    def tags_at(self, offset):
        results = []
        for name in self.tags_.keys():
            for tag in self.tags_.get(name):
                if offset in tag:
                    results.append(tag)

        return results

    def __iter__(self):
        for name in self.tags_.keys():
            for value in self.tags_.get(name):
                yield value
