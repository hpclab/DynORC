from __future__ import absolute_import
from dynamic_orchestrator.models.base_model_ import Model
from dynamic_orchestrator import util


class Body(Model):

    def __init__(self, app_id: str=None, file: str=None):  
        """Body - a model defined in Swagger

        :param app_id: The app_id of this Body.  # noqa: E501
        :type app_id: str
        :param file: The file of this Body.  # noqa: E501
        :type file: str
        """
        self.swagger_types = {
            'app_id': str,
            'file': str
        }

        self.attribute_map = {
            'app_id': 'app_id',
            'file': 'file'
        }
        self._app_id = app_id
        self._file = file

    @classmethod
    def from_dict(cls, dikt) -> 'Body':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The body of this Body.  
        :rtype: Body
        """
        return util.deserialize_model(dikt, cls)

    @property
    def app_id(self) -> str:
        """Gets the app_id of this Body.


        :return: The app_id of this Body.
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id: str):
        """Sets the app_id of this Body.


        :param app_id: The app_id of this Body.
        :type app_id: str
        """

        self._app_id = app_id

    @property
    def file(self) -> str:
        """Gets the file of this Body.


        :return: The file of this Body.
        :rtype: str
        """
        return self._file

    @file.setter
    def file(self, file: str):
        """Sets the file of this Body.


        :param file: The file of this Body.
        :type file: str
        """

        self._file = file
