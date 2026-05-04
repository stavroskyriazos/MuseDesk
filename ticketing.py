from flask import Blueprint, request, jsonify
from models import db, Ticket

ticket = Blueprint('ticket', __name__)

@ticket.route('/api/tickets', methods=['POST'])
def create_ticket():
    data = request.json
    new_ticket = Ticket(
        title=data['title'],
        description=data['description'],
        user_id=data['user_id']
    )
    db.session.add(new_ticket)
    db.session.commit()
    return jsonify({"message": "Ticket created"})

@ticket.route('/api/tickets', methods=['GET'])
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status
        } for t in tickets
    ])