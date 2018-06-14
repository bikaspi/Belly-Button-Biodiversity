# import necessary libraries
import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
samples=pd.read_csv("./DataSets/belly_button_biodiversity_samples.csv")
otu=pd.read_csv("./DataSets/belly_button_biodiversity_otu_id.csv")
metadata=pd.read_csv("./DataSets/Belly_Button_Biodiversity_Metadata.csv")

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route('/names')
def names():
    sample_ids=metadata["SAMPLEID"]
    results=["BB_"+str(sample) for sample in sample_ids]
    return jsonify(results)

  # Create OTU route
@app.route('/otu') 
def otulist():
    otus=otu["lowest_taxonomic_unit_found"]
    return jsonify(otus.tolist())

    #Create app for meta data

@app.route('/metadata/<sample>')
def get_metadata(sample):
    sample_id=int(sample[3:])
    record=metadata[metadata.SAMPLEID==sample_id].iloc[0]
    return record.to_json()

@app.route('/wfreq/<sample>')
def wfreq(sample):
    sample_id=int(sample[3:])
    record=metadata[metadata.SAMPLEID==sample_id].iloc[0]
    wfreq1=record["WFREQ"]
    return jsonify(wfreq1)

@app.route('/samples/<sample>')
def get_samples(sample):
    sorted_sample=samples.sort_values(sample,ascending=False)
    results={
        "otu_ids": sorted_sample['otu_id'].tolist(),
        "sample_values":sorted_sample[sample].tolist()
    }
    return jsonify(results)





if __name__ == "__main__":
    app.run()
   

