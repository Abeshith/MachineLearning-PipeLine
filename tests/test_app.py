import sys
import os
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import app

def test_app():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"Calorie Prediction App" in response.data