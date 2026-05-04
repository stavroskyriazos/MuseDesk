from flask import Blueprint, jsonify, request

from .models import Ticket, User, db


ticket = Blueprint("ticket", __name__)
VALID_STATUSES = {"Open", "In Progress", "Closed"}


@ticket.route("/api/tickets", methods=["POST"])
def create_ticket():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()
    user_id = data.get("user_id")

    if not title or not description or not user_id:
        return jsonify({"message": "Title, description, and user_id are required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    new_ticket = Ticket(title=title, description=description, user_id=user.id)
    db.session.add(new_ticket)
    db.session.commit()

    return jsonify({"message": "Ticket created", "ticket": new_ticket.to_dict()}), 201


@ticket.route("/api/tickets", methods=["GET"])
def get_tickets():
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tickets])


@ticket.route("/api/tickets/<int:ticket_id>", methods=["PATCH"])
def update_ticket(ticket_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")

    if status not in VALID_STATUSES:
        return jsonify({"message": "Status must be Open, In Progress, or Closed"}), 400

    existing_ticket = Ticket.query.get_or_404(ticket_id)
    existing_ticket.status = status
    db.session.commit()

    return jsonify({"message": "Ticket updated", "ticket": existing_ticket.to_dict()})
