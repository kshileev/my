# Assorted materials, mainly configuration and examples 
### How to build docker image:
<code>docker build --force-rm --tag my_image:latest .</code>
#### How to run container from the image with current dir mapped to :
<code>docker run -v $PWD:/repo --env MY_ENV=value --name my_container my_image:latest</code>
#### How to run bash in container:
<code>docker exec -it my_container /bin/bash</code>
