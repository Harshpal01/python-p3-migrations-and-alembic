import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student
# Setup an in-memory SQLite DB for testing
@pytest.fixture(scope="module")
def test_session():
    engine = create_engine('sqlite:///migrations_test.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_create_and_query_model(test_session):
    # Create a Student instance with valid fields
    student = Student(
        name="Test Name",
        email="test@example.com",
        grade=5
    )
    test_session.add(student)
    test_session.commit()

    # Query the student
    retrieved = test_session.query(Student).filter_by(email="test@example.com").first()

    assert retrieved is not None
    assert retrieved.name == "Test Name"
    assert retrieved.grade == 5

