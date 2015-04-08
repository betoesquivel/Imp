from semantics import errors
class MemoryBlock:
    def __init__(self, start_dir, ints_start_dir, floats_start_dir, chars_start_dir, strings_start_dir, limit):
       '''All blocks have to be in ascending order and non overlapping on init. We leave that to the developer that uses this class'''
       self.bools = [ start_dir, 0 ]
       self.ints = [ ints_start_dir, 0 ]
       self.floats = [ floats_start_dir, 0 ]
       self.chars = [ chars_start_dir, 0 ]
       self.strings = [ strings_start_dir, 0 ]
       self.limit = limit

    def __str__(self):
        return "MemoryBlock ({start}-{end}): {boolno} bools, {intno} ints, {floatno} floats, {charno} chars, {stringno} strings".format( start=self.bools[0], end=self.limit, boolno=self.bools[1], intno=self.ints[1], floatno=self.floats[1], charno=self.chars[1], stringno=self.strings[1])

    def add_bool(self, num=1):
        '''Adds a var to the memory block'''
        if ( self.bools[0] + self.bools[1] + num ) < self.ints[0]:
            self.bools[1] += num
            return ( self.bools[0] + self.bools[1] - num )
        else:
            print errors['STACKOVERFLOW']

    def add_int(self, num=1):
        '''Adds a var to the memory block'''
        if ( self.ints[0] + self.ints[1] + num ) < self.floats[0]:
            self.ints[1] += num
            return ( self.ints[0] + self.ints[1] - num )
        else:
            print errors['STACKOVERFLOW']

    def add_float(self, num=1):
        '''Adds a var to the memory block'''
        if ( self.floats[0] + self.floats[1] + num ) < self.chars[0]:
            self.floats[1] += num
            return ( self.floats[0] + self.floats[1] - num )
        else:
            print errors['STACKOVERFLOW']

    def add_char(self, num=1):
        '''Adds a var to the memory block'''
        if ( self.chars[0] + self.chars[1] + num ) < self.strings[0]:
            self.chars[1] += num
            return ( self.chars[0] + self.chars[1] - num )
        else:
            print errors['STACKOVERFLOW']

    def add_string(self, num=1):
        '''Adds a var to the memory block'''
        if ( self.strings[0] + self.strings[1] + num ) < self.limit:
            self.strings[1] += num
            return ( self.strings[0] + self.strings[1] - num )
        else:
            print errors['STACKOVERFLOW']
