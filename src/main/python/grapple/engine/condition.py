class Condition(object):

    def is_valid(self, **kwargs) -> bool:
        raise NotImplementedError('To be overridden in implementing classes')
