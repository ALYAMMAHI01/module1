
# A simple module to determine if a number is even or odd.

def even_or_odd(n):
    """Return 'even' if integer `n` is even, otherwise 'odd'.

    Accepts integers or values convertible to `int` (like strings of digits).
    Raises TypeError for values that cannot be converted to int.
    """
    try:
        i = int(n)
    except (ValueError, TypeError):
        raise TypeError("Input must be an integer or convertible to int")
    return "even" if i % 2 == 0 else "odd"


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            try:
                print(f"{arg}: {even_or_odd(arg)}")
            except TypeError as e:
                print(f"{arg}: error - {e}")
    else:
        try:
            s = input("Enter an integer: ")
            print(even_or_odd(s))
        except Exception as e:
            print("Error:", e)
            

