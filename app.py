from flask import Flask
from database import Base, engine
from routes.post_routes import posts_bp

def create_app():
    app = Flask(__name__)

    from models.post_model import Post

    Base.metadata.create_all(engine)

    app.register_blueprint(posts_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)