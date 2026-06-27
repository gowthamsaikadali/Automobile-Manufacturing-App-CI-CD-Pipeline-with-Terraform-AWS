from flask import Blueprint, jsonify
import datetime

health_bp = Blueprint("health", __name__)


@health_bp.route("/health")
def health_check():
    try:
        return jsonify({
            "status":    "healthy",
            "service":   "automobile-manufacturing-app",
            "version":   "2.0.0",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }), 200
    except Exception as e:
        return jsonify({
            "status":    "unhealthy",
            "error":     str(e),
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }), 500
