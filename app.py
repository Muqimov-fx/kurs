from flask import Flask, render_template, request, redirect, url_for, send_file, session
import os

app = Flask(__name__)
app.secret_key = 'superdev_secret_key'

@app.route('/download-eri')
def download_eri():
    return send_file_mock('mirfayz_eri_key.pfx')

@app.route('/download-key/<key_id>')
def download_key(key_id):
    filename = f"{key_id}.pfx"
    return send_file_mock(filename)

def send_file_mock(filename):
    file_path = filename
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write(f'MOCK KEY CONTENT FOR {filename}')
    return send_file(file_path, as_attachment=True, download_name=filename)

import random
from datetime import datetime, timedelta

# In-memory database (Mock DB)
users_db = {}

# Helper to get current user data
def get_current_user_data():
    if 'user' not in session:
        return None
    username = session['user']
    if username not in users_db:
        users_db[username] = {'keys': []}
    return users_db[username]

@app.route('/about')
def about():
    # Login talab qilinmaydi, hamma ko'ra olishi kerak
    return render_template('about.html')

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_data = get_current_user_data()
    active_keys_count = len(user_data['keys'])
    
    return render_template('index.html', user=session['user'], active_keys=active_keys_count)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = "Mirfayz" # Default fallbadk
        if request.form.get('email'):
             email = request.form.get('email')
             session['user'] = email.split('@')[0].capitalize()
        # Ensure user exists in DB
        get_current_user_data()
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            session['user'] = name
        else:
             session['user'] = "Yangi Foydalanuvchi"
        # Create DB entry
        get_current_user_data()
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/create-eri')
def create_eri():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('create_eri.html', user=session['user'])

@app.route('/api/generate-key', methods=['POST'])
def generate_key_api():
    if 'user' not in session:
        return {"error": "Unauthorized"}, 401
    
    user_data = get_current_user_data()
    
    # Generate mock key data
    new_key_id = f"KEY-{random.randint(1000, 9999)}"
    now = datetime.now()
    expire_date = now + timedelta(days=730) # 2 years
    
    new_key = {
        'id': new_key_id,
        'name': f"Shaxsiy ERI ({len(user_data['keys']) + 1})",
        'created_at': now.strftime("%d-%b, %Y"),
        'expires_at': expire_date.strftime("%d-%b, %Y"),
        'status': 'Faol',
        'file': f"{new_key_id}.pfx"
    }
    
    user_data['keys'].append(new_key)
    
    return {"status": "success", "key_id": new_key_id, "file_url": url_for('download_key', key_id=new_key_id)}

@app.route('/keys')
def keys():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_data = get_current_user_data()
    return render_template('keys.html', keys=user_data['keys'])

@app.route('/keys/<key_id>')
def manage_key(key_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    user_data = get_current_user_data()
    
    # Find key
    key = next((k for k in user_data['keys'] if k['id'] == key_id), None)
    if not key:
        return "Kalit topilmadi", 404
        
    return render_template('manage_key.html', key=key)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
