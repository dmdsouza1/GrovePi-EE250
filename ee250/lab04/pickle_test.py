import pickle

notes = []

# TODO: Using the pickle module...

# A. If notes.pickle exists, read it in using pickle and assign the content to
#   the notes variable

try:
	infile = open('notes.pickle','rb')
	notes = pickle.loads(infile.read())

except FileNotFoundError:

	outfile = open('notes.pickle','wb')
	
	outfile.close()

# B. Print out notes
print(notes)


# C. Read in a string from the user using input() and append it to notes

s = input("Enter something to append to notes ")

# D. Save notes to notes.pickle
outfile = open('notes.pickle','a+b')
pickle.dump(s, outfile)
outfile.close()








