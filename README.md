# QoE_PREDICITON_YOUTUBE_AUTO
YouTube estimeted QoE class from network level measurements(e.g., thourghput, lossrate, and RTT). 
We provide a decison tree model as a json file capturing the link between the network level measurements and the coresponding YouTube QoE CLASS
The model is on a json fomat called YouTube.dash.json, to test we provide realworld samples including network QoS samples(feedback_subset.csv). 
The python code iterate over the json file taking as input the network measurements and give as output the QoE class and the path alll the way to the tree leaf.
