from transcribe import transcribe_audio
import json


def get_languages():
    with open("languages.json") as f:
        data = json.load(f)
        return data
    

def show_languages(languages):
    count = 1
    for language in languages["Languages"]:
        print(f"{count}. {language['LanguageName']}")
        count += 1


def show_main_menu():
    print("1.Translate")
    print("2. Exit")

    option = int(input("\nChoose an option: "))
    if option == 1:
        pass
    elif option == 2:
        exit()
    else:
        print("Pick a valid option.\n")
        show_main_menu()


def main_menu():
    print("Welcome to Polyglot Pro")
    show_main_menu()

    languages = get_languages()
    language_input, language_output = choose_languages(languages)
    transcribe_audio(language_input, language_output)


def choose_languages(languages):
    language_input, language_output = None, None
    salir = False
    option = 0

    while not salir:
        print("\nList of languages:")
        show_languages(languages)
        language_input = int(input("\nInput language: "))
        language_output = int(input("\nOutput language: "))

        if language_input == language_output:
            print("Input and output language cannot be the same.")
        elif language_input < 1 or language_output < 1 or language_input >= len(
            languages['Languages']) + 1 or language_output >= len(languages['Languages']) + 1:
            print("Invalid option.")
        else:
            language_input = languages["Languages"][language_input - 1]["LanguageCode"]
            language_output = languages["Languages"][language_output - 1]["LanguageCode"]

            print(f"\nInput language: {language_input}")
            print(f"\nOutput language: {language_output}")
            salir = True

    return language_input, language_output


if __name__ == "__main__":
    main_menu()
