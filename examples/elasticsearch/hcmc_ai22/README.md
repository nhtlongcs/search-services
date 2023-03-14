## AIC Datasets

This directory contains the scenetext datasets for the Elasticsearch example in HCM-AIC.
AIC dataset is a collection of news videos of Vietnamese News Channel. The example contains
id and extracted scene text of each video every given frame. 


We do not provide the extract method in this example. You can use your own method to extract.
The example only shows how to index and search the data.

### Data format

The data format is a csv file with the following fields:

```csv
id,frame,text
```

- `id`: the id of the video
- `frame`: the frame number
- `text`: the extracted scene text

### Indexing

The indexing process is done by the `index.ipynb` notebook. The notebook transforms the csv
file into dictionary format and then index the data into Elasticsearch.

### Searching

