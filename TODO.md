
#Future work:

+ Provide Docker networking
    + Network analysis
    + Data storage
    + Web app?

Docker is an exciting technology that makes tools and applications more portable.

##0. Docker

Docker is a virtualization platform that allows applications to run on any
hardware that is running a Docker engine, regardless of host environment. The 
result is an infrastructure that allows an application to be run anywhere. In 
this case, even though the library is built on top of open source Linux 
binaries, you can run PyPing2 on Windows, OSX, GNU/Linux, virtual machines, or 
even ARM machines.

## Requirements:

+ Network connection
+ Docker v1.12 or later (for Docker option)

We'll start with assuming your environment has both of these requirements. The
portability of a Raspberry Pi (RPi) is a great use case for PyPing -- if you
need to install Docker on your RPi, run this command: `curl https://get.docker.com | sh`. 
If you receive errors about existing installs, remove previous installs of 
Docker from your RPi with `sudo apt-get purge "docker*"`.

##1. Production: Dockerized workflow 

###Create the environment

Getting started with PyPing2 is easy -- you only need to pull the Docker image, 
and finally spin up the container you will work in.

As a first step, enter the directory where you downloaded or cloned the repo.

###The Docker network

There are different network drivers to use, host network will bypass reporting
the Docker VM IP and is [as fast as host networking](https://www.elastic.co/blog/docker-networking)

###Pull the Docker image

~~Next, build the docker image using the Dockerfile.~~ As much as we all love
building tools from source, for convenience, you can pull an image with all 
tests and tools included:

        docker pull victorclark/PyPing2

###The tests:

If you have a script called example.py, you can run you tests with this docker command:

        docker run --rm \                               #remove after use
            --net=host \                                #this removes Docker NAT
            -v {directory with PyPing2.py}:/pyping2 \   # $(pwd)
            victorclark/PyPing2 \
            python example.py

It's easiest to run Docker in the same directory as you script, so pass the argument to -v like this: `-v $(pwd):PyPing2`


##3. Development: Hacking on PyPing2

What to take a stab at PyPing2? Great! This workflow's contents will help you along the way:

###Spin up container

Now spin up a container that will run the PyPing2 library. Many ways to do it,
here's a suggestion:

        docker run -itd \
            --net=host \                                #this removes Docker NAT
            -v {directory with PyPing2.py}:/pyping2 \
            --name [name for container] \
            victorclark/PyPing2

Note that the -v flag doesn't accept '.' as an argument -- if you'd like to 
mount your current directory, and you're on OSX or GNU/Linx use `$(pwd)`. Note
that this mount point is created at build time and will not update for containers
that are stopped and started. If you change directories, restart, and attach,
you will mount the directory passed during build time.

###Attach container

Finally, attach the container to access the environment we will use for PyPing2:

        docker attach PyPing2

You may need to hit enter twice to see the prompt change. You are now in the
PyPing2 container!

Return to the host machine from the PyPing2 container anytime with `ctrl+p`, 
`ctrl+q`.

To stop the PyPing2 container with the `exit` command or `ctrl+d`. Before you
can reattach the container, you need to start the container again with:

        docker start pyping2

###Set timezone

Docker uses the system time when writing test results and pcap files. If you'd like to set it to something different than UTC, use the command below:

        dpkg-reconfigure tzdata

