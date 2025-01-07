from flask import Blueprint, request, jsonify
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from food_repo_users.database import get_db

def error_message(message='Incorrect parameters'):
    return jsonify({'error': message})

def get_expiry_time():
    return (datetime.now(timezone.utc) + timedelta(hours=24)).strftime('%Y%m%d%H%M')

bp = Blueprint('food_repo_users', __name__)

# User creation
@bp.route('/users', methods=['POST'])
def add_user():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    if first_name and last_name and email and password:
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        db = get_db()

        sql = '''
        SELECT COUNT(*)
        FROM user
        WHERE cEmail = ?
        '''
        user_count = db.execute(sql, (email,)).fetchone()
        if user_count[0] == 0:
            cursor = db.cursor()        
            cursor.execute(
                '''
                    INSERT INTO user
                        (cFirstName, cLastName, cEmail, cPassword)
                    VALUES 
                        (?, ?, ?, ?)
                ''',
                (first_name, last_name, email, password_hash)
            )
            user_id = cursor.lastrowid
            cursor.close()
            db.commit()
            return jsonify({'user_id': user_id}), 201
        else:
            return error_message('A user with this email address already exists'), 400
    else:
        return error_message(), 400
    
# User login validation
@bp.route('/auth/login', methods=['POST'])
def validate_login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        db = get_db()
        sql = '''
            SELECT nUserID, cPassword
            FROM user
            WHERE cEmail = ?
        '''
        user = db.execute(sql, (email,)).fetchone()
        
        if user != None:
            password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if user[1] == password_hash:
                # A 32-byte session token is generated
                token = secrets.token_hex(32)
                # The token will be valid for 24 hours
                expiry_datetime = get_expiry_time()

                user_id = user[0];
                cursor = db.cursor()
                cursor.execute(
                    '''
                        UPDATE user
                        SET cToken = ?,
                            dTokenExpiration = ?
                        WHERE nUserID = ?
                    ''', 
                    (token, expiry_datetime, user_id)
                )
                affected_rows = cursor.rowcount
                cursor.close()
                db.commit()
                if affected_rows == 0:
                    return error_message('It was not possible to generate a session token'), 401
                
                return jsonify({
                    'user_id': user_id,
                    'token': token
                })
            else:
                return error_message('Incorrect password'), 401
        else:
            return error_message('The user does not exist'), 404
    else:
        return error_message(), 400
    
# User logout (token invalidation)
@bp.route('/auth/logout', methods=['DELETE'])
def logout():
    token = request.headers.get('X-Session-Token')

    if not token:
        return error_message('Missing session token'), 401        

    db = get_db()
    sql = '''
        SELECT COUNT(*)
        FROM user
        WHERE cToken = ?
        AND dTokenExpiration >= ?
    '''
    current_time = datetime.now(timezone.utc).strftime('%Y%m%d%H%M')
    user_count = db.execute(sql, (token, current_time)).fetchone()
    if user_count[0] == 0:
        return error_message('Invalid or expired token'), 401

    cursor = db.cursor()
    cursor.execute(
        '''
            UPDATE user
            SET cToken = '',
                dTokenExpiration = ''
            WHERE cToken = ?
        ''',
        (token,)
    )
    affected_rows = cursor.rowcount
    cursor.close()
    db.commit()
    if affected_rows == 0:
        return error_message('It was not possible to log out'), 500
    
    return '', 204
    
# Management of user favourites
@bp.route('/users/<int:user_id>/favourites', methods=('GET', 'POST', 'DELETE'))
def manage_user_favourites(user_id):
    # Get the list of favourite recipes
    if request.method == 'GET':
        db = get_db()
        recipes = db.execute(
            '''
            SELECT nRecipeID
            FROM user_favourites
            WHERE nUserID = ?
            ''',
            (user_id,)
        ).fetchall()

        return jsonify({'recipes': [{'recipe_id': recipe[0]} for recipe in recipes]})

    # Add a new favourite recipe
    elif request.method == 'POST':
        recipe_id = request.form.get('recipe_id')
        if recipe_id is not None:
            db = get_db()
            sql = '''
                SELECT COUNT(*)
                FROM user_favourites
                WHERE nUserID = ?
                AND nRecipeID = ?
            '''
            recipe_count = db.execute(sql, (user_id, recipe_id)).fetchone()
            if recipe_count[0] == 0:
                cursor = db.cursor()
                cursor.execute(
                    '''
                        INSERT INTO user_favourites
                            (nUserID, nRecipeID)
                        VALUES
                            (?, ?)
                    ''',
                    (user_id, recipe_id)
                )
                affected_rows = cursor.rowcount
                cursor.close()
                db.commit()
                if affected_rows > 0:
                    return jsonify({'status': 'ok'})
                else:
                    return error_message('The recipe could not be added as favourite'), 500
            else:
                return error_message('The user has already favourited this recipe'), 400
        else:
            return error_message(), 400
    # Delete a favourite recipe
    elif request.method == 'DELETE':
        recipe_id = request.form.get('recipe_id')
        if recipe_id is not None:
            db = get_db()
            cursor = db.cursor()
            cursor.execute('''
                    DELETE FROM user_favourites
                    WHERE nUserID = ?
                    AND nRecipeID = ?
                ''',
                (user_id, recipe_id)
            )
            deleted_rows = cursor.rowcount
            db.commit()
            cursor.close()
            if deleted_rows > 0:
                return jsonify({'status': 'ok'})
            else:
                return error_message('The recipe could not be deleted as favourite'), 500
        else:
            return error_message(), 400
    else:
        return error_message('Incorrect HTTP method'), 400