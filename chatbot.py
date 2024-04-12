import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import datetime
import db
import requests
import json
def preprocess_text(text):
    # Tokenize, remove stop words, and stem the input text
    tokens = nltk.word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    return stemmed_tokens

def intent_recognition(text):
    # Implement intent recognition using NLTK
    intent_map = {
        'get_books_info': 'get_books_info',
        'add_new_book': 'add_new_book',
        'update_book': 'update_book',
        'view_all_books': 'view_all_books',
        'delete_book_info': 'delete_book_info',
        'delete_all_books': 'delete_all_books'
    }
    for key, value in intent_map.items():
        if key in ' '.join(text):
            return value
    return 'unknown'

def generate_response(intent, user_input):
    # Implement the dialogue management system
    # Based on the identified intent, perform the necessary actions
    from models import Book
    
    if intent == 'get_books_info':
        response_data = requests.get('http://localhost:5000/request/random')
        if response_data.status_code == 200:
            data = response_data.json()
            book = data.get('book')
            if book:
                return f"The book's name is {book['title']} and its availability is {book['available']}."
            else:
                return "No book found."
        else:
            return "Error fetching book information."
        
    elif intent == 'add_new_book':
        new_book = Book(db.getNewId(), True, 'New Book', datetime.datetime.now())
        db.insert(new_book)
        return "New book created successfully."
    
    elif intent == 'update_book':
        response_data = requests.get('http://localhost:5000/request/random')
        if response_data.status_code == 200:
            data = response_data.json()
            book = data.get(book)
            if book:
                book['available'] = False
                b = json.load(book)
                print(b)
                db.update(b)
                return "Book updated successfully."
            else:
                return "No book found."
        else:
            return "Error updating book information."
    
    elif intent == 'view_all_books':
        response_data = requests.get('http://localhost:5000/request/')
        if response_data.status_code == 200:
            data = response_data.json()
            books = data.get('res')
            if books:
                response = "Your books:\n"
                for book in books:
                    response += f"- {book['title']} (Available: {book['available']})\n"
                return response
            else:
                return "No books found."
        else:
            return "Error fetching books information."
    
    elif intent == 'delete_book_info':
        response_data = requests.delete('http://localhost:5000/request/random')
        if response_data.status_code == 200:
            return "Book deleted successfully."
        else:
            return "Error deleting book information."
    
    elif intent == 'delete_all_books':
        response_data = requests.delete('http://localhost:5000/request/')
        if response_data.status_code == 200:
            return "All books deleted successfully."
        else:
            return "Error deleting all books."
    
    else:
        return "I'm sorry, I didn't understand that request."
