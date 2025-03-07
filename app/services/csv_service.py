import pandas as pd
from io import StringIO
from app import db, logger
from app.models import Inventory, Member
from datetime import datetime


def identify_table(columns):
    """Identify the table based on CSV column names."""
    inventory_columns = {'title', 'description', 'remaining_count', 'expiration_date'}
    member_columns = {'name', 'surname', 'booking_count', 'date_joined'}

    if inventory_columns.issubset(columns):
        return 'inventory'
    elif member_columns.issubset(columns):
        return 'member'
    else:
        return None


def parse_date(date_str):
    """Parse a date string into a datetime object."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        logger.error(f"Invalid date format: {date_str}")
        return None


def process_csv(file):
    """
        Process the uploaded CSV file and insert data into the appropriate table.

        Args:
            file: Uploaded CSV file.

        Returns:
            Tuple: JSON response and status code.
    """
    try:
        logger.info(f"Processing uploaded CSV file")
        if not file.filename.endswith('.csv'):
            logger.error("Uploaded file is not a CSV.")
            return {'error': 'Uploaded file is not a CSV'}, 400

        file.stream.seek(0)
        df = pd.read_csv(StringIO(file.stream.read().decode("utf-8")))
        table_name = identify_table(set(df.columns))

        if not table_name:
            logger.error("CSV file structure does not match any known table.")
            return {'error': 'Invalid CSV file structure'}, 400

        if table_name == 'inventory':
            for _, row in df.iterrows():
                expiration_date = parse_date(row['expiration_date'])
                if not expiration_date:
                    continue

                item = Inventory.query.filter_by(title=row['title']).first()
                if not item:
                    new_item = Inventory(
                        title=row['title'],
                        description=row['description'],
                        remaining_count=row['remaining_count'],
                        expiration_date=expiration_date
                    )
                    db.session.add(new_item)

        elif table_name == 'member':
            for _, row in df.iterrows():
                date_joined = parse_date(row['date_joined']) if 'date_joined' in row and pd.notna(
                    row['date_joined']) else datetime.utcnow()

                member = Member.query.filter_by(name=row['name'], surname=row['surname']).first()
                if not member:
                    new_member = Member(
                        name=row['name'],
                        surname=row['surname'],
                        booking_count=row.get('booking_count', 0),
                        date_joined=date_joined
                    )
                    db.session.add(new_member)

        db.session.commit()
        logger.info("CSV file processed successfully.")
        return {'message': 'CSV file processed successfully'}, 200
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        return {'error': 'Error processing CSV'}, 500