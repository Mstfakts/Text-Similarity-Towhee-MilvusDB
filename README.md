# NLP Text Similarity Project w/ Milvus, Docker, and word2Vec


## Installation
Make sure that you have Docker and Docker compose to run the project


## Usage
The usage of this project is as the following;

### Run the Services
The very first step of this project is running all the services. 
```bash
docker-compose up -d
```

### Data to Vectors
Then, convert the HTML based texts to Vectors through the Milvus. 

### Find Similar Jobs
To find the similar jobs from Milvus database, run the following command. However, make sure
that the text in the curl command is preprocessed (no HTML tags, no stopword).

### Check the Outcomes
The similar jobs will be listed in this address: http://127.0.0.1:12345/similar_jobs
The most similar one is located at very firs.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)