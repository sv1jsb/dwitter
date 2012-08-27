from auth.tests.auth_backends import (BackendTest,
    RowlevelBackendTest, AnonymousUserBackendTest, NoBackendsTest,
    InActiveUserBackendTest, NoInActiveUserBackendTest)
from auth.tests.basic import BasicTestCase
from auth.tests.context_processors import AuthContextProcessorTests
from auth.tests.decorators import LoginRequiredTestCase
from auth.tests.forms import (UserCreationFormTest,
    AuthenticationFormTest, SetPasswordFormTest, PasswordChangeFormTest,
    UserChangeFormTest, PasswordResetFormTest)
from auth.tests.remote_user import (RemoteUserTest,
    RemoteUserNoCreateTest, RemoteUserCustomTest)
from auth.tests.management import (
    GetDefaultUsernameTestCase,
    ChangepasswordManagementCommandTestCase,
)
from auth.tests.models import (ProfileTestCase, NaturalKeysTestCase,
    LoadDataWithoutNaturalKeysTestCase, LoadDataWithNaturalKeysTestCase,
    UserManagerTestCase)
from auth.tests.hashers import TestUtilsHashPass
from auth.tests.signals import SignalTestCase
from auth.tests.tokens import TokenGeneratorTest
from auth.tests.views import (AuthViewNamedURLTests,
    PasswordResetTest, ChangePasswordTest, LoginTest, LogoutTest,
    LoginURLSettings)

# The password for the fixture data users is 'password'
