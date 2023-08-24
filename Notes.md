# Create New Virtual Environment
python3 -m venv .venv
# Enter Venv
source .venv/bin/activate
# Install any dependencies from docker
 python3 -m pip install -r requirements.txt
# Run app
  python3 -m flask run

# Exit Venv
deactivate

# Build Docker Image; this 'tag' is for REPOSITORY name attribute
docker build --tag docker-model_01 .

# View Docker Images
docker images

# Change tag; this 'tag' is for the TAG attribute
docker tag [image-name]:latest [image-name]:[tag-value]

# Remove tag attribute custom value
docker rmi [image-name]:[tag-value]

# Run Docker app: Have to map virtual env port to locaal port so I can see the site run on my local laptop
# '-d' means detached mode
# run with volume attached '-v'
docker run 
  -d 
  -v /path/to/host/[local_folder]:/app/[volume_folder] 
  -p [local port (ie. 8000)]:[venv port (default: 5000)] 
  [image-name]


# View all Docker containers
docker ps --all

# Can restart/stop/remove containers
docker restart [container-name]
docker stop [container-name]
docker rm [container-name]

# need to configure Docker Desktop to allow access to the local directory you want to mount as a volume.
# Docker Desktop -> Settings -> Resources -> File Sharing -> Add path to local volume directory.

# docker-model_01:v1.0.3 runs properly:
docker run -v /Users/pallavigupta/Desktop/Other/Github/Docker/Flask-Docker/flask-app/model_files:/app/model_files -p 8000:5000 docker-model_01:v1.0.3

# OR simply use this to build and start the services defined in the docker-compose.yaml file, including setting up the volume mapping as specified.
docker-compose up

# docker-model_01:v1.0.4:
docker run -p 8000:5000 docker-model_01:v1.0.4