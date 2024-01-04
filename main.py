import pickle
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value
        return False
    
class Birthday(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 8:
            raise ValueError("Invalid birthday format")
        super().__init__(value)

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        if new_phone not in self.phones:
            self.phones.append(new_phone)

    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)
        if found_phone:
            self.phones.remove(found_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def edit_phone(self, old_phone, new_phone):
        found_phone = self.find_phone(old_phone)
        if found_phone:
            found_phone.value = new_phone
        else:
            raise ValueError(f"Phone {old_phone} not found for contact {self.name.value}")

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today().date()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
            days_left = (next_birthday - today).days
            return days_left
        return None

    def __str__(self):
        phones_str = "; ".join(str(p) for p in self.phones)
        birthday_str = f", Birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, query):
        results = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower() or any(query in phone.value for phone in record.phones):
                results.append(record)
        return results

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

def search_contacts(address_book):
    query = input("Enter search query: ")
    results = address_book.find(query)
    if results:
        print("Search results:")
        for record in results:
            print(record)
    else:
        print("No matching contacts found.")

def main():
    address_book = AddressBook()

    while True:
        print("1. Add a new contact")
        print("2. List contacts")
        print("3. Search contacts")
        print("4. Save to file")
        print("5. Load from file")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                name = input("Enter contact name: ")
                phone = input("Enter contact phone: ")
                birthday = input("Enter contact birthday (ddmmyyyy): ")

                new_record = Record(name, phone, birthday)
                address_book.add_record(new_record)
                print("Contact added successfully!")
            except ValueError as e:
                print(f"Error: {e}. Please try again.")

        elif choice == "2":
            records = address_book.data.values()
            for record in records:
                print(record)

        elif choice == "3":
            search_contacts(address_book)

        elif choice == "4":
            filename = input("Enter the filename to save to: ")
            address_book.save_to_file(filename)
            print("Address book saved successfully!")

        elif choice == "5":
            filename = input("Enter the filename to load from: ")
            address_book.load_from_file(filename)
            print("Address book loaded successfully!")

        elif choice == "6":
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()
