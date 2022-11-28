"""
Integration test: GET and POST methods
"""
#  pylint: disable=unused-argument
#  noqa:E501


def test_homepage_get(test_client):
    """
    GIVEN a Flask from the main src-code
    WHEN the '/' page is requested with the GET request
    THEN check that the response is correct
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"QuickRead - A text summarizer with Pegasus NLP model\n" in response.data


def test_homepage_post_1(test_client):
    """
    GIVEN a Flask from the main src-code
    WHEN the '/' page is requested with the POST request with invalid payload
    THEN check that the response has the right code and response data has right warning
    """
    payload = {
        'content': """blablabla"""
    }
    response = test_client.post('/', data=payload)
    assert response.status_code == 200
    assert b"Input Error: \
                Make sure that input is English or has max length of 1000" \
        in response.data


def test_homepage_post_2(test_client):
    """
    GIVEN a Flask from the main src-code
    WHEN the '/' page is requested with the POST request with invalid payload
    THEN check that the response has the right code and response data has right warning
    """
    payload = {
        'content': ""
    }
    response = test_client.post('/', data=payload)
    print(response)
    assert response.status_code == 200
    assert b"Input Error: \
                Make sure that input is English or has max length of 1000" \
        in response.data


def test_homepage_post_3(test_client, init_database):
    """
    GIVEN a Flask from the main src-code
    WHEN the '/' page is requested with the POST request with valid payload
    THEN check that the response has the right code and response data has right response
    """
    payload = {
        'content': """
        I need to be very clear that having a set of tests that covers 100% of the source code is by no means an indicator that the code is properly tested.

This metric means that there are a lot of tests and a lot of effort has been put into developing the tests. The quality of the tests still needs to be checked by code inspection.

That said, the other extreme, where this is a minimal set (or none!) of tests, is much worse!

        """
    }
    response = test_client.post('/', data=payload)
    print(response)
    assert response.status_code == 200
    assert b"QuickRead - A text summarizer with Pegasus NLP model\n" in response.data
    assert b"Make sure that input is English or has max character count of 1000\n" \
        not in response.data


def test_homepage_post_4(test_client, init_database):
    """
    GIVEN a Flask from the main src-code
    WHEN the '/unlabeled_data' page is requested with the POST request without
    THEN check that the response is error
    """
    response = test_client.post('/unlabeled_data')
    print(response)
    assert response.status_code != 200
    assert response.status_code == 405
