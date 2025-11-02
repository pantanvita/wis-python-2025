# Program to calculate the area and perimeter of a rectangle (if-else-elif statements)

print("This program will calculate the area and perimeter of a rectangle having a user-specified length and width.")

# To check if length and width are positive numbers and not strings

def rectangle_areaperi(userinput):
    """Calculate the area and perimeter of a rectangle."""
    while True:
        try:
            value= float(input(userinput))
            if value <=0:
                print("Please enter a positive number greater than zero")
            else:
                return value
        except ValueError:
            print("Invalid input! Please enter a numeric value")

# Taking user input

length= rectangle_areaperi("Enter the length of the rectangle: ")
width= rectangle_areaperi("Enter the width of the rectangle: ")

# Formula to calculate area and perimeter

area= length * width

perimeter= 2 * (length + width)

# Print the outputs

print(f"The area of the rectangle is: {area} sq units")
print(f"The perimeter of the rectangle is: {perimeter} units")

# Compare area and perimeter of the rectangle

if area > perimeter:
    print("The area is greater than the perimeter.")
elif area < perimeter:
    print("The perimeter is greater than the area.")
else:
    print("The area and perimeter are equal.")


