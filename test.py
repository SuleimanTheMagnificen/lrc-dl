def test(opt, *add):
    print(opt)
    for value in add:
        if value == "world":
            continue
        print(value)


test("Hello", "world", "Bye")
