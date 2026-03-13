from flask import Flask, request, jsonify
import os, json
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    return connection
    
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided!"}), 400
    
    title = data.get('title')
    content = data.get('content')
    category = data.get('category')
    tags = data.get('tags', [])

    if not title or not content or not category:
        return jsonify({"error": "Title, content, and cateogry values are required."}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            INSERT INTO posts (title, content, category, tags) VALUES (%s, %s, %s, %s)
        """, (title, content, category, json.dumps(tags)))

        conn.commit()

        cursor.execute("SELECT * FROM posts WHERE id = %s", (cursor.lastrowid,))
        new_post = cursor.fetchone()
        new_post['tags'] = json.loads(new_post['tags'])

        cursor.close()
        conn.close()

        return jsonify(new_post), 201
    
    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    
@app.route('/posts', methods=['GET'])
def get_posts():

    search_term = request.args.get('term')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if search_term:
            cursor.execute("""
                SELECT * FROM posts WHERE title LIKE %s OR content LIKE %s OR category LIKE %s    
            """,(f'%{search_term}%', f'%{search_term}%',f'%{search_term}%'))

        else:
            cursor.execute("SELECT * FROM posts")

        posts = cursor.fetchall()

        for post in posts:
            if post['tags']:
                post['tags'] = json.loads(post['tags'])

        cursor.close()
        conn.close()

        return jsonify(posts), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/posts/<int:id>', methods=['GET'])
def get_single_post(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
        post = cursor.fetchone()

        cursor.close()
        conn.close()

        if not post:
            return jsonify({"error": "Post not found."}), 404
        
        return jsonify(post), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
        post = cursor.fetchone()

        if not post:
            return jsonify({"error": "Post not found."}), 404
        

        cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()

        return '', 204
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided."}), 400
    
    title = data.get('title')
    content = data.get('content')
    category = data.get('category')
    tags = data.get('tags', [])

    if not title or not content or not category:
        return jsonify({"error": "Title, content, and cateogry values are required."}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
        post = cursor.fetchone()

        if not post:
            return jsonify({"error": "Post not found."}), 404
        
        cursor.execute("""
            UPDATE posts SET title = %s, content = %s, category = %s, tags = %s WHERE id = %s
                       """, (title, content, category, json.dumps(tags), id))
        
        conn.commit()

        cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
        updated_post = cursor.fetchone()
        updated_post['tags'] = json.loads(updated_post['tags'])

        cursor.close()
        conn.close()

        return jsonify(updated_post), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@app.route('/home')
def home():
    pass

if __name__ == "__main__":
    app.run(debug=True)