# /ayursutra/run.py

from app import create_app

# Create the app instance using our factory
app = create_app()

if __name__ == '__main__':
    # Run the app on a different port, like 5001
    app.run(debug=True, port=5001)