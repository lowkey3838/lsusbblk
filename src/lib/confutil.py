class Version:
    def __init__(self, ver):
        import re

        self.store = dict.fromkeys(["major", "minor", "patch"])

        # Matching v1, V1.1, v1.1.1, 1, 1.1, 1.1.1
        self.regexp = re.compile(
            r"^([v|V])?(?P<major>\d+)(\.(?P<minor>\d+)(\.(?P<patch>\d+))?)?$"
        )
        self.set(ver)

    def __str__(self):
        return self.get()

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.get()}')"

    def set(self, ver):
        match = self.regexp.match(str(ver))
        if not match:
            raise ValueError("Invalid version string format")

        self.store["major"] = 0
        self.store["minor"] = 0
        self.store["patch"] = 0
        self.store["major"] = int(match.group("major"))
        if match.group("minor") is not None:
            self.store["minor"] = int(match.group("minor"))
        if match.group("patch") is not None:
            self.store["patch"] = int(match.group("patch"))

    def set_values(self, major, minor=None, patch=None):
        self.store["major"] = 0
        self.store["minor"] = 0
        self.store["patch"] = 0
        self.store["major"] = int(major)
        if minor is not None:
            self.store["minor"] = int(minor)
        if patch is not None:
            self.store["patch"] = int(patch)

    def major(self, val=None):
        if val is not None:
            self.store["major"] = val
        return self.store["major"]

    def minor(self, val=None):
        if val is not None:
            self.store["minor"] = val
        return self.store["minor"]

    def patch(self, val=None):
        if val is not None:
            self.store["patch"] = val
        return self.store["patch"]

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
            if self.minor() == v.minor():
                return True
            else:
                return False
        else:
            return False

    def interoperable(self, ver):
        if self.equal(ver):
            return "compatible"
        if self.incompatible(ver):
            return "incompatible"
        if self.degraded(ver):
            return "degraded"
        raise ValueError("Unknown state of interoperability")

    def debug(self):
        print(self.__repr__())


if __name__ == "__main__":

    # Init
    myver = Version("v1.0.2")
    assert str(myver) == "1.0.2"  # nosec B101
    assert myver.__repr__() == "Version('1.0.2')"  # nosec B101

    myver = Version(1)
    assert myver.get() == "1.0.0"  # nosec B101
    myver = Version("v1.2")
    assert myver.get() == "1.2.0"  # nosec B101
    myver = Version("1.2.3")  # nosec B101
    assert myver.get() == "1.2.3"  # nosec B101
    myver.set("v3.2")
    assert myver.get() == "3.2.0"  # nosec B101

    # Set
    myver.set("10")
    assert myver.get() == "10.0.0"  # nosec B101
    myver.set("v11")
    assert myver.get() == "11.0.0"  # nosec B101
    myver.set("12.13.14")
    assert myver.get() == "12.13.14"  # nosec B101

    # Set values
    myver.set_values(3)
    assert myver.get() == "3.0.0"  # nosec B101
    myver.set_values(3, 2)
    assert myver.get() == "3.2.0"  # nosec B101
    myver.set_values(3, 2, 1)
    assert myver.get() == "3.2.1"  # nosec B101

    # Get part
    myver = Version("1.2.3")
    assert myver.major() == 1  # nosec B101
    assert myver.minor() == 2  # nosec B101
    assert myver.patch() == 3  # nosec B101

    # Set part
    myver.major(9)
    assert myver.get() == "9.2.3"  # nosec B101
    myver.minor(8)
    assert myver.get() == "9.8.3"  # nosec B101
    myver.patch(7)
    assert myver.get() == "9.8.7"  # nosec B101

    # Equality
    assert myver.equal("9.8.7")  # nosec B101
    assert myver.notequal("1.0.0")  # nosec B101

    # Compatibility
    myver = Version("10.20.30")
    assert myver.incompatible("11")  # nosec B101
    assert myver.incompatible("9")  # nosec B101
    assert myver.incompatible("10") is False  # nosec B101

    assert myver.compatible("11") is False  # nosec B101
    assert myver.compatible("9") is False  # nosec B101
    assert myver.compatible("10") is False  # nosec B101
    assert myver.compatible("10.20")  # nosec B101
    assert myver.compatible("10.20.30")  # nosec B101
    assert myver.compatible("10.20.1")  # nosec B101

    myver = Version("3.2.1")
    assert myver.degraded("1.0.0") is False  # nosec B101
    assert myver.degraded("3.0.0") is False  # nosec B101
    assert myver.degraded("3.2.0")  # nosec B101
    assert myver.degraded("3.2.1")  # nosec B101
    assert myver.degraded("3.2.2")  # nosec B101

    myver = Version("3.2.1")
    assert myver.interoperable("3.2.1") == "compatible"  # nosec B101
    assert myver.interoperable("2.0.0") == "incompatible"  # nosec B101
    assert myver.interoperable("4.0.0") == "incompatible"  # nosec B101
    assert myver.interoperable("4.2.1") == "incompatible"  # nosec B101
    assert myver.interoperable("3.2.0") == "degraded"  # nosec B101
    assert myver.interoperable("3.2.2") == "degraded"  # nosec B101

    print(f"Class {myver.__class__.__name__} completed test successfully")
