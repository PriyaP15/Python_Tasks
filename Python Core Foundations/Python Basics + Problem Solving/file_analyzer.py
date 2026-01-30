fileread=open("example.txt",'r')
lines=1
wordcount=0

file=fileread.read()
if file=='':
    print(0,"line")
    print(0,"word")
else:
    for line in file:
        if line==' ':
            wordcount+=1
        elif line=='\n':
            lines+=1

    print(lines,"line")
    print(wordcount+lines,"word")