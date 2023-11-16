from django.contrib.auth.models import User
from rest_framework import status
from model_bakery import baker
import pytest
 
from store.models import Collection

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection={'title': ''}):
        return api_client.post('/store/collections/', data=collection)

    return do_create_collection


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonumous_return_401(self, create_collection):
        response = create_collection({'title': 'test'})
        response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_return_403(self, authenticate, create_collection):
        authenticate()
        response = create_collection({'title': 'test'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400(self, authenticate, create_collection):
        authenticate(True)
        response = create_collection()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_201(self, authenticate, create_collection):
        authenticate(True)
        response = create_collection({'title': 'test'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_object_exist_return_200(self,authenticate,api_client):
        collection=baker.make(Collection)
        authenticate(True)

        response=api_client.get(f'/store/collections/{collection.id}/')

        assert response.status_code==status.HTTP_200_OK