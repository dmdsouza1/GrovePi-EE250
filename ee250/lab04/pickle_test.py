import pickle

notes = []

# TODO: Using the pickle module...

# A. If notes.pickle exists, read it in using pickle and assign the content to
#   the notes variable

try:
	infile = open('notes.pickle','rb')
	while True:
		try:
			notes.append(pickle.load(infile))
		except EOFError:
			break

except FileNotFoundError:

	outfile = open('notes.pickle','wb')
	
	outfile.close()

print(type(notes))
print(notes)



s = input("Enter something to append to notes ")

outfile = open('notes.pickle','a+b')
pickle.dump(s, outfile)
outfile.close()



# B. Print out notes

# C. Read in a string from the user using input() and append it to notes

# D. Save notes to notes.pickle

