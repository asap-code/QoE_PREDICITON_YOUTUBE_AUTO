#walking through the decison tree model to infer the youtube auto QoE class using newtwork level measurements
#input {'DTH': (row['DTH']) ,'RTT': (row['RTT']) , 'DJ': (row['DJ']) , 'DL': (row['DL']) , 'UJ':(row['UJ']) , 'UL': (row['UL']) , 'UTH': (row['UTH']) }
#output QoE class(1 to 5)      
#we use youtube auto model(decision tree in a json format) built offline with controlled experiments, PREDICT qoE class for new cases 
#json model ""youtube.dash.json"
#network qos samples  "feedback_subset.csv"
#normalize network qos "normalize_string(datafarame):"

import sys, os
import argparse
import time
import pandas as pd
import numpy as np
from copy import deepcopy
from random import seed
from random import random
from random import randint
qoe_prediction=[]
network_qos_input=[]
samples_file='feedback_subset.csv'



class DecisionTree:
    
    

    def __init__(self, **kwargs):
        self.config = kwargs
        self.axis = 'axis'
        self.comp_ope = 'comparisonOperator'
        self.r_operand = 'rightOperand'
        self.qoe_class = 'qoeClass'
    
    def load_samples(self,samples_file):
        dataframe=pd.read_csv(samples_file,delimiter=';')
        feedback=dataframe.dropna()
        return feedback
    
    def normalize_string(self,datafarame):
        for name in ['RTT','UTH','DL','UL','DTH','DJ','UJ']:
            datafarame[name] = datafarame[name].apply(lambda x: float(x.split()[0].replace(',', '.')))
        return datafarame

    def decide_branch(self, comp_operand, val, f_name, features):
        """
            Decide which branch to select: trueBranch or falseBranch
            Parameters
            ----------
            comp_operand : Comperation Operand "lte"
            val          : value given by model tree
            f_name       : name of the feature
            features     : {dictionary-like}

            Returns
            -------
            trueBranch/falseBranch : String
        """

        if comp_operand == 'lte':
            if features[f_name] <= val:
                return 'trueBranch'
            else: return 'falseBranch'
        else:
            return None

    def predict(self, json_model, X_test):
        """
            Predict QoE given decision tree model in json format

            Parameters
            ----------
            json_model  : {json format}
            X_test_input     : {list of dictionary of features}

            Returns
            -------
            QoE_class_prediction         : {List of estimated qoe classes}
        """

        # We predict MoS record by record
        estimated_mos = []
        #for features in X_test:

        _block_info = {}
        found_qoe = False
        depth = 0
        branch = None
        detail_node = []

        _model = deepcopy(json_model)
        while (not found_qoe):
                # Iterate through block information, and keep it in dictionary
                # such as: axis, comparisonOperator, rightOperand, trueBranch, falseBranch
            for key in _model:

                    # Asap, we reach the leaf of the Tree at the moment, 
                    # Retrieve QoE class and leave the loop
                if key == self.qoe_class:
                        #print('QoE class is %s' % (_model[key]))
                    found_qoe = True
                    estimated_mos.append({'QoE': _model[key], 'Depth': depth, 'Detail_node': detail_node})
                        # Leave while loop
                    break
                else:
                    _block_info[key] = _model[key]
                    #print(_block_info)
                    #print('#############')

                # Once we have information about the block, we are able to calculate cost function
                # To decide whether go to trueBranch or falseBranch
            if (not found_qoe) and bool(_block_info):
                    

                    # Parameters for cost function
                comp_operand = _block_info[self.comp_ope]
                val = _block_info[self.r_operand]
                f_name = _block_info[self.axis]

                    # Increment the deep by one
                depth += 1

                    # Get Branch
                branch = self.decide_branch(comp_operand, val, f_name, X_test)

                    # If there exists one branch, we continue. Otherwise, we break
                if branch:
                        # We decide to continue with one branch of the tree,
                        # Select subtree of the tree
                    _model = deepcopy(_block_info[branch])
                    _block_info = {}
                        #print('----------------------')
                    my_string = "D {0} -> F_name: {1}  (F_Val: {2}, M_Val: {3}) Branch: {4}"
                    _node_info = my_string.format(depth, f_name, X_test[f_name], val, branch)
                    detail_node.append(_node_info)
                        #print('D %s -> F_name: %s  (F_Val: %s, M_Val: %s) Branch: %s' % (depth, f_name, features[f_name], val, branch))
                        #print('----------------------')
                else:
                    break
        # 
        #print(detail_node)
        return estimated_mos

    def load_model_json(self, file):
        """
        Read decision tree model from json file
        """
        #from rapidjson import loads, Encoder
        import json

        try:
            with open(file, 'rb') as handle:
                #model = loads(Encoder(ensure_ascii=True)(handle))
                model = json.load(handle)
        except ValueError as error:
            raise Exception(error)
        else:
            return model
        
    
        

    def __test__(self):
        print("\n\r*******************model output********************\n\r")
        #load json from file (feature data)
        filename = "youtube.dash.json"
        json_model = self.load_model_json(filename)
        for index, row in self.normalize_string(self.load_samples(samples_file)).iterrows():
         # access data using column names, cast to float (bydefault its strings and change ',' to '. for all records')
            feature_1 ={'DTH': (row['DTH']) ,'RTT': (row['RTT']) , 'DJ': (row['DJ']) , 'DL': (row['DL']) , 'UJ':(row['UJ']) , 'UL': (row['UL']) , 'UTH': (row['UTH']) }
            #network_qos_input.append(feature_1)

        # Estimated MoS
            
            estimated_mos = self.predict(json_model, feature_1)
            #print(estimated_mos[0])
            #for _record in estimated_mos:
            print("*** Predicted QoE class %s | Depth %s" % (estimated_mos[0]['QoE'], estimated_mos[0]['Depth']))
            for _info in estimated_mos[0]['Detail_node']:
                print(_info)
                
            print("---------------new sample-----------------")
            ##### list of all the samples predicted qoe ### later just add columns ['youtube_auto_qoe'] to the csv :) 
            qoe_prediction.append(estimated_mos[0]['QoE'])
if __name__ == "__main__":
    whole_st = time.time()

    config = {
        'dataset': 'dataset/model/json',
    }

    dt = DecisionTree()
    dt.__test__()
    prepro_time = time.time() - whole_st
    print(prepro_time)