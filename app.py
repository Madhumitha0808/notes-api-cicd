from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for notes (a simple Python dictionary)
# Key: note id (int or str), Value: note text (str)
notes = {}
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to my Automated Notes API!"}), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint to verify the service is alive."""
    return jsonify({"status": "ok"}), 200


@app.route("/notes", methods=["GET"])
def get_notes():
    """Returns a list of all notes."""
    # Convert dictionary into a list of objects: [{"id": 1, "text": "..."}, ...]
    notes_list = [{"id": note_id, "text": text} for note_id, text in notes.items()]
    return jsonify(notes_list), 200


@app.route("/notes", methods=["POST"])
def create_note():
    """Adds a new note. Expects JSON: {"id": 1, "text": "My note"}"""
    data = request.get_json()

    if not data or "id" not in data or "text" not in data:
        return jsonify({"error": "Both 'id' and 'text' are required"}), 400

    note_id = data["id"]
    notes[note_id] = data["text"]

    return jsonify({"message": "Note created", "note": {"id": note_id, "text": data["text"]}}), 201


@app.route("/notes/<note_id>", methods=["DELETE"])
def delete_note(note_id):
    """Deletes a note by its ID, or returns 404 if not found."""
    # Note: URL params are strings. We check string matching or cast if needed.
    # Try direct lookup, or integer lookup if keys are integers:
    target_key = None
    for key in notes.keys():
        if str(key) == str(note_id):
            target_key = key
            break

    if target_key is None:
        return jsonify({"error": "Note not found"}), 404

    del notes[target_key]
    return jsonify({"message": f"Note {note_id} deleted"}), 200


if __name__ == "__main__":
    # Run locally on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)