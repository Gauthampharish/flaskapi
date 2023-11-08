# app.py
from flask import Flask, request, jsonify
from models import db, Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/comments', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    return jsonify([comment.text for comment in comments])

@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    text = data.get('text')
    comment = Comment(text=text)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment created successfully'})

# Add routes for updating and deleting comments as needed
@app.route('/comments/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    data = request.get_json()
    comment.text = data.get('text')
    db.session.commit()
    return jsonify({'message': 'Comment updated successfully'})

@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
