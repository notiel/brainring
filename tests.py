import questiondata
import category
import usbhost
import unittest


class TestGameOpened(unittest.TestCase):

    def test_GameOpened(self):
        game, _ = questiondata.create_game("Example.xlsx")
        self.assertIsNotNone(game)

    def test_GameLen(self):
        game, _ = questiondata.create_game("Example.xlsx")
        self.assertEqual(2, game.length)

    def test_CategoryLen(self):
        game, _ = questiondata.create_game("Example.xlsx")
        self.assertEqual(2, len(game.categories))

    def test_Category(self):
        game, _ = questiondata.create_game("Example.xlsx")
        category = game.get_category_by_name('Красивые картинки')
        self.assertIsNotNone(category)

    def test_CategoryQuestionLen(self):
        game, _ = questiondata.create_game("Example.xlsx")
        category = game.get_category_by_name('Красивые картинки')
        self.assertEqual(2, len(category.questions))

    def test_CategoryQuestionNumber(self):
        game, _ = questiondata.create_game("Example.xlsx")
        total = 0
        for category in game.categories:
            total += category.get_question_number()
        self.assertEqual(4, total)

    def test_CategoryQuestionPoints(self):
        game, _ = questiondata.create_game("Example.xlsx")
        total_points = 0
        for category in game.categories:
            total_points += category.get_total_points()
        self.assertEqual(60, total_points)


class TestSize(unittest.TestCase):

    def test_SizeFor36(self):
        x, y = category.get_size_data(36)
        self.assertEqual([x, y], [6, 6])

    def test_SizeFor35(self):
        x, y = category.get_size_data(35)
        self.assertEqual([x, y], [7, 5])

    def test_SizeFor21(self):
        x, y = category.get_size_data(21)
        self.assertEqual([x, y], [5, 5])

class TestButtonsSort(unittest.TestCase):

    def test_Sort_Simple(self):
        self.assertEqual(1, usbhost.get_first_button_from_answer("1 123456 2 234567"))

    def test_Sort_Not_Pressed(self):
        self.assertEqual(3, usbhost.get_first_button_from_answer("3 123456 1 234567 2 -1"))

    def test_Sort_Nothing_Pressed(self):
        self.assertIsNone(usbhost.get_first_button_from_answer("1 -1 3 -1 2 -1"))

    def test_Sort_Not_Inited(self):
        self.assertIsNone(usbhost.get_first_button_from_answer("1 0 3 0 2 0 4 0"))

    def test_Sort_Long(self):
        self.assertEqual(5, usbhost.get_first_button_from_answer("1 123456 2 234567 5 6789 6 456789 8 676454"))


"""class TestButtons(unittest.TestCase):

    def test_BtnCreation(self):
        game, _ = questiondata.create_game("Example.xlsx")
        category = category_rewritten.CategoryForm(game)
        btn = category.create_button("test", 0, 0)
        self.assertEqual(btn.text(), "test")"""


if __name__ == '__main__':
    unittest.main()
