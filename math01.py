import math

def calculate_sum():
    total_sum = 0
    for a1 in range(2018):  # 0 to 2017 inclusive
        denominator = math.sqrt(a1) + math.sqrt(a1 + 1)
        total_sum += 1 / denominator
    return total_sum

result = calculate_sum()
result = result*result
print(f"The sum is approximately {result:.0f}")