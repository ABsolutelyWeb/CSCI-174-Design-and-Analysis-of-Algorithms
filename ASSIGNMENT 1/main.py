# Python 3.6.2

# Abhishek Gupta
# Assignment 1 for CSCI 174
# Due Date: 9-15-2017


import re     # Used for sub function in regular expression when filtering out 
                    # brackets, parentheses, etc. to isolate the (x1, y1) and 
                    # (x2, y2) coordinates.

import sys    # Python library for argv[]


# We want to create a Coordinate class because we don't know how many coordinates
# we will have to deal with in the input file. This class will be useful in
# creating however many instances of Coordinate as we need to accommodate the
# number of coordinates that we are given.
class Coordinate:
    # This is our initialize function. It works a bit like a constructor in Java
    # and "self" works the same way as "this" works in Java. It is basically
    # representing an instance of the object. So "self.x" and "self.y" both
    # represent coordinates of a single point for whatever Coordinate object that
    # we create.
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Each line consists of two pairs of points. Given that we have no idea how many
# lines our input file will have, we must create a class to create as many
# instances of a line for however many lines as needed.
class Line:
    # This is our Line constructor. index represents which position a given line 
    # is in relative to the other, x1y1 represents the lines first coordinate 
    # while x2y2 represents the lines second coordinates.
    def __init__(self, index, x1y1, x2y2):
        self.index = index
        self.x1y1 = x1y1
        self.x2y2 = x2y2


# The "ccw" and "intersect" functions were taken from Bryce Boe. The article can
# be found at:
        # http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/


# Function "ccw" or "counterclockwise" takes 3 points and determines whether they
# are listed in a counterclockwise order. Assuming we have 3 points A, B, and C
# and if AB's slope is less than AC's slope, then the 3 points are counterclockwise.
# RETURN TYPE: BOOLEAN
def ccw(A, B, C):
    return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)  # Returns a true or false


# Why is the 3 points being counterclockwise significant? Assume we have two lines:
# AB and CD. The two lines are said to intersect if A, B are separated by CD AND
# C, D are separated by AB.
# However, if A, B are separated by CD, then this implies that ACD and BCD have 
# "opposite orientation meaning either ACD or BCD is counterclockwise but not both."
# RETURN TYPE: BOOLEAN
def intersect(A, B, C, D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)   # Returns a true or false
    

# Read, parse, extract information, and store information into the lines list.
# RETURN TYPE: lines LIST of objects
def get_lines(file_name):
    lines = []                                # Allocate lines variable for empty list
    with open(file_name, 'r') as f:           # Open will return a file object with "r" or read-only priviledge.
        # Read file row by row
        for row in f:
            # if row is not empty
            if row:
                # split row by :
                # For example, say s = "1: ([37.788353, -122.387695], [37.829853, -122.294312])"
                # then if we do sp = s.split(':')
                # we will get print(sp) >>> ['1', ' ([37.788353, -122.387695], [37.829853, -122.294312])']
                row_split = row.split(':')
                
                # line number
                # In the above example, "lineNumber" here would be 1.
                lineNumber = row_split[0]
                
                # coordinates
                # In the above example, "rest" here would be ([37.788353, -122.387695], [37.829853, -122.294312]).
                everythingAfterLineNum = row_split[1]

                # split coordinates and convert them from string to float
                # Store the raw points (without parentheses/brackets and other characters) inside the points list. 
                points = []
                
                # In the above example, "rest" here would be ([37.788353, -122.387695], [37.829853, -122.294312])
                # We will split by the comma and get ['([37.788353', '-122.387695]', '[37.829853', '-122.294312])']
                # However, we are using a regular expression to replace the insignificant characters with ''.
                # Therefore, we will end up with ['37.788353', '-122.387695', '37.829853', '-122.294312']
                for pt in everythingAfterLineNum.split(','):
                    new_point = re.sub(r'[^0-9.-]', '', pt)
                    
                    # Since the coordinates are strings, we need to typcast them into floats.
                    float_new_point = float(new_point)
                    
                    # Once the coordinates have been typecasted into floats, we will push them onto our
                    # points list which, given the above example, would like this:
                    # [37.788353, -122.387695, 37.829853, -122.294312]
                    points.append(float_new_point)
                
                # Now that we have extracted a line's coordinates into a list, 
                # we need to create the Coordinate objects. Two per line.
                # x1y1: x1 and y1
                # x2y2: x2 and y2
                x1y1 = Coordinate(points[0], points[1])  # Ex. 37.788353, -122.387695
                x2y2 = Coordinate(points[2], points[3])  # Ex. 37.829853, -122.294312
                
                # A line consists of two coordinates. We have made 2 Coordinate
                # objects. We will create a Line object and then assign the 2
                # Coordinate objects to this Line object.
                lineNumber = Line(int(lineNumber), x1y1, x2y2)
                
                # Store every lineNumber AKA List objects into the lines list.
                lines.append(lineNumber)
    return lines  # Return the list of line numbers


# This function checks every line and counts the number of intersections each line has.
# RETURN TYPE: count INTEGER
def check_line(lineNum, lines):
    count = 0
    
    for line in lines:
    
        # if ids of lines not equal
        if lineNum.index != line.index:
    
            # finding intersections
            if intersect(lineNum.x1y1, lineNum.x2y2, line.x1y1, line.x2y2):
                count = count + 1
    
    return count


# Use the above function to find all lines that don't have intersections.
# RETURN TYPE: lines_without_intersections LIST
def check_intersections(lines):
    
    # List for holding every line that doesn't have intersection(s).
    lines_without_intersections = []
    
    # The lines list must not be empty.
    while len(lines) > 0:
		# Used to find the high intersection for a line in a set.
        max_intersections = 0
		
		# Once we have found that line, store it in this variable.
        max_line = None  # Empty or no value here
    
        # Look for intersections.
        for line in lines:
			# Check each line and store its # of intersections in this variable.
            count_intersection = check_line(line, lines)
    
            # If there are no intersections found for a given line, add the line 
            # number to the "lines_without_intersections" list.
            if count_intersection == 0:
                lines_without_intersections.append(line)
    
            # Every time we find a line that has a greater number of intersections, we
			# store it in the max variables.
            elif count_intersection >= max_intersections:
                max_intersections = count_intersection
                max_line = line
    
        # We remove the line that has the max number of intersections.
        if max_line:
            lines.remove(max_line)
    
        # As we are iterating through the lines_without_intersections list, if we
		# find a line that is also in the lines argument, then we remove it and 
		# continue to iterate. The purpose of this loop is to also get us out of
		# the parent infinite while loop.
        for line in lines_without_intersections:
            if line in lines:
                lines.remove(line)
    return lines_without_intersections



# Take in the list of lines and then for each valid line, print out the line
# number followed by a space.
def print_result(lines_list):
    if len(lines_list) == 0:
        print("Input file is blank.")

    # Insertion Sort
	# lines_list.sort() was not working for me and I couldn't figure out why
	# beause it worked in Python 2. I think Python 3 got confused as to how to
	# sort the objects. I used insertion sort because that's what we went over
	# in class and that's what I understood fairly well.
    for index in range(1, len(lines_list)):
        value = lines_list[index].index
        i = index - 1
        while i >= 0:
            if value < lines_list[i].index:
                lines_list[i+1].index = lines_list[i].index
                lines_list[i].index = value
                i = i - 1
            else:
                break
                    
	# Take the sorted list and then print elements one-by-one
	# followed by a space.
    for line in lines_list:
        print(line.index, end=' ')
    print("")


# This is the entire program. Everything is happening here. The if statement
# makes it so the source is only ran as a standalone script.
if __name__ == '__main__':
    # Program will take a single file argument.
    file_name = sys.argv[1]
    
    # Get the lines from the file and store them.
    lines_from_file = get_lines(file_name)
    
    # From the lines you extracted from the source code, find all the ones that
    # don't have intersections.
    lines_without_intersections = check_intersections(lines_from_file) 
    
    # Print the largest set of line numbers where there exists no intersection.
    print_result(lines_without_intersections)