import os, sys, pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DATABASE_URL", "sqlite:///test.db")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("FLASK_ENV", "testing")


@pytest.fixture
def app():
    from app import create_app
    flask_app = create_app()
    flask_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    yield flask_app
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture
def client(app):
    return app.test_client()


class TestHealth:
    def test_health_200(self, client):
        r = client.get("/health")
        assert r.status_code == 200

    def test_health_json(self, client):
        r = client.get("/health")
        assert r.get_json()["status"] == "healthy"


class TestAuth:
    def test_login_page_loads(self, client):
        assert client.get("/auth/login").status_code == 200

    def test_bad_login(self, client):
        r = client.post("/auth/login", data={"username": "nobody", "password": "wrong"})
        assert r.status_code == 200  # re-renders form


class TestInventory:
    def test_inventory_redirects_when_not_logged_in(self, client):
        r = client.get("/inventory")
        assert r.status_code in [302, 308]


class TestProduction:
    def test_production_redirects_when_not_logged_in(self, client):
        r = client.get("/production")
        assert r.status_code in [302, 308]


class TestDatabase:
    def test_tables_create(self, app):
        with app.app_context():
            from extensions import db
            db.create_all()
