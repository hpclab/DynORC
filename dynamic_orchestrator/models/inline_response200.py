from __future__ import absolute_import
from dynamic_orchestrator.models.base_model_ import Model
from dynamic_orchestrator import util


class InlineResponse200(Model):

    def __init__(self, filename: str=None, app_id: str=None):  # noqa: E501
        """InlineResponse200 - a model defined in Swagger

        :param filename: The filename of this InlineResponse200.  
        :type filename: str
        :param app_id: The app_id of this InlineResponse200.  
        :type app_id: str
        """
        self.swagger_types = {
            'filename': str,
            'app_id': str
        }

        self.attribute_map = {
            'filename': 'filename',
            'app_id': 'app_id'
        }
        self._filename = filename
        self._app_id = app_id

    @classmethod
    def from_dict(cls, dikt) -> 'InlineResponse200':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The inline_response_200 of this InlineResponse200.  # noqa: E501
        :rtype: InlineResponse200
        """
        return util.deserialize_model(dikt, cls)

    @property
    def filename(self) -> str:
        """Gets the filename of this InlineResponse200.


        :return: The filename of this InlineResponse200.
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename: str):
        """Sets the filename of this InlineResponse200.


        :param filename: The filename of this InlineResponse200.
        :type filename: str
        """

        self._filename = filename

    @property
    def app_id(self) -> str:
        """Gets the app_id of this InlineResponse200.


        :return: The app_id of this InlineResponse200.
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id: str):
        """Sets the app_id of this InlineResponse200.


        :param app_id: The app_id of this InlineResponse200.
        :type app_id: str
        """

        self._app_id = app_id
