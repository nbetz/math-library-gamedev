import math


class Vector3:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def dot_product(self, other: "Vector3"):
        if self.w == 0 and other.w == 0:
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            raise Exception("cannot get dot_product on point vector")

    def cross_product(self, other: "Vector3"):
        if self.w == 0 and other.w == 0:
            return Vector3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                           self.x * other.y - self.y * other.x, 0)
        else:
            raise Exception("cannot find angles between point vectors")

    def find_angle(self, other: "Vector3"):
        if self.w == 0 and other.w == 0:
            math.acos((self.dot_product(other) / (self.accurate_magnitude() * other.accurate_magnitude())))
        else:
            raise Exception("cannot find angles between point vectors")

    def normalize(self):
        if self.w == 0:
            acc_mag = self.accurate_magnitude()
            return (self.x / acc_mag) + (self.y / acc_mag) + (self.z / acc_mag)
        else:
            raise Exception("cannot normalize a point vector")

    def accurate_magnitude(self):
        if self.w == 0:
            relative_mag = self.relative_magnitude()
            return math.sqrt(relative_mag)
        else:
            raise Exception("cannot get magnitude of a point vector")

    def relative_magnitude(self):
        if self.w == 0:
            return (self.x * self.x) + (self.y * self.y) + (self.z * self.z)
        else:
            raise Exception("cannot get magnitude of a point vector")

    def __add__(self, other: "Vector3"):
        if self.w == 1 and other.w == 1:
            raise Exception("cannot add two points")
        elif self.w == 1 or other.w == 1:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z, 1)
        elif self.w == 0 and other.w == 0:
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z, 0)
        else:
            raise Exception("the w flag was improperly used")

    def __sub__(self, other: "Vector3"):
        if self.w == 1 and other.w == 1:
            raise Exception("cannot add two points")
        elif self.w == 1 or other.w == 1:
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z, 1)
        elif self.w == 0 and other.w == 0:
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z, 0)
        else:
            raise Exception("the w flag was improperly used")

    def __eq__(self, other: "Vector3"):
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        if self.z != other.z:
            return False
        if self.w != other.w:
            return False
        return True


class Vector2(Vector3):
    def __init__(self, x, y, w):
        super().__init__(x, y, 0, w)

    def cross_product(self, other: "Vector2"):
        return self.x * other.y - self.y * other.x


class Vector4:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def dot_product(self, other: "Vector4"):
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def __add__(self, other: "Vector4"):
        return Vector4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other: "Vector4"):
        return Vector4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __eq__(self, other: "Vector4"):
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        if self.z != other.z:
            return False
        if self.w != other.w:
            return False
        return True


class Matrix:
    def __init__(self, row0: Vector4, row1: Vector4, row2: Vector4, row3: Vector4):
        self._row0 = row0
        self._row1 = row1
        self._row2 = row2
        self._row3 = row3

    def get_val_at_index(self, x, y):
        row = self._get_row(y)
        if x == 0:
            return row.x
        if x == 1:
            return row.y
        if x == 2:
            return row.z
        if x == 3:
            return row.w

    def _get_row(self, y):
        if y == 0:
            return self._row0
        if y == 1:
            return self._row1
        if y == 2:
            return self._row2
        if y == 3:
            return self._row3
        else:
            raise Exception("out of bounds")

    def multiply_with_vector(self, vertical_vector: Vector4) -> Vector4:
        stuff = []
        for x in range(0, 4):
            stuff.append(self._get_row(x).dot_product(vertical_vector))
        return Vector4(stuff[0],stuff[1],stuff[2],stuff[3])

    def __mul__(self, other: "Matrix"):
        spots = []
        cols = []
        cols.append(Vector4(other._row0.x, other._row1.x, other._row2.x, other._row3.x))
        cols.append(Vector4(other._row0.y, other._row1.y, other._row2.y, other._row3.y))
        cols.append(Vector4(other._row0.z, other._row1.z, other._row2.z, other._row3.z))
        cols.append(Vector4(other._row0.w, other._row1.w, other._row2.w, other._row3.w))
        for x in range(0, 4):
            for y in range(0, 4):
                r = self._get_row(x)
                c = cols[y]
                spots.append(r.dot_product(c))
        return Matrix(Vector4(spots[0],spots[1],spots[2],spots[3]),Vector4(spots[4],spots[5],spots[6],spots[7]),Vector4(spots[8],spots[9],spots[10],spots[11]),Vector4(spots[12],spots[13],spots[14],spots[15]))

    def __add__(self, other: "Matrix"):
        spots = []
        for x in range(0, 4):
            for y in range(0, 4):

                spots.append(self.get_val_at_index(x, y) + other.get_val_at_index(x, y))
        return Matrix(Vector4(spots[0], spots[1], spots[2], spots[3]),
                              Vector4(spots[4], spots[5], spots[6], spots[7]),
                              Vector4(spots[8], spots[9], spots[10], spots[11]),
                              Vector4(spots[12], spots[13], spots[14], spots[15]))


    def __sub__(self, other: "Matrix"):
        spots = []
        for x in range(0, 4):
            for y in range(0, 4):
                spots.append(self.get_val_at_index(x, y) - other.get_val_at_index(x, y))

        return Matrix(Vector4(spots[0], spots[1], spots[2], spots[3]),
                      Vector4(spots[4], spots[5], spots[6], spots[7]),
                      Vector4(spots[8], spots[9], spots[10], spots[11]),
                      Vector4(spots[12], spots[13], spots[14], spots[15]))


    def __eq__(self, other: "Matrix"):
        for x in range(0, 4):
            for y in range(0, 4):
                if self.get_val_at_index(x, y) != other.get_val_at_index(x, y):
                    return False
        return True
