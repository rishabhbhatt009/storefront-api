from rest_framework import status
from rest_framework.test import APIClient
import pytest
from django.contrib.auth.models import User

#################################################################################
# PYTEST
# - pytest <store/test/test_collections.pu::TestCreateCollection::func_name>
# - pytest -k <pattern>
# - -p no:warnings 
# 
# - test for behavior not implementation 
# - test should have single responsibility
# 
# - Naming convention : 
#   - the name of the test class/function should be descriptive 
#   - should be prefixed with test
# 
# - AAA : Arrange -> Act -> Assert 
#   - Arrange   : Setup the systems initial state for test 
#   - Act       : Execute the behavior we want to test 
#   - Assert    : We check
# 
# - Continuous testing using pytest-watch 
# - ptw
#################################################################################

@pytest.mark.django_db
class TestCreateCollection:
    
    # skip test 
    # @pytest.mark.skip
    def test_if_user_is_anonymous_return_401(self):
        # Arrange 
        client = APIClient()
        # Act 
        response = client.post(path='/store/collections/',
                            data={'title':'Testing'}
                            )   
        # Assert 
        assert response.status_code == status.HTTP_401_UNAUTHORIZED    
    
    def test_if_user_is_not_admin_return_403(self):
        # Arrange 
        client = APIClient()
        client.force_authenticate(user={})
        # Act 
        response = client.post(path='/store/collections/',
                            data={'title':'Testing'}
                            )   
        # Assert 
        assert response.status_code == status.HTTP_403_FORBIDDEN    
        
    def test_if_data_is_invalid_return_403(self):
        # Arrange 
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        # Act 
        response = client.post(path='/store/collections/',
                            data={'title':''}
                            )   
        # Multiple-Assert 
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None   
        
    def test_if_data_is_valid_return_201(self):
        # Arrange 
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True))
        # Act 
        response = client.post(path='/store/collections/',
                            data={'title':'Test'}
                            )   
        # Multiple-Assert 
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0