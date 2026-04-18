from numbers import Number


class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            # checks if the type of other is a polynomial
            common = min(self.degree(), other.degree()) + 1
            # number of overlapping powers
            coefs = tuple(a - b for a, b in zip(self.coefficients,
                                                other.coefficients))
            # pairs the coefficients with same power then minus
            if self.degree() - other.degree() > 0:
                coefs += self.coefficients[common:]
                # common: starts at index common and no end, adds the
                # remaining unchange coefficients
            else:
                coefs += tuple(-c for c in other.coefficients[common:])
                # if other is longer adds the coefs but with flipped sign
            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] - other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __rsub__(self, other):
        # as not commutative need to do other - self
        if isinstance(other, Number):
            return Polynomial((other - self.coefficients[0],)
                              + tuple(-c for c in self.coefficients[1:]))
        else:
            return NotImplemented

    def __mul__(self, other):

        if isinstance(other, Polynomial):
            result = [0] * (self.degree() + other.degree() + 1)
            # creates a list of n 0's

            for i, a in enumerate(self.coefficients):
                # looping trhough self.coefficients
                # i index the power of x
                # a is the coefficient at that index

                for j, b in enumerate(other.coefficients):
                    # loop through other coefficients
                    # j the index, b the coefficient

                    result[i + j] += a * b
                    # adds a*b to the (i+j)th element of the list
                    # result from the start

            return Polynomial(tuple(result))
        # convert result list into a tuple, then return as a Polynomial

        elif isinstance(other, Number):
            return Polynomial((tuple(a*other for a in self.coefficients)))
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self*other

    def __pow__(self, power):
        if not isinstance(power, int):
            return NotImplemented
        if power <= 0:
            raise ValueError("Value must be positive")

        total = Polynomial((1,))
        for i in range(power):
            total = total * self
        return total

    def __call__(self, x):
        if not isinstance(x, int):
            raise ValueError("Not a number")

        result = 0
        for i, a in enumerate(self.coefficients):
            result += (x**i)*a
        return result

    def dx(self):
        # not a special method as not a preexisiting function
        newcoefs = []
        if len(self.coefficients) == 1:
            return Polynomial((0,))
        # for constant polynomials

        for i, a in enumerate(self.coefficients[1:], start=1):
            newcoefs.append(i*a)
            # adding a value not another list so use append not +=
        return Polynomial(tuple(newcoefs))


def derivative(p):
    return p.dx()
