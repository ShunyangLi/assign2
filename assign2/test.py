from abc import ABC, abstractmethod
from server import User
from EventSystem import Eventsystem

class testLogin(ABC):

    @staticmethod
    def test_successful_login():
        print("test_successful_login")
        user = Eventsystem.validate_login(6119988, 'pass6890')
        assert user is not None
        assert user.role == 'trainee'

    @staticmethod
    def test_invalid_username():
        print("test_invalid_username")
        assert Eventsystem.validate_login(6110000, 'pass6890') is None

    @staticmethod
    def test_empty_username():
        print("test_empty_username")
        assert Eventsystem.validate_login('', 'pass') is None

    @staticmethod
    def test_invalid_password():
        print("test_invalid_password")
        assert  Eventsystem.validate_login(6119988, 'pass689') is None

    @staticmethod
    def test_empty_password():
        print('test_empty_password')
        assert Eventsystem.validate_login(6119988, '') is None

    @staticmethod
    def test_guest_login():
        print('test_guest_login')
        user = Eventsystem.validate_login('147920104@qq.com', 'li1998')
        assert user is not None
        assert user.role == 'guest'

    @staticmethod
    def test_guest_validate_login():
        print('test_guest_validate_login')
        assert Eventsystem.validate_login('147920104@qq.com','li199980812') is None

class testRegist(ABC):

    @staticmethod
    def success_register():
        print('success_register')
        guest = Eventsystem.make_register('12345@qq.com','hello')
        assert guest is not None
        assert guest.zid is None
        assert guest.role == 'guest'

    @staticmethod
    def test_register_username():
        print('test_register_username')
        assert Eventsystem.make_register('1479201404@qq.com','li1998') is None




