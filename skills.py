valid = ("rock", "paper", "scissors")
choice = input("What is your choice? ").lower()
while choice not in valid:
    print("\033[1A\033[K", end="")
    choice = input("Invalid choice.  Try again: ").lower()
print("\033[1A\033[K", end="")