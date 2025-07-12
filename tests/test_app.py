import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def test_app():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"Calorie Prediction App" in response.data