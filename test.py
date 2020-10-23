from server import User
from event import Event, Seminar,Session, db
from EventSystem import Eventsystem
from ErrorMessage import ErrorMessage

class TestLogin(object):

    def test_successful_login(self):
        print("test_successful_login")
        user = Eventsystem.validate_login(6119988, 'pass6890')
        assert user is not None
        assert user.role == 'trainee'

    def test_invalid_username(self):

        print("test_invalid_username")
        try:
            Eventsystem.validate_login(6110000, 'pass6890')
        except ErrorMessage as error:
            assert error.msg == 'Please ensure the zid and password'

    def test_empty_username(self):
        print("test_empty_username")
        try:
            Eventsystem.validate_login('', 'pass')
        except ErrorMessage as error:
            assert error.msg == 'Please prvoide a valid zid'

    def test_empty_password(self):
        print('test_empty_password')
        try:
            Eventsystem.validate_login(6119988, '')
        except ErrorMessage as error:
            assert error.msg == 'Please prvoide a valid password'

    def test_guest_login(self):
        print('test_guest_login')

        user = Eventsystem.validate_login_guest('1479201404@qq.com', 'li1998')
        assert user is not None
        assert user.role == 'guest'

    def test_guest_validate_login(self):
        print('test_guest_validate_login')
        try:
            Eventsystem.validate_login_guest('147920104@qq.com','li199980812')
        except ErrorMessage as error:
            assert error.msg == 'Please ensure the username and password'

class TestRegister(object):

    def test_validate_username(self):
        print('test_validate_username')
        try:
            Eventsystem.make_register('1@1.com','li')
        except ErrorMessage as error:
            assert error.msg == 'Please enter correct email'

    def test_validate_email(self):
        print('test_validate_email')
        try:
            Eventsystem.make_register('11111111','li')
        except ErrorMessage as error:
            assert error.msg == 'Please enter email type as a username'


    def test_used_username(self):
        print('test_used_username')
        try:
            Eventsystem.make_register('147920104@qq.com','li1998')
        except ErrorMessage as error:
            assert error.msg == 'This is username have been used, change another one'


class TestCrateCourse(object):

    def test_validate_start(self):
        print('test_validate_start')
        try:
            Eventsystem.check_start('01-01-2018')
        except ErrorMessage as error:
            assert error.msg == 'Please enter start date before today'

    def test_start_end(self):
        print('test_start_end')
        assert Eventsystem.check_data('01-06-2018','01-09-2018') is True
        assert Eventsystem.validate_period('01-06-2018','01-09-2018', 10) is True

        try:
            Eventsystem.check_data('01-07-2018', '01-06-2018')
        except ErrorMessage as error:
            assert error.msg == 'Please ensure the start date is before the end date'

        try:
            Eventsystem.validate_period('01-06-2018','02-06-2018', 10)
        except ErrorMessage as error:
            assert error.msg=='Early period should between start and end'

        try:
            Eventsystem.validate_period('01-06-2018', '02-06-2018', -10)
        except ErrorMessage as error:
            assert error.msg == 'Early period should greater or equal zero'

    def test_validate_number(self):
        print('test_validate_number')
        assert Eventsystem.valida_seminar_capa(10) is True

        try:
            Eventsystem.valida_seminar_capa(-10)
        except ErrorMessage as error:
            assert error.msg == 'Capacity should greater than zero'


class Test_create_seminar(object):

    def test_validate_start(self):
        print('test_validate_start')
        try:
            Eventsystem.check_start('01-01-2018')
        except ErrorMessage as error:
            assert error.msg == 'Please enter start date before today'


    def test_start_end(self):
        print('test_start_end')
        assert Eventsystem.check_data('01-06-2018','01-09-2018') is True
        assert Eventsystem.validate_period('01-06-2018','01-09-2018', 10) is True

        try:
            Eventsystem.check_data('01-07-2018', '01-06-2018')
        except ErrorMessage as error:
            assert error.msg == 'Please ensure the start date is before the end date'

        try:
            Eventsystem.validate_period('01-06-2018','02-06-2018', 10)
        except ErrorMessage as error:
            assert error.msg=='Early period should between start and end'

        try:
            Eventsystem.validate_period('01-06-2018', '02-06-2018', -10)
        except ErrorMessage as error:
            assert error.msg == 'Early period should greater or equal zero'

    def test_validate_number(self):
        print('test_validate_number')
        assert Eventsystem.valida_seminar_capa(10) is True

        try:
            Eventsystem.valida_seminar_capa(-10)
        except ErrorMessage as error:
            assert error.msg == 'Capacity should greater than zero'


    def test_post_seminar(self):
        print('test_post_seminar')

        seminar = Eventsystem.make_seminar('hello','hehe','01-08-2018','01-09-2018',10,'OPEN','1479201404')
        assert seminar is not None
        assert seminar.title == 'hello'
        assert seminar.capacity == 10
        assert seminar.status == 'OPEN'
        assert seminar.creater == '1479201404'


class TestStudentRegisterSeminar(object):
    seminar = Seminar.query.filter_by(seminar_id = 2).one()
    assert seminar is not  None
    session = Session.query.filter_by(session_id = 3).one()
    assert session is not  None
    user = User.query.filter_by(user_id = 1).one()
    assert user is not None
    assert Eventsystem.Validate_Session_regist(user, session.sessions_all.all()) is True
    assert Eventsystem.speakerof_seesion(user,session) is True

    Eventsystem.cal_fee(session.start, user, session)
    assert user.fee == 0.0


class TestGuestRegisterSeminar(object):
    seminar = Seminar.query.filter_by(seminar_id=2).one()
    assert seminar is not None
    session = Session.query.filter_by(session_id=3).one()
    assert session is not None
    user = User.query.filter_by(user_id = 26).one()
    assert user is not None
    assert Eventsystem.Validate_Session_regist(user, session.sessions_all.all()) is True
    assert Eventsystem.speakerof_seesion(user, session) is True

    Eventsystem.cal_fee(session.start, user, session)
    assert user.fee == 50.0

    session = Session.query.filter_by(session_id=6).one()
    assert Eventsystem.Validate_Session_regist(user, session.sessions_all.all()) is True
    assert Eventsystem.speakerof_seesion(user, session) is True

    Eventsystem.cal_fee(session.start, user, session)
    assert user.fee == 1.0

