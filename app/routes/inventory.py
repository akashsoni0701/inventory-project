from flask import Blueprint, request, jsonify
from app import logger
from app.services.csv_service import process_csv

bp = Blueprint('inventory', __name__)


@bp.route('/upload', methods=['POST'])
def upload_file():
    """
        Upload CSV file to populate data in the Inventory or Member table.
        ---
        tags:
          - Upload
        consumes:
          - multipart/form-data
        parameters:
          - name: file
            in: formData
            type: file
            required: true
            description: The CSV file to upload.
        responses:
          200:
            description: Data uploaded successfully.
          400:
            description: Invalid file or format.
          500:
            description: Internal server error.
    """
    if 'file' not in request.files:
        logger.warning("No file uploaded.")
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        logger.warning("No selected file.")
        return jsonify({'error': 'No selected file'}), 400

    logger.info(f"Processing uploaded file: {file.filename}")
    result, status_code = process_csv(file)
    return jsonify(result), status_code
