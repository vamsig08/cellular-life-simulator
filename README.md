# cellular-life-simulator
Write a C / C++ program that reads signed integer data from a file, makes decisions upon each integer in the file, and then writes each integer to one or more files. The goal of the assignment is to implement this program using multithreading and mutex locks or semaphores to ensure that the various threads don’t interfere with one another.
At minimum, your solution must be divided across two threads:
1. A reader thread that reads data from the file and puts it into a buffer.
2. A processor thread that reads data from the buffer, determines which files to write the data to, then writes the integer to those files.

