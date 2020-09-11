class Pregnancy:
    #
    # Static Methods
    #

    #
    # Properties
    #
    @property
    def weeks(self):
        return self.attrs.get('weeks')

    @property
    def weight(self):
        return self.attrs.get('weight')

    @property
    def sex(self):
        return self.attrs.get('sex')

    #
    # Instance Methods
    #
    def __init__(self, **attrs):
        self.attrs = attrs

    def is_live(self):
        return self.attrs.get('live', False)

    def is_first(self):
        return self.attrs.get('first', False)

    # Private
    # Private
    def __repr__(self):
        f = '<Pregnancy sex={} weight={} weeks={}>'
        return f.format(self.sex, self.weight, self.weeks)
