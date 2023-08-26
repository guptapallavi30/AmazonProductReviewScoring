# AmazonProductReviewScoring

Welcome!

## Goal
The goal of this project was to:
1) Create a ML prediction Model that predicts a overall score a user *might* give to a product, given their text review,
2) Create a Flask project that runs the model and displays its result with a simple UI,
3) Integrate the Flask model with Docker, and
4) Create a github workflow to create Docker images with the codebase.

Follow along for details and resources that help explain the purpose and scope of this project!

## Purpose

The purpose of this project was to understand how scalable ML models can be used and distributed through cloud-based distributing processes.

To simplify the complexity of the whole pipeline, the creation and testing of the ML model itself was done through Google Colab, and the model implementation was done with Flask. 

## Quick Timeline

**Disclaimer**

_"The ML Model started out with a different prediction goal in mind. The previous goal was to create a model that would determine the popularity of a review given the text review, the user's verified status, and the overall score deemed by the user. However, the few simple models created from the chosen dataset didn't provide as much value as anticipated. Some reasons for this may be the heavy skewed upvotes for the data. Furthermore, my hypothesis is that the upvotes are also influenced by the validity of the review: If users are to vote the reviews after having purchased the product, their support for the comment is influenced not only by the details of the review but also by how much they are in agreement with what has been posted. As a result, while the models for this goal are achievable with further research and experimentation, the goal was changed to simplify the model and understand the other primary aspects of this project."_

### Pipeline

- Once a model is created in colab, it is compressed and saved externally on github. As github has a file size limit of 100MB, the compressed files were saved as a release extension.

- When Docker starts, the flask app then moves the compressed file to a new Docker Volume, and opens the files in that volume so they are ready to use within the application.

- After the files have been loaded, it can collect the input data from the UI and then display the prediction result!

## Final Thoughts

This project was enlightening. 

I learned a lot about the finer details involved in building a docker image and running a docker container, and the nuances of flask. 
Some obstacles I faced along the way were 
- **Creating a model** that could provide results that somewhat correlated with our expected predictions when reading a review text. Having worked with NLP before, I set out to explore different techniques for achieving similar language processing models. I explored RandomForestClassifier, LogisticRegression, SVC, and Neural Networks, ultimately settling with RandomForestClassifier as it provided a greater accurate model without much optimization. _(tfidf stands for TfidfVectorizer)_
- **Setting up Docker.** Not a obstacle per se, but I devoted time to understand the terminology of Docker and how to use Docker Desktop. Some resources I used are listed under the _Resources_ section. One of the bigger parts of my understanding came from setting up docker compose and new volumes. I am grateful for taking this direction into experimenting with Docker as it helped me understand the mechanisms of Kubernetes in my external studies!
- **Loading my compressed files.** Somehow, I underestimated the classes involved with de-compressing and loading a .pkl file. Initially I started with zipping both my model and tfidf files. Once I got my model running, I was having trouble uploading my zipped files due to the github file size limit. Eventually I resorted to compressing my model into lzma which reduced the file size but not enough for it to get uploaded into github aas a regular file. I stumbled upon git Releases, which meant I could upload my file, but had modified my flask app to allow the decompression of a .xz file. Ultimately, the difficulty of reaching the file size limit urged me to explore lmza compression, github releases, docker volumes and joblib. A win is a win.

In terms of the future goals for this project, I aim to go back and achieve the original goal I had created for creating an ML model that determines the popularity of a review. Furthermore, I shall explore more functionalities of Flask, to create a more compelling and complex UI design.

If you would like to run and experiment with this project on your own, feel free to fork or **download the release version v1.0.3** to get access to the compressed files and the source code.  
Below I have listed some resources I used during the course of the project. 

Cheers! 

## Resources

The dataset retrieved was through a secondary source: The UCSD Dataset for Amazon Review Data (2018). Below are the links to access the files:

https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/
https://cseweb.ucsd.edu/~jmcauley/datasets.html#amazon_reviews

And here is the Citation for using the datasets:

_Justifying recommendations using distantly-labeled reviews and fined-grained aspects
Jianmo Ni, Jiacheng Li, Julian McAuley
Empirical Methods in Natural Language Processing (EMNLP), 2019 [pdf](!https://cseweb.ucsd.edu//~jmcauley/pdfs/emnlp19a.pdf)_

_Ups and downs: Modeling the visual evolution of fashion trends with one-class collaborative filtering
R. He, J. McAuley
WWW, 2016
[pdf](!https://cseweb.ucsd.edu/~jmcauley/pdfs/www16a.pdf)_

_Image-based recommendations on styles and substitutes
J. McAuley, C. Targett, J. Shi, A. van den Hengel
SIGIR, 2015
[pdf](!https://cseweb.ucsd.edu/~jmcauley/pdfs/sigir15.pdf)_

----
This Docker site includes **step-by-step instructions** into setting up a Flask app with Docker, starting a Docker Image, Running a Docker Container, and Integrating a CI/CD pipeline with Github.:
https://docs.docker.com/language/python/build-images/


For further instructions and **walkthroughs**, make sure to download **Docker Desktop** from their main site here:
https://www.docker.com/products/docker-desktop/

Here is a youtube channel I came across that was extremely helpful in covering Docker with examples and necessary information. I highly recommend giving **TechWorld with Nana** a follow as - in my humble opinion - she is doing wonderful work to create content for being informed about the technologies of the tech world. Check out her **Docker Tutorial for Beginners [FULL COURSE in 3 Hours]** here:
https://www.youtube.com/watch?v=3c-iBn73dDE

Last but not least, here is a personal notes document I created to refer to when debugging and running my Docker project:

**Create New Virtual Environment**

    python3 -m venv .venv

**Enter Venv**

    source .venv/bin/activate

**Install any dependencies from docker**

    python3 -m pip install -r requirements.txt

**Run app**

    python3 -m flask run

**Exit Venv**

    deactivate

**Build Docker Image; this 'tag' is for REPOSITORY name attribute**

    docker build --tag docker-model_01 .

**View Docker Images**

    docker images

**Change tag; this 'tag' is for the TAG attribute**

    docker tag [image-name]:latest [image-name]:[tag-value]

**Remove tag attribute custom value**

    docker rmi [image-name]:[tag-value]

**Run Docker app:**
- **'-p' means publish: _The app runs on a virtual environment port. I cannot see the app run until i have a "window" to see the app run on my local computer. SO, i have to map the virtual environment port to a local port so I can see my app run on my local laptop._**
- **'-d' means detached mode**
- **run with volume attached '-v'**

        docker run 
        -d 
        -v /path/to/host/[local_folder]:/app/[volume_folder]
        -p [local port (ie. 8000)]:[venv port (default: 5000)] 
        [image-name]

- **example:**

        docker run 
        -v [my full path to this folder]/model_files:/app/model_files 
        -p 8000:5000 
        docker-model_01:v1.0.3

**OR have a compose.yaml file. Simply use this to build and start the services defined in the docker-compose.yaml file, including setting up the volume mapping as specified.**

    docker-compose up

**View all Docker containers**

    docker ps --all

**Can restart/stop/remove containers**

    docker restart [container-name]
    docker stop [container-name]
    docker rm [container-name]

**need to configure Docker Desktop to allow access to the local directory you want to mount as a volume.**

Docker Desktop -> Settings -> Resources -> File Sharing -> Add path to local volume directory.

**View the detached mode container's folder in terminal**

    docker ps
    docker exec -it container_id_or_name sh

**exit detached mode container's folder in terminal**

    exit

