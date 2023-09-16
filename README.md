$ export ENV=prod
$ az acr login --name radionova  
$ docker build . -t radionova.azurecr.io/radionova:1.0  
$ docker push radionova.azurecr.io/radionova:1.0