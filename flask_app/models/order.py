from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Order:
    db_name='loginregister'
    def __init__(self,data):
        self.id = data['id'],
        self.fullName = data['fullName'],
        self.numbers = data['numbers'],
        self.model = data['model'],
        self.color = data['color'],
        self.sizeBuy = data['sizeBuy'],
        self.address = data['address'],
        self.cardno = data['cardno'],
        self.cardexp = data['cardexp'],
        self.user_id = data['user_id'],

    @classmethod
    def getAllOrders(cls):
        query = 'SELECT * FROM orders;'
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        for row in results:
            users.append(row)
        return users
    
    @classmethod
    def get_order_by_id(cls,data):
        query = 'SELECT * FROM orders WHERE orders.user_id = %(user_id)s ;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        users = []
        for row in results:
            users.append(row)
        return users
    
    @classmethod
    def create_order(cls,data):
        query = 'INSERT INTO orders (fullName,user_id, numbers, address, cardno,cardexp,model, color, sizeBuy ) VALUES ( %(fullName)s,%(user_id)s, %(numbers)s, %(address)s, %(cardno)s,%(cardexp)s,%(model)s,%(color)s,%(sizeBuy)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def save(cls, data):
        query= 'SELECT * FROM orders WHERE orders.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['fullName']): 
            flash("You must complete the name and surname!", 'NameSurname')
            is_valid = False
        if len(user['number']) < 10:
            flash("Your phone number should be at least 10 numbers", 'phone')
            is_valid = False
        if len(user['address']) < 3:
            flash("Address must be at least 3 characters.", 'address')
            is_valid = False
        if len(user['cardno']) < 8:
            flash("Card number must be completed.", 'cardno')
            is_valid = False
        if len(user['cardexp']) < 8:
            flash("Please complete the expirancy date", 'cardexp')
            is_valid = False
        return is_valid