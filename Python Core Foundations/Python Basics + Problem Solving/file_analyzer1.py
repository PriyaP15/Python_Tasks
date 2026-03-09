fileread=open("example.txt",'r')
lines=1
wordcount=1

file=fileread.read()

total_lines=file.splitlines()
print("Total lines: ",len(total_lines))
print("Total words: ",len(file.split()))