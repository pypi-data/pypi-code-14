import math
import decimal
import readline


def main():
    x_inputs = input("X Values: ").replace(",", ".").split()
    y_inputs = input("Y Values: ").replace(",", ".").split()
    x_vals = list(map(decimal.Decimal, x_inputs))
    y_vals = list(map(decimal.Decimal, y_inputs))
    print("Number of X Values:", len(x_vals))
    print("Number of Y Values:", len(y_vals))
    if len(x_vals) > 0:
        avg_x = avg(x_vals)
        print("X Values - Average:", format(avg_x, ".2f"))
        std_x = std_dev(x_vals)
        print("X Values - St. Dev:", format(std_x, ".2f"))
        if len(y_vals) > 0:
            avg_y = avg(y_vals)
            print("Y Values - Average:", format(avg_y, ".2f"))
            std_y = std_dev(y_vals)
            print("Y Values - St. Dev:", format(std_y, ".2f"))
            if (len(x_vals) != len(y_vals)):
                print("Number of X values and number of Y values must be"
                      " equivalent to calculate line fit.")
            elif (len(x_vals) > 1 and len(y_vals) > 1):
                line_fit(x_vals, y_vals)
            else:
                print("Number of X values and number of Y values must be"
                      " higher than one to calculate line fit.")


def std_dev(arr):
    average = avg(arr)
    return math.sqrt(sum(map(lambda x: (x - average) ** 2, arr)) / len(arr))


def avg(arr):
    return sum(arr) / len(arr)


def line_fit(x_vals, y_vals):
    SIGMA = chr(931)

    l = len(x_vals)
    sum_of_x = sum(x_vals)
    sum_of_y = sum(y_vals)
    sum_of_xy = sum(map(lambda x: x[0] * x[1], zip(x_vals, y_vals)))
    sum_of_x2 = sum(map(lambda x: x ** 2, x_vals))

    m = (l*sum_of_xy - sum_of_x*sum_of_y) / (l*sum_of_x2 - sum_of_x**2)
    n = (sum_of_x2*sum_of_y - sum_of_xy*sum_of_x) / (l*sum_of_x2 - sum_of_x**2)

    points = [(x, m*x + n) for x in x_vals]

    print(SIGMA + "x =", format(sum_of_x, ".2f"))
    print(SIGMA + "y =", format(sum_of_y, ".2f"))
    print(SIGMA + "(xy) =", format(sum_of_xy, ".2f"))
    print(SIGMA + "(x^2) =", format(sum_of_x2, ".2f"))

    print("For an equation like y = mx + n:")
    print("m:", format(m, ".2f"))
    print("n:", format(n, ".2f"))
    print("Equation: y =", format(m, ".2f"), "x +", format(n, ".2f"))

    print("Some points that satisfies the equation: ")
    for x, y in points:
        print("For x =", format(x, ".2f"), "y =", format(y, ".2f"))

    generate_points(m, n)


def generate_points(m, n):
    while True:
        try:
            x = int(input("Enter an x value to calculate another point: "))
        except:
            break
        print("For x =", format(x, ".2f"), "y =", format(m*x + n, ".2f"))


if __name__ == "__main__":
    main()
