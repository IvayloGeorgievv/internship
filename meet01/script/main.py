from positive_and_negative_script import run_script

def main():
    choice = input("What's the business climate right now? [P]ositive or [N]egative: ").strip().upper()

    if choice == "P" or choice == "N":
        run_script(choice)

    else:
        print("Invalid choice. Please enter 'P' or 'N'.")


if __name__ == "__main__":
    main()