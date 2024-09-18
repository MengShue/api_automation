import re
import pytest
from requests.exceptions import HTTPError

from .base_test import BaseTest


class TestURLhausAPI(BaseTest):

    def test_get_recent_urls(self):
        """
        GET v1/urls/recent/limit/{X}: Get latest X number of URL data
        """
        response = self.client.get_recent_urls(limit=3)

        assert response.status_code == 200, "'status_code' should be 200"
        assert response.json()["query_status"] == 'ok', "key 'query_status' should be ok"
        assert "urls" in response.json(), "lack 'urls' key in response"
        assert isinstance(response.json()["urls"], list), "'urls' should be list"
        assert len(response.json()["urls"]) <= 3, f"expected most 3 number of data，actual get {len(response.json()['urls'])} number"
        assert isinstance(response.json()["urls"][0]["tags"], list), "'[urls][0][tags]' should be list"

    def test_post_tag(self):
        """
        POST hv1/tag: Query tag, Should know all tags first
        """
        response = self.client.add_tag(tag="Retefe")

        assert response.status_code == 200, "'status_code' should be 200"
        assert response.json()["query_status"] == 'ok', "key 'query_status' should be ok"
        assert "urls" in response.json(), "lack 'urls' key in response"
        assert re.match("\d+", response.json()["url_count"]), "key 'url_count' should be number"
        assert isinstance(response.json()["urls"], list), "'urls' should be list"
        assert isinstance(response.json()["urls"][0]["tags"], list), "'[urls][0][tags]' should be list"

    @pytest.mark.parametrize(
        "limit, expected_status, expected_error",
        [
            ("gg", 404, "Invalid parameter: limit must be an integer, Return 404"),
            ("-1", 404, "Invalid parameter: limit must be a positive integer, Return 404"),
            (None, 200, "Missing parameter: limit, Return all urls"),
        ]
    )
    def test_get_recent_urls_invalid(self, limit, expected_status, expected_error):
        """
        GET v1/urls/recent/limit/{X}: Error handling
        """
        endpoint = f"urls/recent/limit/{limit}/" if limit is not None else "urls/recent/limit//"
        try:
            response = self.client.get(endpoint)
        except Exception as e:
            assert isinstance(e, HTTPError), f"expected HTTPError, actual get {type(e)}"
            response = e.response

        assert response.status_code == expected_status, f"expected status code {expected_status},actual get {response.status_code}"

    @pytest.mark.parametrize(
        "tag, expected_status, expected_error",
        [
            ("kkk", 200, "no_results"),
            ("", 200, "Tag cannot be empty, return all tags"),
            (None, 200, "Missing parameter: tag, return None"),
        ]
    )
    def test_post_tag_invalid(self, tag, expected_status, expected_error):
        """
        POST hv1/tag: Error handling
        """
        try:
            response = self.client.add_tag(tag=tag)
        except Exception as e:
            assert isinstance(e, HTTPError), f"expected HTTPError,actual get {type(e)}"
            response = e.response

        assert response.status_code == expected_status, f"expected status code {expected_status}, actual get{response.status_code}"
        if tag == 'kkk':
            assert "no_results" in response.json()["query_status"], f"expected error msg {expected_error}, actual get {response.json()}"
        elif tag == "":
            assert response.json()["query_status"] == 'ok', "key 'query_status' should be ok"
        else:
            assert response.text == "", "response.text should be empty"
