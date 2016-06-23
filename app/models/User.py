from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def show_all_users(self):
        query = "SELECT * FROM users"
        all_users = self.db.query_db(query)
        return all_users

    def show_user_by_id(self, u_id):
        
        query = "SELECT * FROM users WHERE id=:id"
        info = {
    		'id': u_id
    	}
        user = self.db.query_db(query, info)
        print user
        return user

    def login_user(self, requestform):
        info = {
            'email': requestform['email'],
            'password': requestform['password']
        }
        errors = []
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        user_data = {'email': info['email']}
        user = self.db.query_db(user_query, user_data)
        if user:
           # check_password_hash() compares encrypted password in DB to one provided by user logging in
            if self.bcrypt.check_password_hash(user[0]['pw_hash'], info['password']):
                return { "status": True, "user": user[0]}
        else:
            errors.append('Incorrect Email or Password')
            return {"status": False, "errors": errors}


    def add_user(self, requestform):
        info = {
    		'firstname': requestform['firstname'], 
    		'lastname': requestform['lastname'], 
    		'email': requestform['email'],
    		'user_level': requestform['user_level'],
    		'password': requestform['password'],
    		'confirmation': requestform['confirmation']

    	}
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        PASS_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')
        USER_REGEX = re.compile(r'^[a-zA-Z]+$')
        errors = []
        # Some basic validation
        if not info['firstname']:
            errors.append('First name cannot be blank')
        elif len(info['firstname']) < 2:
            errors.append('first name must be at least 2 characters long')
        elif not USER_REGEX.match(info['firstname']):
            errors.append('first name can contain only letters')
        if not info['lastname']:
            errors.append('Last name cannot be blank')
        elif len(info['lastname']) < 2:
            errors.append('Last name must be at least 2 characters long')
        elif not USER_REGEX.match(info['firstname']):
            errors.append('first name can contain only letters')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif not PASS_REGEX.match(info['password']):
            errors.append('Password must contain an uppercase letter and a number')
        elif info['password'] != info['confirmation']:
            errors.append('Password and confirmation must match!')
        # If we hit errors, return them, else return True.
        if errors:
            return {"status": False, "errors": errors}
        else:
            pw_hash = self.bcrypt.generate_password_hash(info['password'])
            insert_query = "INSERT INTO users (firstname, lastname, email, user_level, pw_hash, created_at, updated_at) VALUES (:firstname, :lastname, :email, :user_level, :pw_hash, NOW(), NOW())"
            data = { 'firstname': info['firstname'], 'lastname': info['lastname'], 'email': info['email'], 'user_level': info['user_level'], 'pw_hash': pw_hash }
            print data
            self.db.query_db(insert_query, data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            if users[0]['id'] == 1:
                query = "UPDATE users SET user_level='admin' WHERE id=0"
                self.db.query_db(query)
            return { "status": True, "user": users[0]}

    def infoupdate(self, requestform):
        info = {
    		'firstname': requestform['firstname'], 
    		'lastname': requestform['lastname'], 
    		'email': requestform['email'],
    		'user_level': requestform['user_level'],
    		'id': requestform['id']
    	}
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        USER_REGEX = re.compile(r'^[a-zA-Z]+$')
        errors = []
        # Some basic validation
        if not info['firstname']:
            errors.append('First name cannot be blank')
        elif len(info['firstname']) < 2:
            errors.append('first name must be at least 2 characters long')
        elif not USER_REGEX.match(info['firstname']):
            errors.append('first name can contain only letters')
        if not info['lastname']:
            errors.append('Last name cannot be blank')
        elif len(info['lastname']) < 2:
            errors.append('Last name must be at least 2 characters long')
        elif not USER_REGEX.match(info['firstname']):
            errors.append('first name can contain only letters')
        if not info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email format must be valid!')
        if errors:
            return {"status": False, "errors": errors, "user_id": info['id']}
        else:
            query = "UPDATE users SET firstname=:firstname, lastname=:lastname, email=:email, user_level=:user_level WHERE id=:id"
            self.db.query_db(query, info)
            return {"status": True, "id": info['id']}

    def pw_update(self, requestform):
        info = {
    		'password': requestform['password'],
    		'confirmation': requestform['confirmation'],
    		'id':requestform['id']
    	}
        errors = []
        PASS_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif not PASS_REGEX.match(info['password']):
            errors.append('Password must contain an uppercase letter and a number')
        elif info['password'] != info['confirmation']:
            errors.append('Password and confirmation must match!')
        # If we hit errors, return them, else return True.
        if errors:
            return {"status": False, "errors": errors, "user_id": info['id']}
        else:
            pw_hash = self.bcrypt.generate_password_hash(info['password'])
            query = "UPDATE users SET pw_hash= pw_hash WHERE id=:id"
            self.db.query_db(query, info)
            return {"status": True, "id": info['id']}

    def desc_update(self, requestform):
        info = {
    		'description': requestform['description'],
    		'id': requestform['id']
    	}
        query = "UPDATE users SET description=:description WHERE id=:id"
        self.db.query_db(query, info)
        return {"status": True, "id": info['id']}

    def delete_user(self, requestform):
        info = {
            'id': requestform['user_id']
        }
        query = 'DELETE FROM users WHERE id=:id'
        self.db.query_db(query, info)
        status = 'success'
        return status


    def show_messages(self, u_id):
        query= 'SELECT messages.message, messages.created_at AS created_at, users.firstname, users.lastname, users.id AS message_user_id, messages.id AS message_id FROM users LEFT JOIN messages ON users.id = messages.touser_id WHERE messages.message_id IS NULL AND messages.touser_id =:id ORDER BY messages.created_at DESC'
        info = {
    		'id': u_id
    	}
        messages = self.db.query_db(query, info)
        return messages

    def show_comments(self, u_id):
        query= "SELECT messages.message, messages.created_at AS created_at, users.firstname, users.lastname, users.id AS message_user_id, messages.id AS message_id, messages.message_id AS match_id  FROM users  LEFT JOIN messages ON users.id = messages.touser_id WHERE messages.touser_id = :id AND messages.message_id IS NOT NULL ORDER BY messages.created_at DESC"
        info = {
            'id': u_id
        }
        comments = self.db.query_db(query, info)
        return comments


    def add_message(self, requestform):
        info = {
			'message': requestform['message'],
			'touser_id': requestform['touser_id'],
			'user_id': requestform['user_id']
		}
        query = "INSERT INTO messages (message, users_id, touser_id, created_at)" \
		"VALUES (:message, :user_id, :touser_id, NOW())"
        message = self.db.query_db(query, info)
        return info['touser_id']


    def add_comment(self, requestform):
        info = {
			'message': requestform['message'],
			'touser_id': requestform['touser_id'],
			'user_id': requestform['user_id'],
			'message_id': requestform['message_id']
		}
        query = "INSERT INTO messages (message, users_id, touser_id, message_id, created_at) VALUES (:message, :user_id, :touser_id, :message_id, NOW())"
        comment = self.db.query_db(query, info)
        return info['touser_id']



