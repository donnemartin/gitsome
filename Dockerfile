##########################################################
#                                                        #
#  Build the image:                                      #
#    docker build -t gitsome .                           #
#                                                        #
#  Run the container:                                    #
#   docker run -ti --rm -v $(pwd):/src/                \ #
#       -v ${HOME}/.gitsomeconfig:/root/.gitsomeconfig \ #
#       -v ${HOME}/.gitconfig:/root/.gitconfig         \ #
#       gitsome                                          #
#                                                        #
##########################################################
FROM python:3.6

RUN pip install Pillow

COPY /requirements-dev.txt /gitsome/
WORKDIR /gitsome/
RUN pip install -r requirements-dev.txt

COPY / /gitsome/
RUN pip install -e .

RUN mkdir /src/
WORKDIR /src/
ENTRYPOINT ["gitsome"]
