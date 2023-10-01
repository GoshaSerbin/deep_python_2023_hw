import unittest
from io import StringIO


from generator import occurrences_generator


class TestGenerator(unittest.TestCase):
    def test_with_no_occurences_found(self):
        test_file_content = StringIO(
            "Have you heard the news that you're dead?\n"
            "No one ever had much nice to say\n"
            "I think they never liked you anyway\n"
        )
        search_words = ["word"]

        gen = occurrences_generator(test_file_content, search_words)
        self.assertRaises(StopIteration, next, gen)

    def test_empty_file_object(self):
        test_file_content = StringIO("")
        search_words = ["word"]

        gen = occurrences_generator(test_file_content, search_words)
        self.assertRaises(StopIteration, next, gen)

    def test_stop_iteration_raises_in_the_end(self):
        test_file_content = StringIO("a\na\na\na\na")
        search_words = ["a"]

        gen = occurrences_generator(test_file_content, search_words)
        for _ in range(5):
            next(gen)
        self.assertRaises(StopIteration, next, gen)

    def test_few_suitable_lines_in_file_object(self):
        test_file_content = StringIO(
            "suitable_line\nsuitable_line\nbad_line\nsuitable_line"
        )
        search_words = ["suitable_line"]
        for line in occurrences_generator(test_file_content, search_words):
            self.assertEqual("suitable_line", line)

    def test_find_all_occurences(self):
        test_file_content = StringIO("a\na\nb\nb\na\nc\na")
        search_words = ["a"]
        count = len(
            list(occurrences_generator(test_file_content, search_words))
        )
        self.assertEqual(4, count)

    def test_with_few_words_in_each_line(self):
        test_file_content = StringIO(
            "some line with long text and alot of words\n                     "
            "                another line for testing generator\n             "
            "                        third line with test text"
        )
        search_words = ["with"]
        count = len(
            list(occurrences_generator(test_file_content, search_words))
        )
        self.assertEqual(2, count)

    def test_words_with_upper_case(self):
        test_file_content = StringIO("ABC\nabc\naBc")
        search_words = ["abc"]
        gen = occurrences_generator(test_file_content, search_words)
        self.assertEqual("ABC", next(gen))
        self.assertEqual("abc", next(gen))
        self.assertEqual("aBc", next(gen))
        self.assertRaises(StopIteration, next, gen)

    def test_words_with_same_root(self):
        test_file_content = StringIO("abc\nabcdef\nabc")
        search_words = ["abc"]
        gen = occurrences_generator(test_file_content, search_words)
        self.assertEqual("abc", next(gen))
        self.assertEqual("abc", next(gen))
        self.assertRaises(StopIteration, next, gen)

    def test_with_few_search_words(self):
        test_file_content = StringIO(
            "Python code\nJava code\nC code\nPascal code"
        )
        search_words = ["Python", "Java"]
        gen = occurrences_generator(test_file_content, search_words)
        self.assertEqual("Python code", next(gen))
        self.assertEqual("Java code", next(gen))
        self.assertRaises(StopIteration, next, gen)

    def test_with_opening_file(self):
        search_words = ["I"]
        gen = occurrences_generator("test_data/test_file.txt", search_words)
        self.assertEqual("All I see", next(gen))
        self.assertEqual("As below so above and beyond I imagine", next(gen))
        self.assertRaises(StopIteration, next, gen)
