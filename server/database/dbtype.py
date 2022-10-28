# -*- coding: utf-8 -*-

class DatabaseType:
    template = []  # indexed from tuple

    def __init__(self, *args):
        for i, v in enumerate(args):
            setattr(self, self.template[i], v)

    def dict(self) -> dict:
        return {
            k: getattr(self, k)
            for k in dir(self)
            if not k.startswith('_') and not callable(getattr(self, k)) and k != 'template'
        }
