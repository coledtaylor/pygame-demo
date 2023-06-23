import math
from functools import reduce
import operator


def linear_conversion(X, m, k, b, c):
    return m * (X - c) / (k + b)


def logarithmic_conversion(X, m, k, b, c):
    return (math.log10(X / (1 - X)) + (10 * b)) / (10 / m)


def sinus_conversion(X, m, k, b, c):
    return math.sin((X - c) * m * (2 * math.pi)) * (k / 2) + (b + 0.5)


def boolean_conversion(V, isHighPositive, BreakPoint):
    minValue = 0.0  # Set the minimum value of the concern
    maxValue = 1.0  # Set the maximum value of the concern

    # Normalize the input value between 0 and 1
    V_normalized = (V - minValue) / (maxValue - minValue)

    if V_normalized > BreakPoint:
        if isHighPositive:
            return 1.0
        else:
            return 0.0
    else:
        if isHighPositive:
            return 0.0
        else:
            return 1.0


# Example usage
X = 0.75  # Sample input value
m = 1.5  # Slope of the curve or frequency of the wave
k = 2.0  # Vertical size of the curve
b = 0.2  # Vertical shift of the curve
c = 0.5  # Horizontal shift of the curve
V = 0.75  # Sample input value
isHighPositive = True  # Indicator for high positive concern
BreakPoint = 0.5  # Threshold value for the breakpoint

Y_linear = linear_conversion(X, m, k, b, c)
Y_logarithmic = logarithmic_conversion(X, m, k, b, c)
Y_sinus = sinus_conversion(X, m, k, b, c)
Y_boolean = boolean_conversion(V, isHighPositive, BreakPoint)

print("Utility values:")
print("Linear Conversion:", Y_linear)
print("Logarithmic Conversion:", Y_logarithmic)
print("Sinus Conversion:", Y_sinus)
print("Boolean Conversion:", Y_boolean)
