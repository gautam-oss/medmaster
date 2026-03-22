"""
Smoke tests — MedMaster
Covers all 5 Django apps: core, users, appointments, chatbot, insurance.
Runs in CI on every push to main. Uses SQLite (local settings).
No external services (Gemini, Postgres) are needed.
"""
import json
import pytest
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    return Client()


@pytest.fixture
def patient_user(db):
    """Registered patient with a linked Patient profile."""
    user = User.objects.create_user(
        username='testpatient',
        password='testpass123',
        user_type='patient',
        first_name='Test',
        last_name='Patient',
        email='patient@test.com',
    )
    from users.models import Patient
    Patient.objects.create(user=user)
    return user


@pytest.fixture
def doctor_user(db):
    """Registered doctor with a linked Doctor profile."""
    user = User.objects.create_user(
        username='testdoctor',
        password='testpass123',
        user_type='doctor',
        first_name='Test',
        last_name='Doctor',
        email='doctor@test.com',
    )
    from users.models import Doctor
    Doctor.objects.create(
        user=user,
        specialization='General Medicine',
        license_number='LIC-TEST-001',
        experience_years=5,
        consultation_fee=500.00,
    )
    return user


@pytest.fixture
def patient_client(client, patient_user):
    """Logged-in patient client."""
    client.login(username='testpatient', password='testpass123')
    return client


@pytest.fixture
def doctor_client(client, doctor_user):
    """Logged-in doctor client."""
    client.login(username='testdoctor', password='testpass123')
    return client


# ── core app ──────────────────────────────────────────────────────────────────

class TestCoreApp:
    def test_home_page_loads(self, client):
        r = client.get('/')
        assert r.status_code == 200

    def test_home_contains_brand_name(self, client):
        r = client.get('/')
        assert b'MedMaster' in r.content

    def test_home_shows_register_link_when_logged_out(self, client):
        r = client.get('/')
        assert b'register' in r.content.lower()


# ── users app ─────────────────────────────────────────────────────────────────

class TestUsersApp:
    def test_login_page_loads(self, client):
        r = client.get('/users/login/')
        assert r.status_code == 200

    def test_register_patient_page_loads(self, client):
        r = client.get('/users/register/patient/')
        assert r.status_code == 200

    def test_register_doctor_page_loads(self, client):
        r = client.get('/users/register/doctor/')
        assert r.status_code == 200

    def test_dashboard_redirects_anonymous(self, client):
        r = client.get('/users/dashboard/')
        assert r.status_code == 302
        assert '/login' in r['Location']

    def test_dashboard_loads_for_patient(self, patient_client):
        r = patient_client.get('/users/dashboard/')
        assert r.status_code == 200

    def test_dashboard_loads_for_doctor(self, doctor_client):
        r = doctor_client.get('/users/dashboard/')
        assert r.status_code == 200

    def test_dashboard_shows_patient_name(self, patient_client):
        r = patient_client.get('/users/dashboard/')
        assert b'Test' in r.content

    def test_dashboard_shows_doctor_specialization(self, doctor_client):
        r = doctor_client.get('/users/dashboard/')
        assert b'General Medicine' in r.content


# ── appointments app ──────────────────────────────────────────────────────────

class TestAppointmentsApp:
    def test_book_redirects_anonymous(self, client):
        r = client.get('/appointments/book/')
        assert r.status_code == 302

    def test_my_appointments_redirects_anonymous(self, client):
        r = client.get('/appointments/my/')
        assert r.status_code == 302

    def test_book_page_loads_for_patient(self, patient_client):
        r = patient_client.get('/appointments/book/')
        assert r.status_code == 200

    def test_my_appointments_loads_for_patient(self, patient_client):
        r = patient_client.get('/appointments/my/')
        assert r.status_code == 200

    def test_my_appointments_loads_for_doctor(self, doctor_client):
        r = doctor_client.get('/appointments/my/')
        assert r.status_code == 200

    def test_doctor_cannot_book_appointment(self, doctor_client):
        """Doctors should be redirected away from the booking page."""
        r = doctor_client.get('/appointments/book/')
        # Either redirect or error — not allowed to book
        assert r.status_code in (302, 403)


# ── chatbot app ───────────────────────────────────────────────────────────────

class TestChatbotApp:
    def test_chat_page_loads_as_guest(self, client):
        r = client.get('/chatbot/')
        assert r.status_code == 200

    def test_chat_page_loads_when_logged_in(self, patient_client):
        r = patient_client.get('/chatbot/')
        assert r.status_code == 200

    def test_send_message_rejects_get(self, client):
        r = client.get('/chatbot/send/')
        assert r.status_code == 405

    def test_send_message_rejects_empty_message(self, client):
        r = client.post(
            '/chatbot/send/',
            data=json.dumps({'message': ''}),
            content_type='application/json',
        )
        assert r.status_code == 400

    def test_send_message_rejects_too_long(self, client):
        r = client.post(
            '/chatbot/send/',
            data=json.dumps({'message': 'x' * 1001}),
            content_type='application/json',
        )
        assert r.status_code == 400

    def test_send_message_rejects_invalid_json(self, client):
        r = client.post(
            '/chatbot/send/',
            data='not-json',
            content_type='application/json',
        )
        assert r.status_code == 400


# ── insurance app ─────────────────────────────────────────────────────────────

class TestInsuranceApp:
    def test_predict_page_loads_as_guest(self, client):
        r = client.get('/insurance/predict/')
        assert r.status_code == 200

    def test_predict_page_loads_when_logged_in(self, patient_client):
        r = patient_client.get('/insurance/predict/')
        assert r.status_code == 200

    def test_about_page_loads(self, client):
        r = client.get('/insurance/about/')
        assert r.status_code == 200

    def test_history_redirects_anonymous(self, client):
        r = client.get('/insurance/history/')
        assert r.status_code == 302

    def test_history_loads_for_patient(self, patient_client):
        r = patient_client.get('/insurance/history/')
        assert r.status_code == 200

    def test_guest_result_redirects_without_session(self, client):
        r = client.get('/insurance/guest-result/')
        assert r.status_code == 302


# ── ML model unit tests ───────────────────────────────────────────────────────

class TestInsuranceMLModel:
    def test_prediction_returns_positive_value(self):
        from insurance.ml_model import predictor
        result = predictor.predict(30, 'male', 25.0, 0, 'no', 'northeast')
        assert result > 0

    def test_smoker_costs_significantly_more(self):
        from insurance.ml_model import predictor
        smoker    = predictor.predict(30, 'male', 25.0, 0, 'yes', 'northeast')
        nonsmoker = predictor.predict(30, 'male', 25.0, 0, 'no',  'northeast')
        assert smoker > nonsmoker * 2   # smoking should at least double cost

    def test_older_person_costs_more(self):
        from insurance.ml_model import predictor
        young = predictor.predict(25, 'male', 25.0, 0, 'no', 'northeast')
        old   = predictor.predict(60, 'male', 25.0, 0, 'no', 'northeast')
        assert old > young

    def test_higher_bmi_costs_more(self):
        from insurance.ml_model import predictor
        normal = predictor.predict(30, 'male', 22.0, 0, 'no', 'northeast')
        obese  = predictor.predict(30, 'male', 40.0, 0, 'no', 'northeast')
        assert obese > normal

    def test_feature_importance_returns_dict(self):
        from insurance.ml_model import predictor
        importance = predictor.get_feature_importance()
        assert isinstance(importance, dict)
        assert 'Smoking Status' in importance

    def test_all_regions_work(self):
        from insurance.ml_model import predictor
        for region in ['northeast', 'northwest', 'southeast', 'southwest']:
            result = predictor.predict(30, 'female', 25.0, 1, 'no', region)
            assert result > 0, f"Failed for region: {region}"