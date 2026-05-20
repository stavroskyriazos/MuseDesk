from flask import Blueprint, jsonify
from models import Ticket

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    total = Ticket.query.count()
    open_tickets = Ticket.query.filter_by(status="Open").count()

    return jsonify({
        "total_tickets": total,
        "open_tickets": open_tickets
    })