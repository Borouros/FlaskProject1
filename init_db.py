import argparse
from app import app, db, User
from werkzeug.security import generate_password_hash

parser = argparse.ArgumentParser(description='Add a user to the database.')
parser.add_argument('--username', required=True, help='Username for the new user')
parser.add_argument('--password', required=True, help='Password for the new user')
parser.add_argument('--role', default='viewer', choices=['viewer', 'editor', 'admin'], help='Role of the new user')

args = parser.parse_args()

with app.app_context():
    if User.query.filter_by(username=args.username).first():
        print(f"User '{args.username}' already exists.")
    else:
        user = User(
            username=args.username,
            password=generate_password_hash(args.password),
            role=args.role
        )
        db.session.add(user)
        db.session.commit()
        print(f"Created user '{args.username}' with role '{args.role}'.")
