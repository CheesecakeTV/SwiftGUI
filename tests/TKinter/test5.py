from SwiftGUI_LeButch import ElementFlag


class derTest:
    _hallo = "Welt"
    test:ElementFlag

    @property
    def hallo(self):
        return self._hallo


x = derTest()
x._hallo = 15

y = derTest()
y._hallo = 20

print(x.hallo)
print(y.hallo)
print(x.test)

