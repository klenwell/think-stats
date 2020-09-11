class Mother:
    #
    # Static Methods
    #

    #
    # Properties
    #
    @property
    def babies(self):
        return [baby for baby in self.pregnancies if baby.is_live()]

    @property
    def first_baby(self):
        if self.babies:
            return [baby for baby in self.babies if baby.is_first()][0]
        else:
            return None

    @property
    def later_babies(self):
        if self.had_multiple_babies():
            return [baby for baby in self.babies if not baby.is_first()]
        else:
            return None

    #
    # Instance Methods
    #
    def __init__(self, case_id, pregnancies):
        self.case_id = case_id
        self.pregnancies = pregnancies

    def had_multiple_babies(self):
        return len(self.babies) > 1

    def diff_first_baby_weeks(self):
        baby_weeks = [baby.weeks for baby in self.later_babies]
        other_weeks_avg = sum(baby_weeks) / len(baby_weeks)
        return self.first_baby.weeks - other_weeks_avg

    # Private
    def __repr__(self):
        f = '<Mother case_id={} pregnancies={} babies={}>'
        return f.format(self.case_id, len(self.pregnancies), len(self.babies))
