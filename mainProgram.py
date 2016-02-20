
class abelPaul(object):
    def __init__(self, name):
        self.name = name

    def speak(self):
        for i in self.name:
            print i


def main():
    abel = abelPaul("hey what up")
    print "abel"
    abel.speak()


if __name__ == "__main__":
    main()
