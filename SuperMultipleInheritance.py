class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * self.length + 2 * self.width


class Square(Rectangle):
    def __init__(self, length):
        super(Square, self).__init__(length, length)


# calling .area_2() will give us an AttributeError since .base and .height don’t have any values.
# To fix this it requires to use **kwargs, which is very messy.
# https://realpython.com/python-super/#what-can-super-do-for-you
# class Triangle:
#     def __init__(self, base, height):
#         self.base = base
#         self.height = height

#     def tri_area(self):
#         return 0.5 * self.base * self.height

# class RightPyramid(Square, Triangle):
#     def __init__(self, base, slant_height):
#         self.base = base
#         self.slant_height = slant_height
#         super().__init__(self.base)

#     def area(self):
#         base_area = super().area()
#         perimeter = super().perimeter()
#         return 0.5 * perimeter * self.slant_height + base_area

#     def area_2(self):
#         base_area = super().area()
#         triangle_area = super().tri_area()
#         return triangle_area * 4 + base_area

# pyramid = RightPyramid(2, 4)
# print(pyramid.area_2())

class VolumeMixin:
    def volume(self):
        return self.area() * self.height


class Cube(VolumeMixin, Square):
    def __init__(self, length):
        super().__init__(length)
        self.height = length

    def face_area(self):
        return super().area()

    def surface_area(self):
        return super().area() * 6


cube = Cube(2)
print(cube.surface_area())
print(cube.volume())
