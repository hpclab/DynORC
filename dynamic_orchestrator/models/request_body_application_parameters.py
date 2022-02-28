# coding: utf-8

from __future__ import absolute_import
#from datetime import date, datetime  # noqa: F401

#from typing import List, Dict  # noqa: F401

from dynamic_orchestrator.models.base_model_ import Model
from dynamic_orchestrator import util


class RequestBodyApplicationParameters(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, component_name: str=None, external_ip: str=None, latency_qoe_level_threshold: float=None, device_ip: str=None):  # noqa: E501
        """RequestBodyApplicationParameters - a model defined in Swagger

        :param component_name: The component_name of this RequestBodyApplicationParameters.  # noqa: E501
        :type component_name: str
        :param external_ip: The external_ip of this RequestBodyApplicationParameters.  # noqa: E501
        :type external_ip: str
        :param latency_qoe_level_threshold: The latency_threshold of this RequestBodyApplicationParameters.  # noqa: E501
        :type latency_qoe_level_threshold: float
        :param device_ip: The device_ip of this RequestBodyApplicationParameters.  # noqa: E501
        :type device_ip: str
        """
        self.swagger_types = {
            'component_name': str,
            'external_ip': str,
            'latency_qoe_level_threshold': float,
            'device_ip': str
        }

        self.attribute_map = {
            'component_name': 'component_name',
            'external_ip': 'external_ip',
            'latency_qoe_level_threshold': 'latency_qoe_level_threshold',
            'device_ip': 'device_ip'
        }
        self._component_name = component_name
        self._external_ip = external_ip
        self._latency_qoe_level_threshold = latency_qoe_level_threshold
        self._device_ip = device_ip

    @classmethod
    def from_dict(cls, dikt) -> 'RequestBodyApplicationParameters':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The request_body_application_parameters of this RequestBodyApplicationParameters.  # noqa: E501
        :rtype: RequestBodyApplicationParameters
        """
        return util.deserialize_model(dikt, cls)

    @property
    def component_name(self) -> str:
        """Gets the component_name of this RequestBodyApplicationParameters.


        :return: The component_name of this RequestBodyApplicationParameters.
        :rtype: str
        """
        return self._component_name

    @component_name.setter
    def component_name(self, component_name: str):
        """Sets the component_name of this RequestBodyApplicationParameters.


        :param component_name: The component_name of this RequestBodyApplicationParameters.
        :type component_name: str
        """

        self._component_name = component_name

    @property
    def external_ip(self) -> str:
        """Gets the external_ip of this RequestBodyApplicationParameters.


        :return: The external_ip of this RequestBodyApplicationParameters.
        :rtype: str
        """
        return self._external_ip

    @external_ip.setter
    def external_ip(self, external_ip: str):
        """Sets the external_ip of this RequestBodyApplicationParameters.


        :param external_ip: The external_ip of this RequestBodyApplicationParameters.
        :type external_ip: str
        """

        self._external_ip = external_ip

    @property
    def latency_qoe_level_threshold(self) -> float:
        """Gets the latency_qoe_level_threshold of this RequestBodyApplicationParameters.


        :return: The latency_qoe_level_threshold of this RequestBodyApplicationParameters.
        :rtype: float
        """
        return self._latency_qoe_level_threshold

    @latency_qoe_level_threshold.setter
    def latency_qoe_level_threshold(self, latency_qoe_level_threshold: float):
        """Sets the latency_threshold of this RequestBodyApplicationParameters.


        :param latency_threshold: The latency_threshold of this RequestBodyApplicationParameters.
        :type latency_threshold: float
        """

        self._latency_qoe_level_threshold = latency_qoe_level_threshold

    @property
    def device_ip(self) -> str:
        """Gets the device_ip of this RequestBodyApplicationParameters.


        :return: The device_ip of this RequestBodyApplicationParameters.
        :rtype: str
        """
        return self._device_ip

    @device_ip.setter
    def device_ip(self, device_ip: str):
        """Sets the device_ip of this RequestBodyApplicationParameters.


        :param device_ip: The device_ip of this RequestBodyApplicationParameters.
        :type device_ip: str
        """

        self._device_ip = device_ip
