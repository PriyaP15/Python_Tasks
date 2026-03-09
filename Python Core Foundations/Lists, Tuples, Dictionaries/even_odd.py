values = input("Enter the elements to seperate even and odd numbers: ").split()

lst=[int(i) for i in values]
even=[i for i in lst if i%2==0]
odd=[i for i in lst if i%2!=0]

if len(even)==0:
    print("\nNo even numbers")
else:
    print(f"Even list: {even}")

if len(odd)==0:
    print("No odd numbers")
else:
    print(f"Odd list: {odd}")