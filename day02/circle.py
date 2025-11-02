# Program to calculate the diameter, area and circumference of a circle from user input radius value

print("This program will calculate the diameter, area and circumference of a circle having a user-specified radius.")

# To check if radius is a positive number and not a string

def circle_area(radius):
    """Calculate the area of a circle"""
    while True:
        try:
            value= float(input(radius))
            if value <0:
                print("Please enter a positive number")
            else:
                return value
        except ValueError:
            print("Invalid input! Please enter a numeric value")

# Taking user input

radius= circle_area("Enter the radius of the circle: ")

# Formula to calculate the diameter, area and circumference
    
diameter= 2 * radius
area= 3.14 * radius * radius
circumference= 2 * 3.14 * radius

# Print the outputs

print(f"The diameter of the circle is: {diameter} units")
print(f"The area of the circle is: {area} sq units")
print(f"The circumference of the circle is: {circumference} units")



