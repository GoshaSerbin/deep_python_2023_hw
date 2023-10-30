class CustomList(list):
    def __str__(self):
        return super().__str__() + f", sum = {sum(self)}"

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __operate(self, other, operation):
        result = CustomList([0 for _ in range(max(len(self), len(other)))])
        i = 0
        while i < min(len(self), len(other)):
            result[i] = getattr(self[i], operation)(other[i])
            i += 1
        while i < len(self):
            result[i] = getattr(self[i], operation)(0)
            i += 1
        while i < len(other):
            result[i] = getattr(0, operation)(other[i])
            i += 1

        return result

    def __add__(self, other):
        return self.__operate(other, "__add__")

    def __sub__(self, other):
        return self.__operate(other, "__sub__")

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return CustomList([-1 * i for i in self - other])
