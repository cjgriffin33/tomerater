class User(object):
	def __init__(self, name, email):
		self.name = name
		self.email = email
		self.books = {}

	# Returns user's email
	def get_email(self):
		return self.email

	# Changes user's email
	def change_email(self, address):
		self.email = address
		print('{name}\'s email has been changed to {email}.'.format(name=self.name, email=self.email))
		
	# Returns user's name
	def get_name(self):
		return self.name

	def __repr__(self):
		return 'User {name}; Email: {email}; Books read: {book_count}'.format(name=self.name, email=self.email, book_count=self.get_read_count())

	# Two Users are equal if their name and email address are the same
	def __eq__(self, other_user):
		if self.name == other_user.name and self.email == other_user.email:
			return True
		else:
			return False
		
	# Stores book that has been read with an optional rating
	def read_book(self, book, rating=None):
		self.books[book] = rating
	
	# Returns average rating of all books user has read ignoring those with no rating
	def get_average_rating(self):
		total_rating = 0
		rating_count = 0
		for rating in self.books.values():
			if rating in range(5):
				total_rating += rating
				rating_count += 1
		return total_rating/rating_count
		
	# Returns number of books user has read
	def get_read_count(self):
		return len(self.books)
			
class Book():
	def __init__(self, title, isbn):
		self.title = title
		self.isbn = isbn
		self.ratings = []
		
	# Returns book's title
	def get_title(self):
		return self.title
		
	# Returns book's ISBN
	def get_isbn(self):
		return self.isbn
		
	# Changes book's ISBN
	def set_isbn(self, isbn):
		self.isbn = isbn
		print('The ISBN for "{title}" has been updated to {isbn}'.format(title=self.title, isbn=self.isbn))
		
	# Adds a rating to the book's rating list if it is a valid rating (0-4)
	def add_rating(self, rating):
		if rating in range(5):
			self.ratings.append(rating)
		elif rating is None:
			print('No rating provided.')
		else:
			print('"Invalid rating: {rating}"'.format(rating=rating))
	
	# Two Books are equal if their name and isbn are the same
	def __eq__(self, other_book):
		if self.name == other_book.name and self.isbn == other_book.isbn:
			return True
		else:
			return False
			
	def __hash__(self):
		return hash((self.title, self.isbn))
		
	def __repr__(self):
		return '{title}, ISBN: {isbn}'.format(title=self.title, isbn=self.isbn)
		
	# Returns the average rating for the book
	def get_average_rating(self):
		total_rating = 0
		for rating in self.ratings:
			total_rating += rating
		return total_rating/len(self.ratings)
		
# Class Fiction extends Book
class Fiction(Book):
	def __init__(self, title, author, isbn):
		super().__init__(title, isbn)
		self.author = author
		
	# Returns fiction book's author
	def get_author(self):
		return self.author
		
	def __repr__(self):
		return '{title} by {author}'.format(title=self.title, author=self.author)
		
# Class Non_Fiction extends Book
class Non_Fiction(Book):
	def __init__(self, title, subject, level, isbn):
		super().__init__(title, isbn)
		self.subject = subject
		self.level = level
		
	# Returns non-fiction book's subject
	def get_subject(self):
		return self.subject
		
	# Returns non-fiction book's level
	def get_level(self):
		return self.level
		
	def __repr__(self):
		return '{title}, a {level} manual on {subject}'.format(title=self.title, level=self.level, subject=self.subject)
		
# Main TomeRater class
class TomeRater():
	def __init__(self):
		self.users = {}
		self.books = {}
		
	# Creates new instance of Book class
	def create_book(self, title, isbn):
		return Book(title, isbn)
		
	# Creates new instance of Fiction class
	def create_novel(self, title, author, isbn):
		return Fiction(title, author, isbn)
		
	# Creates new instance of Non_Fiction class
	def create_non_fiction(self, title, subject, level, isbn):
		return Non_Fiction(title, subject, level, isbn)
		
	# Adds a book to a user if user exists, adds optional rating to the book, and increases the read count for the book
	def add_book_to_user(self, book, email, rating=None):
		if email in self.users.keys():
			user = self.users.get(email)
			user.read_book(book, rating)
			book.add_rating(rating)
			if book in self.books.keys():
				self.books[book] += 1
			else:
				self.books[book] = 1
		else:
			print('"No user with email {email}"'.format(email=email))
			
	# Adds a user to TomeRater, and adds optional list of read books to the new user
	def add_user(self, name, email, user_books=None):
		self.users[email] = User(name, email)
		if user_books is not None:
			for book in user_books:
				self.add_book_to_user(book, email)
				
	# Iterates through all read books and prints their string representation
	def print_catalog(self):
		for book in self.books.keys():
			print(book)
			
	# Iterates through all users and prints their string representation
	def print_users(self):
		for user in self.users.values():
			print(user)
			
	# Returns the Book with the highest read count
	def most_read_book(self):
		read_count = 0
		read_book = None
		for book, count in self.books.items():
			if count > read_count:
				read_count = count
				read_book = book
		return read_book
		
	# Returns the Book with the highest average rating
	def highest_rated_book(self):
		current_high_average = 0
		current_high_book = None
		for book in self.books.keys():
			average = book.get_average_rating()
			if average > current_high_average:
				current_high_average = average
				current_high_book = book
		return current_high_book
		
	# Returns the User with the highest review average
	def most_positive_user(self):
		current_high_average = 0
		current_high_user = None
		for user in self.users.values():
			average = user.get_average_rating()
			if average > current_high_average:
				current_high_average = average
				current_high_user = user
		return current_high_user
		
	# Returns the read count for passed Book
	def get_read_count(self, book):
		return self.books.get(book, 0)
		
	# Returns a list of the n most read Books, in descending order
	def get_n_most_read_books(self, n):
		temp_books = self.books.copy()
		sorted_books = []
		# Limit number of iterations to number of Books
		if n > len(temp_books):
			n = len(temp_books)
		for i in range(n):
			highest_read_count = 0
			most_read_book = None
			for book, count in temp_books.items():
				if count > highest_read_count:
					highest_read_count = count
					most_read_book = book
			sorted_books.append(most_read_book)
			temp_books.pop(most_read_book)
		return sorted_books
		
	# Returns a list of n Users with the highest read count, in descending order
	def get_n_most_prolific_readers(self, n):
		temp_users = self.users.copy()
		sorted_users = []
		# Limit number of iterations to number of Users
		if n > len(temp_users):
			n = len(temp_users)
		for i in range(n):
			highest_read_count = 0
			highest_read_user = None
			for user in temp_users.values():
				if user.get_read_count() > highest_read_count:
					highest_read_count = user.get_read_count()
					highest_read_user = user
			sorted_users.append(highest_read_user)
			temp_users.pop(highest_read_user.get_email())
		return sorted_users
		
	# Returns a list of n Books with the highest average rating, in descending order
	def get_n_highest_rated_books(self, n):
		temp_books = self.books.copy()
		sorted_books = []
		# Limit number of iterations to number of Books
		if n > len(temp_books):
			n = len(temp_books)
		for i in range(n):
			highest_average = -1
			highest_rated_book = None
			for book in temp_books.keys():
				rating = book.get_average_rating()
				if rating > highest_average:
					highest_average = rating
					highest_rated_book = book
			sorted_books.append(highest_rated_book)
			temp_books.pop(highest_rated_book)
		return sorted_books