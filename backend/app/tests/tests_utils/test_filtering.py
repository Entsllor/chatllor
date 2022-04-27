import pytest
import sqlalchemy
from pydantic import BaseModel
from sqlalchemy.orm import Query

from app.models import User
from app.utils.filtering import handle_filter_param, filter_by_model, Filter, add_filter


class FakeUser(BaseModel):
    id: int
    username: str


class FakeRequest:
    def __init__(self, **kwargs):
        self.query_params = kwargs


def test_handle_filter_params():
    fields = FakeUser.__fields__
    assert handle_filter_param(fields["username"], "like:you") == ("like", "you")
    assert handle_filter_param(fields["username"], "you") == ("eq", "you")
    assert handle_filter_param(fields["username"], "ne:you") == ("ne", "you")
    assert handle_filter_param(fields["username"], "gt:you") == ("gt", "you")
    assert handle_filter_param(fields["username"], "lt:you") == ("lt", "you")
    assert handle_filter_param(fields["username"], "ge:you") == ("ge", "you")
    assert handle_filter_param(fields["username"], "le:you") == ("le", "you")
    assert handle_filter_param(fields["id"], "10") == ("eq", "10")
    assert handle_filter_param(fields["id"], "ne:10") == ("ne", "10")
    assert handle_filter_param(fields["id"], "gt:10") == ("gt", "10")
    assert handle_filter_param(fields["id"], "lt:10") == ("lt", "10")
    assert handle_filter_param(fields["id"], "ge:10") == ("ge", "10")
    assert handle_filter_param(fields["id"], "le:10") == ("le", "10")


def test_failed_filter_params_wrong_operators():
    fields = FakeUser.__fields__
    with pytest.raises(ValueError):
        assert handle_filter_param(fields["username"], "as:you")
    with pytest.raises(ValueError):
        assert handle_filter_param(fields["id"], "sm:10")
    with pytest.raises(ValueError):
        assert handle_filter_param(fields["id"], ":10")
    with pytest.raises(ValueError):
        assert handle_filter_param(fields["id"], "*:10")


def test_filter_by_model():
    filter_handler = filter_by_model(FakeUser)
    assert filter_handler(FakeRequest(id="gt:10")) == [Filter("id", "gt", "10")]
    assert filter_handler(FakeRequest(id="sm:10")) == []
    assert filter_handler(FakeRequest(username="like:you")) == [Filter("username", "like", "you")]
    assert filter_handler(FakeRequest(username="like:you", id="ne:10")) \
           == [Filter("username", "like", "you"), Filter("id", "ne", "10")]
    assert filter_handler(FakeRequest(error="ne:you", id="ne:10")) == [Filter("id", "ne", "10")]


def test_query_str_is_a_sql_code():
    query_str = str(sqlalchemy.select(User).where(User.username == "Knight")).lower()
    assert 'select' in query_str
    assert 'from' in query_str
    assert 'where' in query_str
    assert 'username' in query_str


def is_queries_equal(query_1: Query, query_2: Query) -> bool:
    return str(query_1) == str(query_2) and query_1.compile().params == query_2.compile().params


def test_comparing_queries():
    q: Query = sqlalchemy.select(User)
    assert is_queries_equal(q.where(User.id == 1), add_filter(q, Filter("id", "eq", "1")))
    assert not is_queries_equal(q.where(User.id > 1), add_filter(q, Filter("id", "eq", "1")))
    assert not is_queries_equal(q.where(User.id == 2), add_filter(q, Filter("id", "eq", "1")))
    assert not is_queries_equal(q.where(User.email == 2), add_filter(q, Filter("id", "eq", "1")))
    assert not is_queries_equal(q, add_filter(q, Filter("id", "eq", "1")))


def test_filter_by_condition_with_int_value():
    q: Query = sqlalchemy.select(User)
    assert is_queries_equal(q.where(User.id == 1), add_filter(q, Filter("id", "eq", "1")))
    assert is_queries_equal(q.where(User.id != 1), add_filter(q, Filter("id", "ne", "1")))
    assert is_queries_equal(q.where(User.id > 1), add_filter(q, Filter("id", "gt", "1")))
    assert is_queries_equal(q.where(User.id >= 1), add_filter(q, Filter("id", "ge", "1")))
    assert is_queries_equal(q.where(User.id < 1), add_filter(q, Filter("id", "lt", "1")))
    assert is_queries_equal(q.where(User.id <= 1), add_filter(q, Filter("id", "le", "1")))


def test_filter_by_condition_with_str_value():
    q: Query = sqlalchemy.select(User)
    name_field = User.username
    assert is_queries_equal(q.where(name_field == "me"), add_filter(q, Filter("username", "eq", "me")))
    assert is_queries_equal(q.where(name_field != "me"), add_filter(q, Filter("username", "ne", "me")))
    assert is_queries_equal(q.where(name_field > "me"), add_filter(q, Filter("username", "gt", "me")))
    assert is_queries_equal(q.where(name_field >= "me"), add_filter(q, Filter("username", "ge", "me")))
    assert is_queries_equal(q.where(name_field < "me"), add_filter(q, Filter("username", "lt", "me")))
    assert is_queries_equal(q.where(name_field <= "me"), add_filter(q, Filter("username", "le", "me")))
    assert is_queries_equal(q.where(name_field.like("you")), add_filter(q, Filter("username", "like", "you")))
    assert is_queries_equal(q.where(name_field.like("%you")), add_filter(q, Filter("username", "like", "%you")))
    assert is_queries_equal(q.where(name_field.like("%you%")), add_filter(q, Filter("username", "like", "%you%")))
    assert is_queries_equal(q.where(name_field.like("%y_u%")), add_filter(q, Filter("username", "like", "%y_u%")))
    assert is_queries_equal(q.where(name_field.like("%y%u%")), add_filter(q, Filter("username", "like", "%y%u%")))
