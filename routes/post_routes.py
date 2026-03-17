from flask import Blueprint, request, jsonify
from database import Session
from models.post_model import Post

posts_bp = Blueprint('posts', __name__)

def format_post(post):
    return{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'category': post.category,
        'tags': post.tags,
        'created_at': post.created_at,
        'updated_at': post.updated_at
    }

@posts_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    title = data.get('title')
    content = data.get('content')
    category = data.get('category')
    tags = data.get('tags', [])

    if not data:
        return jsonify({'error': "No data provided!"}), 400

    if not title or not content or not category:
        return jsonify({'error': 'Title, content, and category are required'}), 400
    
    try:
        session = Session()

        new_post = Post(
            title=title,
            content=content,
            category=category,
            tags=tags
        )

        session.add(new_post)
        session.commit()
        session.refresh(new_post)

        return jsonify(format_post(new_post)), 201
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()


@posts_bp.route('/posts', methods=['GET'])
def get_posts():

    try:
        session = Session()
        search_term = request.args.get('term')

        if search_term:
            posts = session.query(Post).filter(
                Post.title.like(f'%{search_term}%') |
                Post.content.like(f'%{search_term}%') | 
                Post.category.like(f'%{search_term}%')
            ).all()
        else:
            posts = session.query(Post).all()

        return jsonify([format_post(post) for post in posts]), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()

@posts_bp.route('/posts/<int:id>', methods=['GET'])
def get_single_post(id):
    try:
        session = Session()
        post = session.query(Post).filter(Post.id==id).first()

        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        return jsonify(format_post(post)), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()

@posts_bp.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    try:
        session = Session()
        post = session.query(Post).filter(Post.id==id).first()

        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        session.delete(post)
        session.commit()

        return jsonify({'message': 'Pot deleted successfully'}), 204
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        session.close()

@posts_bp.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):

    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data proveded'}), 400
    
    title = data.get('title')
    content = data.get('content')
    category = data.get('category')
    tags = data.get('tags', [])

    if not title or not content or not category:
        return jsonify({'error': 'Title, content, and category are required'}), 400
    
    try:

        session = Session()

        post = session.query(Post).filter(Post.id == id).first()

        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        post.title = title
        post.content = content
        post.category = category
        post.tags = tags

        session.commit()
        session.refresh(post)

        return jsonify(format_post(post)), 200
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()