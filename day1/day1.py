from collections import Counter

with open("data.txt", "r") as file:
    numbers = [int(num) for line in file for num in line.split()]

left_list = numbers[0::2]
right_list = numbers[1::2]

print("left list numbers:", left_list)
print("right list numbers:", right_list)
print("\n")

left_list_sorted = sorted(left_list)
right_list_sorted = sorted(right_list)

print("Sorted left list numbers:", left_list_sorted)
print("Sorted right list numbers:", right_list_sorted)
print("\n")

distances = [abs(a - b) for a, b in zip(left_list_sorted, right_list_sorted)]
total_distance = sum(distances)

print("Distances between corresponding numbers:", distances)
print("Sum of all distances:", total_distance)
print("\n")

right_count = Counter(right_list)

similarities = [num * right_count[num] for num in left_list]

similarities_sum = sum(similarities)

print("List of similarities:", similarities)
print("Sum of similarities:", similarities_sum)