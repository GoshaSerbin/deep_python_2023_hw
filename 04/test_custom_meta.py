import unittest

from custom_meta import CustomMeta


class TestCustomMeta(unittest.TestCase):
    def test_class_atributes(self):
        class CustomClass(metaclass=CustomMeta):
            x = 50

        self.assertEqual(CustomClass.custom_x, 50)
        self.assertRaises(AttributeError, getattr, CustomClass, "x")

    def test_nonpublic_and_private_atributes(self):
        class CustomClass(metaclass=CustomMeta):
            _protected = 5
            __private = 10

        self.assertEqual(CustomClass.custom__protected, 5)
        self.assertEqual(CustomClass.custom__CustomClass__private, 10)

        self.assertRaises(AttributeError, getattr, CustomClass, "_protected")
        self.assertRaises(
            AttributeError, getattr, CustomClass, "_CustomClass__private"
        )

    def test_class_instance_atributes(self):
        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

        inst = CustomClass()
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(str(inst), "Custom_by_metaclass")

        self.assertRaises(AttributeError, getattr, inst, "x")
        self.assertRaises(AttributeError, getattr, inst, "val")
        self.assertRaises(AttributeError, getattr, inst, "line")
        self.assertRaises(AttributeError, getattr, inst, "yyy")

    def test_dynamic_class_atributes(self):
        class CustomClass(metaclass=CustomMeta):
            pass

        CustomClass.x = 50
        self.assertEqual(CustomClass.custom_x, 50)
        self.assertRaises(AttributeError, getattr, CustomClass, "x")

    def test_dynamic_instance_atributes(self):
        class CustomClass(metaclass=CustomMeta):
            pass

        inst = CustomClass()
        inst.x = 50
        self.assertEqual(inst.custom_x, 50)
        self.assertRaises(AttributeError, getattr, inst, "x")

    def test_class_creation_on_the_fly(self):
        CustomClass = CustomMeta("CustomClass", (), {"x": 50})
        self.assertEqual(CustomClass.custom_x, 50)
        self.assertRaises(AttributeError, getattr, CustomClass, "x")

    def test_setattr_for_class(self):
        class CustomClass(metaclass=CustomMeta):
            pass

        setattr(CustomClass, "x", 10)
        self.assertEqual(CustomClass.custom_x, 10)
        self.assertRaises(AttributeError, getattr, CustomClass, "x")

        setattr(CustomClass, "_protected_x", 10)
        self.assertEqual(CustomClass.custom__protected_x, 10)
        self.assertRaises(AttributeError, getattr, CustomClass, "_protected_x")

        setattr(CustomClass, "__private_x", 10)
        self.assertEqual(CustomClass.custom___private_x, 10)
        self.assertRaises(AttributeError, getattr, CustomClass, "x")

        setattr(CustomClass, "__magic__", 10)
        self.assertEqual(CustomClass.__magic__, 10)

    def test_setattr_for_class_instance(self):
        class CustomClass(metaclass=CustomMeta):
            pass

        inst = CustomClass()

        setattr(inst, "x", 10)
        self.assertEqual(inst.custom_x, 10)
        self.assertRaises(AttributeError, getattr, inst, "x")

        setattr(inst, "_protected_x", 10)
        self.assertEqual(inst.custom__protected_x, 10)
        self.assertRaises(AttributeError, getattr, inst, "_protected_x")

        setattr(inst, "__private_x", 10)
        self.assertEqual(inst.custom___private_x, 10)
        self.assertRaises(AttributeError, getattr, inst, "x")

        setattr(inst, "__magic__", 10)
        self.assertEqual(inst.__magic__, 10)
