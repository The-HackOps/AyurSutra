# /ayursutra/run.py

from app import create_app

# Create the app instance using our factory
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
