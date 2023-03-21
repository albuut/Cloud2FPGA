# Template for Web Applications at UCR

This repository contains a simple templete to develop and deploy a simple web application with a front-end,
back-end API, and data store. Both the back-end and front-end are then pulled under the same server using
Nginx as a reverse proxy. This configuration avoids issues with cross-site scripting. These components are 
contained with in Docker and is easily run on a developer's computer. Additionally, it can be deployed for 
testing, staging and production.

Below is a brief description of the frameworks for each of the front-end, back-end API and data store. Then 
the steps necessary to get this template up and running are provided. At the end is a list of tutorials that
will help the user create the code necessary for their own projects using the frameworks. Discussions about
how to use these frameworks is beyond the scope of this document, and best handled by their developers.

Below is a drawing that represents the overall architecture.

![Template Architecture Diagram](/assets/architecture.png)

## Front-End

For the front-end web interface, this template uses the [Vue](https://vuejs.org/) framework. I chose this 
framework because of its overall quality, my experience with it and the growing number of projects using it
in place of other frameworks such as Reactive. 

Vue is a good replacement for React because it's somewhat simpler to learn and is slightly less verbose. 
While an argrument could be made for React and many other frameworks, this is my template, so Vue is the
choice.

The code given as the project template was directly created using the VUE cli.

## Back-end API

For the back-end API, this template uses the [Django](https://www.djangoproject.com/) framework. I chose this 
framework because it is similar  to Ruby on Rails, a framework I have several years of experience using, and a 
good replacement for Ruby on Rails as well. Ruby on Rails suffers from many weaknesses, not the least of which 
includes it horrible scalability, it's nightmarish upgrade requirements (Ruby and Rails updates are often 
breaking changes), and the fact that fewer and fewer students know Ruby. Python, however, is very well known 
by students, is known to be highly scalable, and while there have been breaking changes in the past, they do 
not seem as severe as the Ruby and Rails changes.

Django is a good replacement for Ruby on Rails because of its scalability and its similarity, with improvements
to Ruby on Rails. For example, in Ruby on Rails, the DB model is in a separate file from the Model. In Django, 
both the code and DB model are located in the same file.

The code given in this project was created using the Django tutorials.

## Data Store

For the data store, this template uses the [PostgreSQL](https://www.postgresql.org/) database. There's no need 
to justify this choice, since replacing it is the easiest part of these types of projects. Frameworks such as 
Ruby on Rails and Django make change the backend data store very simple. The only part of the template that 
would need to be changes is the docker-compose.yml file.

Included with this template is a seed file that can used to populate the database. A later section will 
how to use this seed file.

## Nginx

To avoid issues with cross-site scripting, this template using [Nginx](https://www.nginx.com/) to reverse proxy 
the back-end API and the front-end for development. For production deployment, Nginx can then directly host
the built code from webpack.

The configuration in this template is taken from this [tutorial](https://blog.logrocket.com/how-to-run-a-node-js-server-with-nginx/).

## Docker

This template uses [Docker](https://www.docker.com/) extensively to provide for a consistent development and 
deployment experience. Docker works on Windows, Mac OS X, and Linux. There are plenty of tutorials online that
can teach you how to use this tool. There are several containers built in this template, and composed together 
using the Docker compose plug-in.

## Getting up and running

To get things started, but sure you have Git, and Docker install. All the other tools will be within a Docker 
container. First clone this repository with the following command in a shell or terminal:

```sh
$ git clone https://github.com/ucrdrk/ucr_webapp_template
```

The `cd` into the directory `ucr_webapp_template`.  Once there, bring up all the 
containers with the following command:

```sh
$ docker compose up -d --build
```

This command will build all the containers, start them with the proper parameters
and then put them all in the background. You can check that all the containers are 
running after the build with the following command:

```sh
$ docker container ps
```

Which should give you output similar to the following:

```sh
CONTAINER ID IMAGE              STATUS         PORTS                   NAMES
b44bc4b06074 ucr_webapp_template-proxy   Up 6 minutes   0.0.0.0:8800->80/tcp    ucr_webapp_template-proxy-1
ce4842fbc28b ucr_webapp_template-api     Up 6 minutes   0.0.0.0:8000->8000/tcp  ucr_webapp_template-api-1
d00e1e7b8235 postgres           Up 6 minutes   0.0.0.0:5432->5432/tcp  ucr_webapp_template-db-1
2fd3dfbf3a2d ucr_webapp_template-web     Up 6 minutes   0.0.0.0:3000->3000/tcp  ucr_webapp_template-web-1
```

Once all the containers are up and running you will we need to setup the database tables, and populate 
it with a couple of rows. To setup the database, use the following command in a terminal or shell:

```sh
$ docker compose exec api python manage.py migrate
```

Next need to create a super user for Django. You can do that using the following docker compose command:
```sh
$ docker compose exec api python manange.py createsuperuser
```

Follow all the prompts to create the username and password for the super user. Once 
you have completed this task you can check that the command was succesfull by going 
in your browser to http://localhost:8000/admin. Login using the credentials you created 
when creating the super user.

Finally, to populate the database with some seed data, enter this final command in a 
terminal or shell:

```sh
$ docker compose exec api python manage.py loaddata seed.json
```

That's it. Now when you go to http://localhost:8800 you should see the front-end with 
the data from the seed. It should look something like the following:

![Screen shot of Template Frontend](/assets/frontend_screenshot.png)

## Tips and Tricks

There are lots of ways to interact with the container as they are running. 

### Viewing logs of the composed containers

To view in real-time the logs of all the containers simultaneously, remove the `-d` flag
from the `docker compose` command. This will continually follow the logs of all the 
containers until you type Ctrl-c, which will bring down all the containers as well.

If you want to view the log of one container then type the following command into a 
terminal or shell:

```sh
$ docker compose logs <service name>
```

The above command will dump the entire contents of the log to the console. To find the service 
name, look in the docker-compose.yml file and identify the serive you want to see the log for.
 To follow the log for a specific container, add the `--follow` argument like this:

```sh
$ docker compose logs --follow <service name>
```

### Getting a shell in a compose container

You can bring up a shell for any of the containers as well. Most, if not all, the 
containers include the bash shell. Type the following command to bring up a shell:

```sh
$ docker compose exec <service name> /bin/bash
```

You can even bring up the PostgreSQL command line tool with the following command:

```sh
$ docker compose exec db psql -U postgres
```

### Why are my changes not taking affect

Sometimes changes to your files will not seem to change the behavior in the container.
For most of the containers, the local filesystem is mounted within the conatiner so that
changes that occur are immediately seen within the contain. However, for example, the
configuration file for Nginx, nginx.conf, is not. When you change it you need to rebuild
the containers. The following command will rebuild all the containers in a compose file:

```sh
$ docker compose build
```
