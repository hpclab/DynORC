'''
Created on 11 feb 2021

@author: Luca Ferrucci
'''

from dynamic_orchestrator.core.abstract_orchestrator import AbstractOrchestrator
#from numbers import Number
from mip import Model, xsum, BINARY, maximize, OptimizationStatus
import json
#import math

class ConcreteOrchestrator(AbstractOrchestrator):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''               
    def add_latency_to_component_requirements(self,component_reqs,application_component_instance_name, application_parameters): 
        for component in application_parameters:
            if component._component_name == application_component_instance_name:
                if component._latency_qoe_level_threshold:
                    component_reqs['hardware_requirements']['latency_qoe_level_threshold_' + application_component_instance_name] = component._latency_qoe_level_threshold
                                        
    def component_requirements_translation(self, requirements, application_component_instance_name):
        component_translation = {}
        for requirement_name, requirement_value in requirements.items():
            if requirement_name == 'os':
                if requirement_value == 'linux':
                    component_translation['QEos'] = 1             
            if requirement_name == 'arch':
                if requirement_value == 'x86_64': 
                    component_translation['QEarch'] = 1
                elif 'ARM' in requirement_value:                  
                    component_translation['QEarch'] = 2                
            if requirement_name == 'hardware_requirements':
                for hw_requirement_name, hw_requirement_value in requirements['hardware_requirements'].items(): 
                    if hw_requirement_name == 'cpu':
                        component_translation['hardware_requirements_cpu'] = int(hw_requirement_value)
                    if hw_requirement_name == 'ram':
                        component_translation['hardware_requirements_ram'] = int(hw_requirement_value)
                    if hw_requirement_name == 'disk':
                        component_translation['hardware_requirements_disk'] = int(hw_requirement_value)
                    if 'latency_qoe_level_threshold' in hw_requirement_name:
                        component_translation['QLlatency_qoe_level_threshold_' + application_component_instance_name] = hw_requirement_value
                    #if hw_requirement_name == 'gpu':
                    #    for gpu_requirement_name, gpu_requirement_value in requirements['hardware_requirements']['gpu'].items():
                    #        if gpu_requirement_name == 'model':
                    #            if 'INTEL' in gpu_requirement_value:
                    #                component_translation['QEhardware_requirements_gpu_model'] = 3
                    #            if 'NVIDIA' in gpu_requirement_value:
                    #                component_translation['QEhardware_requirements_gpu_model'] = 1
                    #            elif 'AMD' in gpu_requirement_value:
                    #                component_translation['QEhardware_requirements_gpu_model'] = 2
                    #        if gpu_requirement_name == 'dedicated':
                    #            if gpu_requirement_value == 'True':
                    #                component_translation['Qhardware_requirements_gpu_dedicated'] = 1
                                                                    
        return component_translation

    def node_resources_translation(self, current_app, node, lat_qoe_levels): 
        node_res_translation = {}
        
        current_app.config.get('LOGGER').info('[') 
        current_app.config.get('LOGGER').info('   ... ')
        current_app.config.get('LOGGER').info('   Node name: %s' % node['device.device_name'])
        
        if 'arm' in node['device.CPU.Arch']:                    
            node_res_translation['QEarch'] = 2
            current_app.config.get('LOGGER').info('   Architecture: Armv7')
        elif node['device.CPU.Arch'] == 'x86_64':
            node_res_translation['QEarch'] = 1
            current_app.config.get('LOGGER').info('   Architecture: Intel x86_64')
        else:
            node_res_translation['QEarch'] = 0
            
        if node['device.OS.OS_name'] == 'Linux':
            current_app.config.get('LOGGER').info('   OS: Linux')
            node_res_translation['QEos'] = 1
        else:
            node_res_translation['QEos'] = 0        
          
        for app_component_name, lat_qoe_level_list in lat_qoe_levels.items():
            minicloud_found = False
            for lat_qoe_level in lat_qoe_level_list:                  
                if lat_qoe_level:
                    if lat_qoe_level['minicloudId'] == node['minicloud_id']:
                        node_res_translation['QLlatency_qoe_level_threshold_' + app_component_name] =  lat_qoe_level['qoe']
                        current_app.config.get('LOGGER').info('   Latency QoE Threshold  for component' + app_component_name + ': %s ' % (node_res_translation['QLlatency_qoe_level_threshold_' + app_component_name]))
                        minicloud_found = True
                else:
                    node_res_translation['QLlatency_qoe_level_threshold_' + app_component_name] = -1
                    current_app.config.get('LOGGER').info('   Latency QoE Threshold for component' + app_component_name + ': NA ')

            if minicloud_found == False:
                node_res_translation['QLlatency_qoe_level_threshold_' + app_component_name] = -1
                current_app.config.get('LOGGER').info('   Latency QoE Threshold  for component' + app_component_name + ': NA ')
                

        node_res_translation['hardware_requirements_cpu'] = node['device.CPU.cores'] - (node['device.CPU.cores'] * float(node['cpu_usage(percentage)'])/100)
        current_app.config.get('LOGGER').info('   Number of CPU cores: %s ' % node['device.CPU.cores'])
        
        node_res_translation['hardware_requirements_ram'] = int(node['available_memory(bytes)'])
        current_app.config.get('LOGGER').info('   Memory: %s ' % node['device.RAM(bytes)'])

        
        node_res_translation['hardware_requirements_disk'] = int(node ['disk_free_space(bytes)'])
        current_app.config.get('LOGGER').info('   Disk size: %s ' % node['device.DISK.size'])
        current_app.config.get('LOGGER').info('   ...')
        current_app.config.get('LOGGER').info(']')
        
        #if 'Intel' in node['device.GPU.GPU_name']:
        #    node_res_translation['QEhardware_requirements_gpu_model'] = 3
        #if 'AMD' in node['device.GPU.GPU_name']:
        #    node_res_translation['QEhardware_requirements_gpu_model'] = 2
        #elif 'Nvidia' in node['device.GPU.GPU_name']:
        #    node_res_translation['QEhardware_requirements_gpu_model'] = 1
        #else:
        #    node_res_translation['QEhardware_requirements_gpu_model'] = 0
           
        #if 'Integrated' in node['device.GPU.GPU_type']:
        #    node_res_translation['Qhardware_requirements_gpu_dedicated'] = 0
        #else:
        #    node_res_translation['Qhardware_requirements_gpu_dedicated'] = 1
            
        return node_res_translation
        
    def generate_app_components_request_model(self, components, matchmaking_model,application_parameters):      
        app_components_request_model = []    
        application_component_instance_parts = components[0].component_name.rsplit('-',1)
        application_instance = application_component_instance_parts[0]
        for component in matchmaking_model[application_instance]:
            for application_component_instance_req in components:
                if application_component_instance_req.component_name == component['component']:
                    # Found the requirements of one the component to be deployed
                    self.add_latency_to_component_requirements(component['host']['requirements'], application_component_instance_req.component_name, application_parameters) 
                    app_components_request_model.append(self.component_requirements_translation(component['host']['requirements'], application_component_instance_req.component_name))                           
        return app_components_request_model
    
    def generate_federation_resource_availability_model(self, current_app, node_parts,lat_qoe_levels):
        federation_resource_availability_model = []
        for node in node_parts:          
            #node = json.loads(node_parts[i])
            federation_resource_availability_model.append(self.node_resources_translation(current_app,node,lat_qoe_levels))       
        return federation_resource_availability_model
    
    def calculate_dep_plan(self, current_app, components, node_parts, matchmaking_model, application_parameters,lat_qoe_levels):
        """calculate_dep_plan
           matchmaking of components and ACCORDION federation resources will be done in this method
        :param components: 
        :type : array of dictionaries
        :param : RID_response
        :type : 
        :param : matchmaking_model
        :type : 
        :rtype: List[str] list of file names
                return a None List if there is an error during process 
                status: -1 Error
                         4 Infeasible 
                         5 No solution found
                                              
        """            
        
        App_Components_req = self.generate_app_components_request_model(components,matchmaking_model,application_parameters)
        
        #node_parts = RID_response.split('\n')
        Fed_res_availability = self.generate_federation_resource_availability_model(current_app, node_parts,lat_qoe_levels)
                
        # Construction of Python-MIP MILP problem
        current_app.config.get('LOGGER').info(" Request to solver started to calculate deployment plan ")  

        MILP = Model()
        NumComponents = len(App_Components_req)
        NumNodes = len(Fed_res_availability)
        
        # decision variables: decision_vars x(jn) with j in Components, n in Nodes 
        decision_variables = [[MILP.add_var('x({},{})'.format(j, n), var_type=BINARY)
                            for j in range(NumComponents)] for n in range(NumNodes)]

        # every application component MUST be deployed     
        #MILP += xsum(decision_variables[n][j] 
        #             for j in range(NumComponents) 
        #                for n in range(NumNodes)) == NumComponents
        
        # every application component MUST be deployed on exactly a Node
        for j in range(NumComponents):
            MILP += xsum(decision_variables[n][j]  for n in range(NumNodes)) == 1
            
        # every dep plan must respect contraints on resource availability of every Node
        for resource in Fed_res_availability[0]:
            if not (resource == 'links'): 
                if not (resource[0] == 'Q'):
                    n=0
                    for Node in Fed_res_availability:    
                        MILP += xsum(((decision_variables[n][j])*((App_Components_req[j])[resource])) 
                                     for j in range(NumComponents) 
                                        if resource in (App_Components_req[j])) <= Node[resource]
                        n+=1 
         
        # every dep plan must respect constraints on QoS indicators of every Nodes
        #(case of a resource with first letter Q not followed by the letter E 
        for resource in Fed_res_availability[0]:
            if not (resource == 'links'): 
                if (resource[0] == 'Q' and (not resource[1] == 'E')):
                    n=0
                    for Node in Fed_res_availability:    
                        for j in range(NumComponents):
                            if resource in (App_Components_req[j]):
                                res_diff = (App_Components_req[j])[resource] - Node[resource]
                                if not (res_diff == 0):
                                    MILP += ((decision_variables[n][j])*res_diff) <= 0                                
                        n+=1                                            
        
        # every dep plan must respect constraints on QoS indicators of every Node
        #(case of a resource with first letter Q, followed by the letter E 
        # In this case the value of the decision variable must be an exact value: if it is not present
        # in the requirements of the components, it means that it's not important 

        for resource in Fed_res_availability[0]:
            if not (resource == 'links'): 
                if (resource[0] == 'Q' and resource[1] == 'E'):
                    n=0
                    for Node in Fed_res_availability:    
                        for j in range(NumComponents):
                            if resource in (App_Components_req[j]):
                                if not ((App_Components_req[j])[resource] == Node[resource]):
                                    MILP += (decision_variables[n][j]) == 0                                
                        n+=1  
               
        # auxiliary decision variables: decision_vars y (ijn1n2) with i and j in Components with i!=j, n1 and n2 in Nodes with n1!=n2 
        #auxiliary_decision_variables = [[[[MILP.add_var('y({},{},{},{})'.format(i, j, n1, n2), var_type=BINARY)
        #        for i in range(NumComponents)] for j in range(NumComponents)] for n1 in range(NumNodes)] for n2 in range(NumNodes)]               
                              
        # every dep plan must respect contraints on resource availability of every link between components, 
        # for every network link between Nodes, using auxiliary variables to linearize the constraint        
        #for edge_resource in ((Fed_res_availability[0])['links'])[0]:
        #    if not (edge_resource[0] == 'Q'):
        #        n1=0
        #        for Nodes in Fed_res_availability:
        #            n2=0 
        #            pos=0
        #            while n2 < len(Fed_res_availability):                        
        #                if not (n1 == n2):      
        #                    MILP += xsum(((auxiliary_decision_variables[n2][n1][j][i])*((((App_Components_req[i])['links'])[j])[edge_resource]))
        #                             for i in range(NumComponents)
        #                                  for j in range(NumComponents) 
        #                                    if not (i==j) 
        #                                        if ((App_Components_req[i])['links']) 
        #                                            if (j in ((App_Components_req[i])['links'])) 
        #                                                if ((App_Components_req[i])['links'])[j] 
        #                                                    if (edge_resource in ((App_Components_req[i])['links'])[j])) <= ((Nodes['links'])[pos])[edge_resource]
        #                    pos+=1
        #                n2+=1
        #            n1+=1            
  
        # every dep plan must respect contraints on QoS indicators of every link between components, 
        # for every network link between Nodes, using auxiliary variables to linearize the constraint
        #for edge_resource in ((Fed_res_availability[0])['links'])[0]:
        #    if (edge_resource[0] == 'Q'):
        #        n1=0
        #        for Nodes in Fed_res_availability:
        #            n2=0 
        #            pos=0
        #            while n2 < len(Fed_res_availability):                        
        #                if not (n1 == n2):  
        #                    for i in range(NumComponents):
        #                        for j in range(NumComponents): 
        #                            if not (i==j):   
        #                                if ((App_Components_req[i])['links']): 
        #                                    if (j in ((App_Components_req[i])['links'])): 
        #                                        if ((App_Components_req[i])['links'])[j]:
        #                                            if (edge_resource in ((App_Components_req[i])['links'])[j]):                                                         
        #                                                    MILP += ((auxiliary_decision_variables[n2][n1][j][i])*((((App_Components_req[i])['links'])[j])[edge_resource] - ((Nodes['links'])[pos])[edge_resource])) <= 0
        #                    pos+=1                            
        #                n2+=1
        #            n1+=1  
                    
        #conditions to link auxiliary decision variable to main decision variables
        #for i in range(NumComponents):
        #    for j in range(NumComponents): 
        #        if not (i==j):
        #            for n1 in range(NumNodes):
        #                    for n2 in range(NumNodes):   
        #                        if not (n1==n2):                         
        #                            MILP +=  (decision_variables[n1][i] + decision_variables[n2][j] - auxiliary_decision_variables[n2][n1][j][i]) <= 1
        #                            MILP +=  (decision_variables[n1][i]/2 + decision_variables[n2][j]/2 - auxiliary_decision_variables[n2][n1][j][i]) >= 0
     
        # Maximize the availability of resources, except QoS indicators 

        MILP.objective = maximize(xsum ((Fed_res_availability[n])[resource] -  
                                        xsum(((decision_variables[n][j])*((App_Components_req[j])[resource]))
                                               for j in range(NumComponents) 
                                                    if resource in (App_Components_req[j])) 
                                          for n in range(NumNodes)
                                               for resource in Fed_res_availability[0]
                                                  if not (resource == 'links')
                                                    if not (resource[0] == 'Q'))
        
                                #and maximize the QoE for latency
                                + xsum ((Fed_res_availability[n])[resource] * (decision_variables[n][j])
                                          for n in range(NumNodes)
                                               for resource in Fed_res_availability[0]
                                                    for j in range(NumComponents) 
                                                        if resource in (App_Components_req[j]) 
                                                            if not (resource == 'links')
                                                                if ((resource[0] == 'Q') and (resource[1] == 'L'))))
                                                                               
        status = MILP.optimize()
        result_documents = {}
        if status == OptimizationStatus.ERROR or status == OptimizationStatus.NO_SOLUTION_FOUND or status == OptimizationStatus.INFEASIBLE or status == OptimizationStatus.INT_INFEASIBLE or status == OptimizationStatus.UNBOUNDED:  
            return None, status
        if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
            #print('solution:')
            n=0
            for v in MILP.vars:
                if(v.name[0] == 'x'):
                    if v.x == 1:
                        Nodes = divmod(n,NumComponents)[0]  
                        #print('Nodes: ', Nodes)                 
                        Appcomponent = divmod(n,NumComponents)[1]
                        #print('AppComponent: ', Appcomponent)                                                    
                        minicloud_id = node_parts[Nodes].get('minicloud_id')
                        minicloud_id = minicloud_id[:3]
                        if not result_documents.get(minicloud_id):
                            result_documents[minicloud_id] = []
                        name = components[Appcomponent].component_name
                        result_documents[minicloud_id].append(name)    
                    #print('{} : {}'.format(v.name, v.x))
                    n+=1 
        return result_documents, status       