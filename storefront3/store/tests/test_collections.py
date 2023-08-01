from rest_framework import status
import pytest

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
# 
# - Fixtures :
#   - remove redundant code 
#################################################################################

#################################################################################
#  Fixtures specific to this test module
#################################################################################

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post(path='/store/collections/', data= collection)
    return do_create_collection

#################################################################################

@pytest.mark.django_db
class TestCreateCollection:
    
    # skip test 
    # @pytest.mark.skip
    def test_if_user_is_anonymous_return_401(self, create_collection):
        response = create_collection({'title':'Testing'})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED    
    
    #-------------------------------------------------------------------------------------
    # 
    # Understanding control flow : 
    # 
    # 1. test_if_user_is_not_admin_return_403() is called
    #   - receives the do_authenticate function as the value of the authenticate fixture
    #   - receives the do_create_collection function  
    # 
    # 2. authenticate() : calls force_authenticate using the api_client object
    #    Note : Since the do_authenticate function was created within the authenticate 
    #    fixture, it has access to the api_client object defined in the same scope
    # 
    # 3. create_collection() : calls post using the same api_client object (created by 
    #    the api_client fixture) as an argument 
    # 
    #-------------------------------------------------------------------------------------
    
    def test_if_user_is_not_admin_return_403(self, authenticate, create_collection):
        authenticate()
        
        # create_collection fixture, which also receives the api_client object (created by the api_client fixture) as an argument
        response = create_collection({'title':'Testing'})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN    
    
    def test_if_data_is_invalid_return_403(self, authenticate, create_collection):
        authenticate(is_staff=True)
        
        response = create_collection({'title':''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None   
        
    def test_if_data_is_valid_return_201(self, authenticate, create_collection):
        authenticate(is_staff=True)
        
        response = create_collection({'title':'Testing'})
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0