

class Version:
    def __init__(self, ver):
        import re
        self.store  = dict.fromkeys(['major','minor','patch'])

        # Matching v1, V1.1, v1.1.1, 1, 1.1, 1.1.1
        self.regexp = re.compile(r'^([v|V])?(?P<major>\d+)(\.(?P<minor>\d+)(\.(?P<patch>\d+))?)?$')
        self.set(ver)

    def __str__(self):
        return self.get()

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.get()}')"

    def set(self, ver):
        match = self.regexp.match(str(ver))
        if not match: raise ValueError('Invalid version string format')

        self.store['major'] = 0 
        self.store['minor'] = 0
        self.store['patch'] = 0
        self.store['major'] = int(match.group('major'))
        if match.group('minor') != None: self.store['minor'] = int(match.group('minor'))
        if match.group('patch') != None: self.store['patch'] = int(match.group('patch'))

    def set_values(self, major, minor=None, patch=None):
        self.store['major'] = 0 
        self.store['minor'] = 0
        self.store['patch'] = 0
        self.store['major'] = int(major)
        if minor != None: self.store['minor'] = int(minor)
        if patch != None: self.store['patch'] = int(patch)
    
    def major(self, val=None):
        if val != None: self.store['major'] = val
        return self.store['major']

    def minor(self, val=None):
        if val != None: self.store['minor'] = val
        return self.store['minor']

    def patch(self, val=None):
        if val != None: self.store['patch'] = val
        return self.store['patch']

    def get(self):
        return f"{self.store['major']}.{self.store['minor']}.{self.store['patch']}"

    def notequal(self, ver):
        return not self.equal(ver)         

    def equal(self, ver):
        v = Version(ver)
        return self.get() == v.get()

    def incompatible(self, ver):
        v = Version(ver)
        return self.major() != v.major()

    def degraded(self, ver):
        v = Version(ver)
        if self.major() == v.major():
            return self.minor() == v.minor()
        else:
            return False 

    def compatible(self, ver):
        v = Version(ver)
        if self.major() == v.major():
            if self.minor() == v.minor():   return True
            else:                           return False
        else:                               return False 

    def interoperable(self, ver):
        if self.equal(ver):         return "compatible"
        if self.incompatible(ver):  return "incompatible"
        if self.degraded(ver):      return "degraded"
        raise ValueError('Unknown state of interoperability')

    def debug(self):
        print(self.__repr__())

if __name__ == '__main__':

    # Init
    myver = Version('v1.0.2')
    assert(str(myver) == '1.0.2')
    assert(myver.__repr__() == "Version('1.0.2')")
    myver = Version(1)
    assert(myver.get() == "1.0.0")
    myver = Version('v1.2')
    assert(myver.get() == "1.2.0")
    myver = Version('1.2.3')
    assert(myver.get() == "1.2.3")
    myver.set('v3.2')
    assert(myver.get() == "3.2.0")

    # Set 
    myver.set('10')
    assert(myver.get() == "10.0.0")
    myver.set('v11')
    assert(myver.get() == "11.0.0")
    myver.set('12.13.14')
    assert(myver.get() == "12.13.14")

    # Set values 
    myver.set_values(3)
    assert(myver.get() == "3.0.0")
    myver.set_values(3, 2)
    assert(myver.get() == "3.2.0")
    myver.set_values(3, 2, 1)
    assert(myver.get() == "3.2.1")

    # Get part
    myver = Version('1.2.3')
    assert(myver.major() == 1)
    assert(myver.minor() == 2)
    assert(myver.patch() == 3)

    # Set part
    myver.major(9)
    assert(myver.get() == '9.2.3')
    myver.minor(8)
    assert(myver.get() == '9.8.3')
    myver.patch(7)
    assert(myver.get() == '9.8.7')

    # Equality
    assert(myver.equal('9.8.7'))
    assert(myver.notequal('1.0.0'))

    # Compatibility
    myver = Version('10.20.30')
    assert(myver.incompatible('11'))
    assert(myver.incompatible('9'))
    assert(myver.incompatible('10') == False)

    assert(myver.compatible('11')   == False)
    assert(myver.compatible('9')    == False)
    assert(myver.compatible('10')   == False)
    assert(myver.compatible('10.20'))
    assert(myver.compatible('10.20.30'))
    assert(myver.compatible('10.20.1'))

    myver = Version('3.2.1')
    assert(myver.degraded('1.0.0') == False)
    assert(myver.degraded('3.0.0') == False)
    assert(myver.degraded('3.2.0'))
    assert(myver.degraded('3.2.1'))
    assert(myver.degraded('3.2.2'))

    myver = Version('3.2.1')
    assert(myver.interoperable('3.2.1') == 'compatible')
    assert(myver.interoperable('2.0.0') == 'incompatible')
    assert(myver.interoperable('4.0.0') == 'incompatible')
    assert(myver.interoperable('4.2.1') == 'incompatible')
    assert(myver.interoperable('3.2.0') == 'degraded')
    assert(myver.interoperable('3.2.2') == 'degraded')

    print(f'Class {myver.__class__.__name__} completed test successfully')
