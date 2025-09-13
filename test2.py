marks = {'Dhanish':100, 'Vedesh':98, 'Aditya':99, 'Shoumik':95, 'Marudai':78, 'Billie':60}
lowest = min(marks, key=marks.get)
highest = max(marks, key=marks.get)


# The variables already contain the correct names, no need for the loop
topper = highest
lowest_scorer = lowest

print(topper)
print(lowest_scorer)
print(f"The topper is {topper} with {marks[topper]} marks")
print(f"The lowest scorer is {lowest_scorer} with {marks[lowest_scorer]} marks")