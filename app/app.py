from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
import pymysql
import os

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

def get_db_connection():
    try:
        return pymysql.connect(
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            database=os.environ.get('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
    except Exception as e:
        app.logger.error('Database connection failed')
        raise


# Health check endpoint
@app.route('/')
def index():
    return jsonify({'status': 'ok', 'message': 'API Biblioteca funcionando'})

# Error handler for all exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    app.logger.error(f"Error: {str(e)}")
    return jsonify({'error': 'Ocurrió un error interno'}), code

# ENDPOINTS CRUD PARA LIBROS
@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
    conn.close()
    return jsonify(books)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
        book = cursor.fetchone()
    conn.close()
    if book:
        return jsonify(book)
    else:
        return jsonify({'error': 'Book not found'}), 404

@app.route('/books', methods=['POST'])
def add_book():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    required = ['title', 'published_date', 'isbn', 'pages', 'category_id', 'author_id']
    if not all(k in data and data[k] for k in required):
        return jsonify({'error': 'Missing or empty fields'}), 400
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            'INSERT INTO books (title, published_date, isbn, pages, category_id, author_id) VALUES (%s, %s, %s, %s, %s, %s)',
            (data['title'], data['published_date'], data['isbn'], data['pages'], data['category_id'], data['author_id'])
        )
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': new_id}), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Book not found'}), 404
        fields = []
        values = []
        for key in ['title', 'published_date', 'isbn', 'pages', 'category_id', 'author_id']:
            if key in data:
                fields.append(f"{key} = %s")
                values.append(data[key])
        if not fields:
            conn.close()
            return jsonify({'error': 'No fields to update'}), 400
        values.append(book_id)
        cursor.execute(f'UPDATE books SET {", ".join(fields)} WHERE id = %s', tuple(values))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Book updated'})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Book not found'}), 404
        cursor.execute('DELETE FROM books WHERE id = %s', (book_id,))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Book deleted'})

# CRUD para MEMBERS
@app.route('/members', methods=['GET'])
def get_members():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM members')
        members = cursor.fetchall()
    conn.close()
    return jsonify(members)

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM members WHERE id = %s', (member_id,))
        member = cursor.fetchone()
    conn.close()
    if member:
        return jsonify(member)
    else:
        return jsonify({'error': 'Member not found'}), 404

@app.route('/members', methods=['POST'])
def add_member():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    if not all(k in data for k in ['name', 'email']):
        return jsonify({'error': 'Missing fields'}), 400
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO members (name, email) VALUES (%s, %s)', (data['name'], data['email']))
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': new_id}), 201

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM members WHERE id = %s', (member_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Member not found'}), 404
        fields = []
        values = []
        for key in ['name', 'email', 'join_date']:
            if key in data:
                fields.append(f"{key} = %s")
                values.append(data[key])
        if not fields:
            conn.close()
            return jsonify({'error': 'No fields to update'}), 400
        values.append(member_id)
        cursor.execute(f'UPDATE members SET {", ".join(fields)} WHERE id = %s', tuple(values))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Member updated'})

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM members WHERE id = %s', (member_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Member not found'}), 404
        cursor.execute('DELETE FROM members WHERE id = %s', (member_id,))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Member deleted'})

# CRUD para AUTHORS
@app.route('/authors', methods=['GET'])
def get_authors():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM authors')
        authors = cursor.fetchall()
    conn.close()
    return jsonify(authors)

@app.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM authors WHERE id = %s', (author_id,))
        author = cursor.fetchone()
    conn.close()
    if author:
        return jsonify(author)
    else:
        return jsonify({'error': 'Author not found'}), 404

@app.route('/authors', methods=['POST'])
def add_author():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    if not 'name' in data:
        return jsonify({'error': 'Missing name'}), 400
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO authors (name, biography) VALUES (%s, %s)', (data['name'], data.get('biography')))
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': new_id}), 201

@app.route('/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM authors WHERE id = %s', (author_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Author not found'}), 404
        fields = []
        values = []
        for key in ['name', 'biography']:
            if key in data:
                fields.append(f"{key} = %s")
                values.append(data[key])
        if not fields:
            conn.close()
            return jsonify({'error': 'No fields to update'}), 400
        values.append(author_id)
        cursor.execute(f'UPDATE authors SET {", ".join(fields)} WHERE id = %s', tuple(values))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Author updated'})

@app.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM authors WHERE id = %s', (author_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Author not found'}), 404
        cursor.execute('DELETE FROM authors WHERE id = %s', (author_id,))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Author deleted'})

# CRUD para CATEGORIES
@app.route('/categories', methods=['GET'])
def get_categories():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
    conn.close()
    return jsonify(categories)

@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM categories WHERE id = %s', (category_id,))
        category = cursor.fetchone()
    conn.close()
    if category:
        return jsonify(category)
    else:
        return jsonify({'error': 'Category not found'}), 404

@app.route('/categories', methods=['POST'])
def add_category():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    if not 'name' in data:
        return jsonify({'error': 'Missing name'}), 400
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO categories (name) VALUES (%s)', (data['name'],))
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': new_id}), 201

@app.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM categories WHERE id = %s', (category_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Category not found'}), 404
        if 'name' not in data:
            conn.close()
            return jsonify({'error': 'No fields to update'}), 400
        cursor.execute('UPDATE categories SET name = %s WHERE id = %s', (data['name'], category_id))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Category updated'})

@app.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM categories WHERE id = %s', (category_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Category not found'}), 404
        cursor.execute('DELETE FROM categories WHERE id = %s', (category_id,))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Category deleted'})

# CRUD para LOANS
@app.route('/loans', methods=['GET'])
def get_loans():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM loans')
        loans = cursor.fetchall()
    conn.close()
    return jsonify(loans)

@app.route('/loans/<int:loan_id>', methods=['GET'])
def get_loan(loan_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM loans WHERE id = %s', (loan_id,))
        loan = cursor.fetchone()
    conn.close()
    if loan:
        return jsonify(loan)
    else:
        return jsonify({'error': 'Loan not found'}), 404

@app.route('/loans', methods=['POST'])
def add_loan():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    required = ['book_id', 'member_id', 'loan_date', 'return_date']
    if not all(k in data for k in ['book_id', 'member_id']):
        return jsonify({'error': 'Missing fields'}), 400
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO loans (book_id, member_id, loan_date, return_date) VALUES (%s, %s, %s, %s)',
                       (data['book_id'], data['member_id'], data.get('loan_date'), data.get('return_date')))
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': new_id}), 201

@app.route('/loans/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    data = request.get_json()
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM loans WHERE id = %s', (loan_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Loan not found'}), 404
        fields = []
        values = []
        for key in ['book_id', 'member_id', 'loan_date', 'return_date']:
            if key in data:
                fields.append(f"{key} = %s")
                values.append(data[key])
        if not fields:
            conn.close()
            return jsonify({'error': 'No fields to update'}), 400
        values.append(loan_id)
        cursor.execute(f'UPDATE loans SET {", ".join(fields)} WHERE id = %s', tuple(values))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Loan updated'})

@app.route('/loans/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM loans WHERE id = %s', (loan_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Loan not found'}), 404
        cursor.execute('DELETE FROM loans WHERE id = %s', (loan_id,))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Loan deleted'})

# Aquí irán los endpoints CRUD para inventario

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

##Test
