import random

def main():
    while True:
        print("Project Labyrinth")
        print("1. Start Game")
        print("2. Quit")
        choice = int(input("Enter 1 or 2: "))

        if choice == 1:
            # Start the game
            Reimu_HP = 10
            Reimu_MP = 10
            Reimu_ATK = 3
            Reimu_DEF = 2
            Marisa_HP = 15

            while Reimu_HP > 0 and Marisa_HP > 0:
                print("Reimu's HP:", Reimu_HP)
                print("Reimu's MP:", Reimu_MP)
                print("Reimu's ATK:", Reimu_ATK)
                print("Reimu's DEF:", Reimu_DEF)
                print("Marisa's HP:", Marisa_HP)
                print("\n")
                print("What will Reimu do?")
                print("1. Fantasy Seal (2 + ATK damage, 3 MP)")
                print("2. Rest (Regain 5 MP)")
                player_choice = int(input("Enter 1 or 2: "))

                if player_choice == 1:
                    # Player chose Fantasy Seal
                    if Reimu_MP >= 3:
                        Reimu_MP -= 3
                        Marisa_HP -= (2 + Reimu_ATK)
                        print("\nReimu uses Fantasy Seal!")
                        print("Marisa takes", 2 + Reimu_ATK, "damage.")
                    else:
                        print("\nReimu doesn't have enough MP to use Fantasy Seal.")
                elif player_choice == 2:
                    # Player chose Rest
                    Reimu_MP += 5
                    print("\nReimu rests and regains 5 MP.")

                # Check if Marisa is defeated
                if Marisa_HP <= 0:
                    break

                # Enemy turn
                enemy_choice = random.choice([1, 2])
                if enemy_choice == 1:
                    # Marisa uses Magic Missle
                    Reimu_HP -= max(2 - Reimu_DEF, 0)
                    print("\nMarisa uses Magic Missle!")
                    print("Reimu takes", max(2 - Reimu_DEF, 0), "damage.")
                elif enemy_choice == 2:
                    # Marisa uses Master Spark
                    Reimu_HP -= max(5 - Reimu_DEF, 0)
                    print("\nMarisa uses Master Spark!")
                    print("Reimu takes", max(5 - Reimu_DEF, 0), "damage.")

            # Check the result
            if Reimu_HP <= 0:
                print("\nReimu has been defeated. You lose.")
            else:
                print("\nMarisa has been defeated. You win!")

        elif choice == 2:
            # Quit the game
            print("Thank you for playing Project Labyrinth!")
            break

if __name__ == "__main__":
    main()
