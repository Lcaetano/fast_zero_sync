from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='luis',
        email='luis@mail.br',
        password='minha_senha-legal',
    )

    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.email == 'luis@mail.br'))

    assert result.username == 'luis'
