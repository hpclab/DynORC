'''
Created on 8 feb 2021

@author: Ferrucci
'''
    
from abc import ABCMeta, abstractmethod, abstractproperty

class AbstractOrchestrator(metaclass=ABCMeta):

    def AppModelContent_getter(self):
        return 

    def MonitorDataContent_getter(self):
        return 

    @abstractmethod
    def calculate_dep_plan(self, AppModelContent, MonitorDataContent):
        """calculate_dep_plan
           parsing of the AppModel and MonitorData must be done in this method
        :param AppModelContent: 
        :type AppModelContent: 
        :param MonitorDataContent: 
        :type MonitorDataContent: 

        :rtype: List[str] list of file names
                return a None List if there is an error during process 
        """
        return  #['./test/ProvaAppModel.yml', './test/ProvaMonitorModel.yml'] 
    
    AppModelContent = abstractproperty(AppModelContent_getter)
    MonitorDataContent = abstractproperty(AppModelContent_getter)


        