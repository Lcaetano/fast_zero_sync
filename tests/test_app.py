from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_e_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'teste@teste.br',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'username': 'testusername',
        'email': 'teste@teste.br',
        'id': 1,
    }


def test_create_user_invalido(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Test',
            'email': 'teste@test.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_invalido_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Test1',
            'email': 'teste@test.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get(
        '/users/'
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get(
        '/users/',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_um(client, user):
    response = client.get('/users/1')
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.json() == user_schema


def test_read_user_um_retorno_not_found(client):
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'testusername2',
            'email': 'teste@teste.br',
            'password': 'password',
        },
    )

    assert response.json() == {
        'username': 'testusername2',
        'email': 'teste@teste.br',
        'id': 1,
    }


def test_update_user_retorno_not_found(client, token):
    response = client.put(
        '/users/2',
        json={
            'username': 'testusername2',
            'email': 'teste@teste.br',
            'password': 'password',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.json() == {'message': 'User deleted!'}


def test_delete_user_retorno_not_found(client, token):
    response = client.delete(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not enough permissions'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
