HextoRGB Converter Guide
===========
----------------------

This is a WIP development guide for HextoRGBConverter. Please follow the instructions to run/contribute to the project.

#### HOW TO ?
Follow these instructions to run this project locally

- Make sure you installed **Docker** and **docker-compose** in your local machine; If not please follow the links to do the same.
    
    - [Docker installation guide](https://docs.docker.com/engine/installation/) <br>
    - [Docker-compose installation guide](https://docs.docker.com/compose/install/)

- Clone the project to local machine
    ```commandline
    git clone https://github.com/athulk2dev/HexToRGBConverter.git
    ```
    
- Change directory to project
    ```commandline
    cd HexToRGBConverter/
    ```
- Run following command
    ```commandline
    docker-compose up
    ```
    This will take a while to complete the process, please be patient. 

## TESTING

To test the api, send a post request to **http://127.0.0.1:8080/convert/**, with the following post data 
  ```
    { 'hex' : HEX_CODE_TO_BE_CONVERTED }
   ```
## DESIGN CHOICES

- Used AIOHTTP to design the api and provide concurrency, to reduce the overhead cost of running Celery to acheive concurrency when using Flask or Falcon

## NOTE 
If you are using linux machine, you may need to add ```sudo``` as prefix to ```docker``` and ```docker-compose``` commands.
