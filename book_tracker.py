#personal book tracker
import json
import requests
import os

def book_track():
    print("===Personal Book Tracker===")
    while True:
        print("1. Search book\n2. View saved book(s)\n3. Remove book(s)\n4. Exit")
        choice = input("Choose: ")
        if choice.lower() in ["search book", "search books", "1"]:
            book = input("Book name: ")
            api_key = os.environ.get("BOOKS_API_KEY")
            url = f"https://www.googleapis.com/books/v1/volumes?q={book}&key={api_key}"
            response = requests.get(url)
            data = response.json()
            book_info = data["items"][0]["volumeInfo"]
                
            print(f"Title: {book_info['title']}")
            print(f"Author: {book_info['authors'][0]}")
            print(f"Published: {book_info['publishedDate']}")

            while True:
                save = input("Do you want to save this book? (y/n): ")
                if save.lower() in ["yes", "y"]:
                    try:
                        with open("books.json", "r") as file:
                            books  = json.load(file)

                    except (FileNotFoundError, json.JSONDecodeError):
                        books = []
                        books.append(data)
                    with open("books.json", "w") as file:
                        json.dump(books, file, indent=2, sort_keys=True)
                        print("Book is saved\n")
                        break
                elif save.lower() in ["no", "n"]:
                    print("\n")
                    break
                else:
                    print("Please put yes or no")
        elif choice.lower() in ["view book", "view books", "2"]:
            try:
                    with open("books.json", "r") as file:
                        books = json.load(file)
                    for i in books:
                        info = books["items"][0]["volumeInfo"]
                        print(f"Title: {info['title']}, by {info['authors'][0]}")
            except FileNotFoundError:
                print("No book saved yet\n")

        elif choice.lower() in ["remove book", "remove books", "3"]:
            try:
                with open("books.json", "r") as file:
                    books = json.load(file)
                for i in range(len(books)):
                    print(f"{i + 1}. {books[i]['items'][0]['volumeInfo']['title']}")
                remove = int(input("Which book would you like to remove? "))
                books.pop(remove - 1)

                with open("books.json", "w") as file:
                    json.dump(books, file, indent=2, sort_keys=True)
                print("Book succesfully removed!\n")

            except FileNotFoundError:
                print("No books in the gallery yet")
            
            
        elif choice.lower() in ["exit", "4"]:
            print("Bye!")
            break

        else:
            print("Invalid input please try again\n")


book_track()