# StatisticalLibrary.py

# Prompts the user for 5 numbers, then stores these numbers in a list
# Then calculates the min, max, mean, and standard deviation for this list,
# and stores these results in another list

# Nick Crews
# 2/15/16


# import the sqrt function necessary for the std_dev functions
import math



def mean(a_list):
	'''simple function for the mean of a list'''
	# make sure we don't divide by 0
	return sum(a_list) / max(len(a_list), 1)



def std_dev(a_list):
	'''given a_list, return standard deviation'''
	# what is the mean of this list?
	avg = mean(a_list)
	# calculate the variance of the list
	variance = mean(  [(x-avg)**2 for x in a_list] )
	return math.sqrt(variance)

def read5nums():
	'''reads 5 floats from the command line. Continues tring until success'''
	# declare our list to hold the 5 numbers
	nums = None

	# get the 5 numbers from the user
	while (True):
		raw_string = raw_input("Please input 5 numbers, separated by spaces: ")

		# try to convert the raw string to a list of floats
		try:
			nums = [float(num) for num in raw_string.split()]
		except:
			# if there was a problem, prompt the user again
			print("Could not understand that input.")
			continue


		# parsing was succesful, check that there are the correct number of elements
		if len(nums) == 5:
			# the input was totally good!
			return nums
		else:
			# tell the user, and prompt again
			print("That was not the right amount of numbers.")

def main():
	# get the data from the user
	nums = read5nums()

	# OK, we have our list of 5 numbers
	print("The numbers you entered were: {}".format(nums))

	# now lets do our calculations
	results = [min(nums), max(nums), mean(nums), std_dev(nums)]

	# and print out the results!
	print("Min: {}".format(results[0]))
	print("Max: {}".format(results[1]))
	print("Mean: {}".format(results[2]))
	print("Standard deviation: {}".format(results[3]))


if __name__ == '__main__':
	main()


