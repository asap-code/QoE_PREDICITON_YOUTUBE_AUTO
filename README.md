# what is YouTube.dash.json?
We build a decison tree model able to predict YouTube user experience class from network level measurements(e.g., thourghput, lossrate, and RTT), we save the model as a json file called YouTube.dash.json. The model is able to capture the mapping between the network level measurements and the coresponding YouTube QoE CLASS with an accuracy of around 85%. 

# how to use it ?
To test we provide realworld samples, collected uisng a crowdsourcing application called ACQUA. The samples include network QoS metrics (feedback_subset.csv). 

# Json parsing python code
The python code iterate over the json file taking as input the network measurements and give as output the QoE class and the path all the way to the tree leaf.
