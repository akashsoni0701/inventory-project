from app import create_app, logger

def main() -> None:
    """
    Entry point for the Flask application.
    """
    logger.info("Starting Flask application.")
    app.run(debug=True)

app = create_app()

if __name__ == '__main__':
    main()

## app/__init__.py (Initialize