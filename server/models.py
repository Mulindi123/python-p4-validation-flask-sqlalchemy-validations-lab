from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Author name is required")
        return value
    
    # __table_args__= (db.UniqueConstraint("name", name="unique_author_name"))
    
    @validates("phone_number")
    def validate_phone_number(self, key, value):
        #ensure the phone number is exactly 10 digits
        if value and len(value) != 10:
            raise ValueError("Author phone number must be exactly ten digits")
        return value
    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("title")
    def validate_title(self, key, title):
        required_phrases = ["Won't Believe", "Secret", r"Top \d+", "Guess"]
        if not any(phrase in title for phrase in required_phrases):
            raise ValueError("Title should be clickbait-y and contain at least one of: 'Won't Believe', 'Secret', 'Top [number]', 'Guess'")
        
        return title

    @validates("content")
    def validates_content(self, key, content):

        #Ensure the post content is atleast 250 characters long
        if len(content)< 250:
            raise ValueError("Post content must be atleast 250 characters long")
        return content
    
    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) >= 250:
            raise ValueError("Summary too long. More than 250 chars.")
        return summary
    
    @validates("category")
    def validate_category(self, key, category):
        if category !="Fiction" and category!= "Non-Fiction":
            raise ValueError("Post category must be eitherFiction or Non-Fiction")
        
        return category


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
