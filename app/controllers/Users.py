from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.db = self._app.db

    def index(self):
        return self.load_view('index.html')


    def dashboard(self):
        all_users = self.models['User'].show_all_users()
        return self.load_view('dashboard.html', all_users= all_users)


    def signin(self):   
        return self.load_view('signin.html')
       


    def register(self):
        return self.load_view('register.html')
        


    def show(self, user_id):
        user = self.models['User'].show_user_by_id(user_id)
        messages = self.models['User'].show_messages(user_id)
        comments = self.models['User'].show_comments(user_id)
        print "this is the comment data", comments
        return self.load_view('show.html',user= user[0], messages= messages, comments= comments)


    def edit(self, user_id):
        user = self.models['User'].show_user_by_id(user_id)
        print user
        return self.load_view('profile.html', user= user[0])
        


    def add(self):
        requestform = request.form
        create_status = self.models['User'].add_user(requestform)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id'] 
            session['user_level'] = create_status['user']['user_level']
            return redirect('users/dashboard')
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/users/register')  
    	

    def login(self):
        requestform = request.form
        login_status = self.models['User'].login_user(requestform)
        if login_status['status'] == True:
            session['id'] = login_status['user']['id'] 
            session['user_level'] = login_status['user']['user_level']  
            return redirect('users/dashboard')
        else:
            for message in login_status['errors']:
                flash(message, 'login_errors')
            return redirect('/users/signin')

    def admin_add(self):
        requestform = request.form
        create_status = self.models['User'].add_user(requestform)
        if create_status['status'] == True:
            return redirect('users/dashboard')
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('/users/register')


    def admin_delete(self):
        requestform = request.form
        delete_status = self.models['User'].delete_user(requestform)
        return redirect('users/dashboard')


    def info_update(self):
        requestform = request.form
        update_status = self.models['User'].infoupdate(requestform)
        if update_status['status'] == True:
            return redirect('users/dashboard')
        else:
            for message in update_status['errors']:
                flash(message, 'update_errors')
            return redirect('/users/edit/'+update_status['user_id'])

    def password_update(self):
        requestform = request.form
        update_status = self.models['User'].pw_update(requestform)
        if update_status['status'] == True:
            return redirect('users/dashboard')
        else:
            for message in update_status['errors']:
                flash(message, 'update_errors')
            return redirect('/users/edit/'+update_status['user_id'])


    def description_update(self):
        requestform = request.form
        update_status = self.models['User'].desc_update(requestform)
        if update_status['status'] == True:
            return redirect('users/dashboard')
        else:
            for message in update_status['errors']:
                flash(message, 'update_errors')
            return redirect('/users/edit/'+update_status['user_id'])


    def message(self):
        requestform = request.form
        user_id = self.models['User'].add_message(requestform)
        return redirect('users/show/'+user_id)


    def comment(self):
        requestform = request.form
        user_id = self.models['User'].add_comment(requestform)
        return redirect('users/show/'+user_id)

    def logoff(self):
        session.clear
        return redirect('/')




