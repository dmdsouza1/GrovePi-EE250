Question 4 REFLECTION QUESTIONS

4.1

git clone git@github.com:my-name/my-imaginary-repo.git
touch my_second_file.py
git add my_second_file.py
git commit -m "Adding a second file"
git push --set-upstream origin master #Assuming that you are pushing to the master branch or just git push


4.2

I wrote code on my VM and pushed to my lab02 branch on my repo. I then pulled the code from the repo onto my Rpi and used nano to edit minor changes. I can be more efficient if I learn how to use text-based editors so I can code on the SSHed Rpi terminal so it will be faster to test code and make changes quicker.

4.3 

There are two 0.1s => 2*0.1 = 0.2s sleep command in the analogRead() function. Additionally, in the ultrasonicRead() function there is a 0.2s sleep command as well. So in total there is a 0.4s delay.

The Raspberry pi uses the I2C communication protocol to communicate with teh Atmega328P on the GrovePi