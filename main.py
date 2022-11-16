from waitress import serve

from vehicle_location_service.app import create_app
from config import settings


if __name__ == "__main__":
    app = create_app()

    print(f"Serving on port {settings.SERVER_PORT}...")
    serve(app, listen=f"localhost:{settings.SERVER_PORT}")
