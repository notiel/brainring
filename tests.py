import questiondata
import category_rewritten


def test_file_open():
    game, error = questiondata.create_game("Example.xlsx")
    if not game:
        print("Open file test failed: " + error)
        return
    if game.length != 2 or len(game.categories) != 2:
        print('open file test failed, wrong category number')
        return
    category = game.get_category_by_name('Красивые картинки')
    if not category:
        print('open file test failed, category is absent')
        return
    if len(category.questions) != 2:
        print('open file failed, wrong questions')
        return
    total = 0
    total_points = 0
    for category in game.categories:
        total += category.get_question_number()
        total_points += category.get_total_points()
    if total != 4:
        print('open file test: wrong questions number')
        return
    if total_points != 60:
        print('open file test: wrong points')
        return
    print('Open file test: passed')


def test_get_size():
    x, y = category_rewritten.get_size_data(36)
    if x != 6 or y != 6:
        print("Get  size failed for 36")
        return
    x, y = category_rewritten.get_size_data(35)
    if x != 7 or y != 5:
        print("Get  size failed for 35")
        return
    x, y = category_rewritten.get_size_data(21)
    if x != 5 or y != 5:
        print("Get  size failed for 21")
        return
    print("Get size function: passed")


def test_buttons():
    category = category_rewritten.CategoryForm()
    btn = category.create_button("test", 0, 0)
    if not btn or btn.text() != "test":
        print("Create button failed")
        return
    print("Btn create: passed")


def test_main():
    test_file_open()
    test_get_size()
    # test_buttons()


if __name__ == '__main__':
    test_main()
