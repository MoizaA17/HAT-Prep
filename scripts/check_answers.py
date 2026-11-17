import re
from fractions import Fraction as F


def pick(value, options):
    """Return the option whose numeric value equals the computed answer."""
    for opt in options:
        body = re.sub(r"^[A-D]\.\s*", "", opt)           # drop "A. " prefix
        m = re.search(r"\d[\d,]*(?:\.\d+)?", body)       # first number, e.g. 1,600 or 52.5
        if m and F(m.group().replace(",", "")) == F(value):
            return opt
    raise ValueError(f"No option matches {value}")


def q1():
    total, a, b = 1200, 3, 5
    sara = F(total * b, a + b)
    return pick(sara, ["A. Rs. 750", "B. Rs. 450", "C. Rs. 600", "D. Rs. 720"])


def q2():
    boys, rb, rg = 18, 3, 2
    girls = F(boys * rg, rb)
    return pick(boys + girls, ["A. 12", "B. 27", "C. 30", "D. 36"])


def q3():
    cost = F(275, 5) * 8
    return pick(cost, ["A. Rs. 330", "B. Rs. 385", "C. Rs. 400", "D. Rs. 440"])


def q4():
    dist = F(15, 2) * 7
    return pick(dist, ["A. 105 km", "B. 52.5 km", "C. 26.25 km", "D. 14 km"])


def q5():
    # Hina = 2x, mother = 5x; (2x + 8) / (5x + 8) = 1/2  ->  2(2x+8) = 5x+8
    # 4x + 16 = 5x + 8  ->  x = 8
    x = F(16 - 8, 5 - 4)
    return pick(2 * x, ["A. 8 years", "B. 24 years", "C. 16 years", "D. 40 years"])


def q6():
    total, m, w = 35, 5, 2
    milk = F(total * m, m + w)
    water = F(total * w, m + w)
    new_water = milk * 4 / 5          # milk:water = 5:4
    added = new_water - water
    return pick(added, ["A. 10 litres", "B. 20 litres", "C. 15 litres", "D. 5 litres"])


def q7():
    days = F(12 * 18, 8)              # constant worker-days
    return pick(days, ["A. 12 days", "B. 24 days", "C. 30 days", "D. 27 days"])


def q8():
    # A:B = 2:3, B:C = 4:5 -> make B equal: B = 12
    a, b, c = F(2 * 4), F(3 * 4), F(3 * 5)   # 8 : 12 : 15
    c_share = 7000 * c / (a + b + c)
    return pick(c_share, ["A. Rs. 1,600", "B. Rs. 3,000", "C. Rs. 2,400", "D. Rs. 3,500"])


def q9():
    # Alloy 1: Cu 3/5, Zn 2/5. Alloy 2: Cu 1/5, Zn 4/5.
    # Mix x:y with equal Cu and Zn: 3x + y = 2x + 4y -> x = 3y
    cu1, zn1, cu2, zn2 = F(3, 5), F(2, 5), F(1, 5), F(4, 5)
    # (cu1 - zn1) x = (zn2 - cu2) y
    ratio = (zn2 - cu2) / (cu1 - zn1)   # x / y
    options = ["A. 1:3", "B. 2:3", "C. 3:1", "D. 4:1"]
    for opt in options:
        p, q = map(int, opt.split(". ")[1].split(":"))
        if F(p, q) == ratio:
            return opt


def q10():
    # Income 7k, 5k; expenditure 3m, 2m; savings 4000 each.
    # 7k - 3m = 4000 ; 5k - 2m = 4000
    # Solve the 2x2 system with Cramer's rule.
    a1, b1, c1 = 7, -3, 4000
    a2, b2, c2 = 5, -2, 4000
    det = a1 * b2 - a2 * b1
    k = F(c1 * b2 - c2 * b1, det)
    ahmad_income = 7 * k
    return pick(ahmad_income, ["A. Rs. 20,000", "B. Rs. 24,000", "C. Rs. 32,000", "D. Rs. 28,000"])


if __name__ == "__main__":
    for i in range(1, 11):
        print(f"Q{i}:", globals()[f"q{i}"]())