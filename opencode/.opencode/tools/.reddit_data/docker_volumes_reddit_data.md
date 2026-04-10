# Reddit Data - docker volumes

## Collected Posts and Comments

### Post 1: Full Docker Course for Beginners (~3 Hours, Free)
- Score: 323, Comments: 10
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/jhby3d/full_docker_course_for_beginners_3_hours_free/
- Body: Hi there **👋**

I created a [**complete Docker course**](https://youtu.be/3c-iBn73dDE), which I think could be interesting for some (beginners) of you. If you're just getting started with Docker, but maybe also good for refreshing some concepts.

By the end, you will have a deep understanding of the concepts and a **great overall big picture of how Docker is used in the whole software development process**.

The course is a **mix of animated theoretic explanations** and **hands-on demo’s** to follow along, so you get your first hands-on experience with Docker and feel more confident using it in your projects.

.

Demo project: JS/NodeJS/MongoDB/MongoExpress

.

**COURSE OUTLINE**

**What is Docker?**

* What is a container and what problems does it solve?
* Container repository - where do containers live?
* Development - before/after container
* Deployment - before/after container

.

**What is a Container?**

* What is a container technically? (layers of images)
* Demo part (docker hub and run a docker container locally)

.

**Docker vs Virtual Machine**

.

**Docker Installation**

.

**Main Docker Commands**

* docker pull
* docker run
* docker ps
* docker run --options
* docker stop
* docker start
* docker ports, docker port mapping

.

**Debugging a Container**

* docker logs
* docker exec -it

.

**Demo Project Overview - Docker in Practice**

.

**Developing with Containers**

* Pre-Requisites
* what we will do in this part
* 1st part: The JavaScript App (HTML, JavaScr

#### Top Comments:

**Comment 1** (score: 11): I clicked on the post because of the title and began watching because of the content :) Thanks for sharing! I'm specially looking forward to the part about the Docker on AWS.

**Comment 2** (score: 3): Thanks Nana. Really Nice to got this course video as I am picking up docker and network automation recently.

**Comment 3** (score: 3): Thank you Nana!

**Comment 4** (score: 2): Really thanks! I learn a lot!

**Comment 5** (score: 2): I can confirm. Good Quality Content from her YouTube Channel.

She summed up all the key skills needed in the DevOps Space.

---
### Post 2: A Handy Docker-compose commands and examples cheatsheet
- Score: 191, Comments: 6
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/cwe2bt/a_handy_dockercompose_commands_and_examples/
- Body: * [Docker-compose commands cheatsheet](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_commands_cheatsheet)
   * [docker-compose up](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_up)
   * [docker-compose down](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_down)
   * [docker-compose ps](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_ps)
   * [docker-compose bundle](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_bundle)
   * [docker-compose config](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_config)
   * [docker-compose events](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_events)
   * [docker-compose logs](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_logs)
   * [docker-compose port](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_port)
   * [docker-compose pull](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_pull)
   * [docker-compose push](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_push)
   * [docker-compose version](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_version)
   * [docker-compose build](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_build)
   * [docker-compose start](https://jstobigdata.com/docker-compose-cheatsheet/#docker-compose_start)
   * [docker-compose stop](https://jstobigdata.com/docker-compose-cheatsh

#### Top Comments:

**Comment 1** (score: 6): Thank you guys for your upvotes, really encouraging.

**Comment 2** (score: 4): What is bundle used for exactly?

**Comment 3** (score: 1): as someone starting out, this is awesome. i can get the synopsis of what im dealing with without having to go thru pages and pages of documentaiton on the commands.

**Comment 4** (score: 1): I've been using [this](https://www.portainer.io/) as my docker cheatsheet

**Comment 5** (score: 4): Just like how you build containers from images, and images are portable... similarly bundle will help you create distributed application bundle(DAB) files from your `docker-compose.yml`, and stacks(containers and services) can be created from that bundle.

---
### Post 3: Minimal guide on Reverse proxy Using different reverse proxies - Caddy, nginx-proxy & Traefik
- Score: 171, Comments: 19
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/gkyvke/minimal_guide_on_reverse_proxy_using_different/
- Body: ##EDIT: Added HAProxy!

# Introduction

I personally love to use anologies or have a side by side comparison among different tools that tackle the same thing, so I came up with this little guide to get the ball rolling for everyone. **Each reverse proxy example resolves the exact same domain, subdomain and even subpath.** New users can easily dive into reverse proxy with the simple Caddy wheareas users that are more familiar with Nginx can opt for nginx-proxy instead. Users that are looking to move from Caddy or nginx-proxy to Traefik can also have a decent one-to-one mapping so they can understand what are the terms/components used in Traefik that means the same for Caddy or Nginx.

Often times Traefik will be the go-to recommendation whenever a question about reverse proxy is raised in this sub and it is no doubt a very feature-rich reverse proxy compared to others, but I do personally think there is nothing wrong in going with a simpler one like Caddy for smaller setups. I believe it can be a great starting point to wrap their head around reverse proxies. Once they are comfortable with it, they can then move on to Traefik to fit their more robust needs with hopefully a lesser learning curve.

I do implore new users to do some googling & research to find out the benefits of reverse proxies. I had to choose not to cover it for simplicity sake (though I'm already 3 paragraphs in now...).

# Disclaimer

**This MINIMAL guide will not be covering HTTPS or TLS certs.** Since we w

#### Top Comments:

**Comment 1** (score: 8): Excellent work!

Now add the most performant and minimal reverse proxy to your guide... HAProxy. 😎

**Comment 2** (score: 5): This is REALLY awesome! But I had to let out a laugh after reading the title "Minimal guide", and then scrolling, and scrolling, and scrolling :D

**Comment 3** (score: 3): [deleted]

**Comment 4** (score: 6): Just in time ! I was searching a clear comparison of them. Thanks

**Comment 5** (score: 5): You commented on something similar today or yesterday which was also fantastic, thank you for being so helpful! The part about using different compose files has baffled me for a while as I could never get them to join my already made proxy network! Thank you

---
### Post 4: [For Docker beginners] I've prepared material for learning Docker basics, organized in 3 real real life scenarios - Interactive, step by step, suitable if you don't want to be pointed to a bunch of documentation links in your first steps
- Score: 166, Comments: 37
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/gvb964/for_docker_beginners_ive_prepared_material_for/
- Body: Let me be clear, documentation is important, and it will come later for sure.

To see if I'm targeting the right people, check if you agree with the following: Usually if you ask someone how to do X, they throw you pile of links, and you don't even know where to start. You spend some time browsing all the documentation and you made 0 progress (or some progress in wrong direction).

So, this is the kind of self-teaching material where you need your laptop and some free time. Let's say 2 hours. It's organized in 3 scenarios so you don't have to do it all at once.

While executing commands, we'll cover some introduction topics, but also some not so basic docker concepts, but explained in the same level. Just enough how much you need, if you want to learn more, you'll get good fundamentals.

\- Setting up postgres DB server, pgAdmin, having everything setup so you can play with psql without installing it.

\- Setting up nginx server with custom html, mounting volumes, will the content survive container recreation etc

\- Creating your own Dockerfiles and introduction to the docker layer caching, creating image that you can ship to others to see what you've built

**Main takeaways after finishing the course**

\- become confident executing docker commands in front of your colleagues

\- truly understand 90% of every day commands that you see in your project (not just copy paste them)

\- have a general impression what you can achieve with docker

\- learn how you can ship your app

#### Top Comments:

**Comment 1** (score: 3): Thank you! I am just getting interested in containerized apps.

**Comment 2** (score: 3): I just finished the tutorial. I think it gave a nice quick view of a broad (enough) set of features and commands.

One thing though - in the section where you talk about the Dockerfile, you mention that the command 'RUN apt-get update' will give an up to date system.  
While it serves as a good example to what you explain later on, it is not correct that 'apt-get update' updates your system. It will only download the latest list of available packages.  It is the upgrade command that actually upd

**Comment 3** (score: 2): Thank you, man, will take a look

**Comment 4** (score: 2): Yes!!! I totally dig this and I've been super interested in what else I can pull/make into a container app

**Comment 5** (score: 2): Thank you for this

---
### Post 5: TIL that you declaring version in docker-compose has been deprecated.
- Score: 144, Comments: 28
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/ny4syf/til_that_you_declaring_version_in_dockercompose/
- Body: [link](https://nickjanetakis.com/blog/docker-tip-51-which-docker-compose-api-version-should-you-use) where i read it

>Update in 2021: The new Docker Compose spec supports not defining a version property and is the recommended way to go moving forward. It supports both v2 and v3 properties.

#

>The Compose file is a YAML file defining version (DEPRECATED), services (REQUIRED), networks, volumes, configs and secrets.

#### Top Comments:

**Comment 1** (score: 18): Does it support v2 and v3 properties at the same time?

**Comment 2** (score: 16): At first I was upset but now that I’ve read the link, I like it. I don’t need to make sure the version is correct for the properties I’m setting. Cool.

**Comment 3** (score: 12): It's a shame that swarm and non-swarm things aren't inter-compatible yet from what I can see.

I want secrets already dammit!

**Comment 4** (score: 6): ha. interesting. so but then does this imply we should be using relatively knew version of docker-compose that knows about this?

**Comment 5** (score: 3): Hey, thanks for linking one of my blog posts.

That topic was also one of the first things I covered in my DockerCon 21 talk around best practices using Docker Compose. That post / video is at: https://nickjanetakis.com/blog/best-practices-around-production-ready-web-apps-with-docker-compose

---
### Post 6: Does anyone actually think Docker is easy/simple? NOTHING I do in Docker works without a struggle.
- Score: 132, Comments: 84
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/797rwg/does_anyone_actually_think_docker_is_easysimple/
- Body: I'm sorry... I'm really sorry for being so whiny. I just have to vent. Docker has kicked my ass and made me feel like a know-nothing noob. I am completely overwhelmed by even the "simple" stuff...I'm literally wasting my life trying to figure out how to use this piece of shit.

Edit: I'm trying to connect phpmyadmin, and mysql: https://paste.pound-python.org/show/4WsRXmqdmNxPzRvrOGeh/

There's been a couple "DOH" moments... where I figured it out over something stupid. Like when I tried to start a Laravel framework using the Bitnami image, and I simply forgot to start the server via the $ docker exec container php artisan serve...

But I can't get ANYTHING to work without some serious Google searching for errors.

A lot of times, I'm like "okay... I'll check the logs... So I check every single containers logs, and There's nothing to be found that helps me solve the error. Maybe I just lack the necessary knowledge of networking to actually use Docker. But... for something that claims to be "simple"... It's really freaking difficult.


I guess I should provide at least ONE example, but... I just had a huge explanation of why I couldn't connect phpmyadmin to Mysql and it turned out to be I needed to set the PMA_HOST environment variable to the name of the mysql container. But it seems like everything I do in Docker has some sort of ridiculous problem. (Maybe I'm the problem...)

Now when I try to get PHPMyadmin connected to Mysql using docker-compose.. I'm getting some garbage a

#### Top Comments:

**Comment 1** (score: 21): One good thing is that their documentation is IMO very good. Dockerfile reference, run reference, etc. been using it for about 3 years but I go through those pages pretty frequently.

**Comment 2** (score: 14): Can we start with what were you trying to do? Maybe we can help you solve it

**Comment 3** (score: 5): No you're right. DOCKER FUCKING SUCKS. Especially on Mac. Fucking useless shit barely runs and I keep getting 'docker engine stopped' errors. It's absolutely dreadful, even in 2023 going into '24. We need a new alternative.

**Comment 4** (score: 5): Docker is complicated and the documentation is a typical example of documentation by a programmer not by a user.

**Comment 5** (score: 5): Well. To be honest it is quite unnecessary complicated for easy tasks. If you want to develop something, quickly deploy it for testing - avoid Docker for sure.

---
### Post 7: Docker for development, why, and how?
- Score: 122, Comments: 19
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/982cag/docker_for_development_why_and_how/
- Body: # Docker for development, why? and how?

Docker is one of the most used tools in the DevOps world. It is considered the de facto containerization application. However, it might be a little vague for newcomers what Docker is exactly used for. To some junior DevOps engineers, they might not see a big difference between a Docker container and a virtual machine (perhaps a Vagrant one). And, more importantly, why not just use a configuration management application (which is another DevOps tool) to do the job? So, to let's be all on the same page and read along.

# The problem

Any invention or technology must address a certain problem or pain point. Even in non-tech circles, you'll always learn that your product must solve a problem or a pain point. So, what does Docker solve here?

Let's say you're a developer working on a NodeJS web application. Throughout coding the app, you come to install some dependencies. NodeJS uses a tool called `npm` to make dependency satisfaction easier. You just keep a file called `package.json` in the root directory of the app, where you add all the libraries and modules that your software will need, and then run `npm install.` Now all is good. But, what about NodeJS itself? it must be installed first, right? here is where the problem starts to arise. Which version of NodeJS was this app built against? Although NodeJS is very generous when it comes to the platform where is can run, but sometimes, a specific version needs a specific OS and, more impor

#### Top Comments:

**Comment 1** (score: 33): Full disclosure: I only skimmed your article; it looks great and will read it in full later.

I’m a web dev and sysops guy for nearly 30 years. Docker has absolutely revolutionized local laptop development for me. 

It’s hard to explain how amazing Docker is to someone who has grown up in the virtualization era. But when you’ve been in IT for as long as I have, you remember what it was like to get your CEO and CFO to understand why you’re submitting a $25,000 proposal and a 3 month timeline as t

**Comment 2** (score: 19): You did a good job of expressing *why* you might want to use Docker for development but you did not really tell us *how*. Where do we put our code? Should it be inside the container or outside the container on a shared volume? You didn't tell us. Are you suggesting that people should use an Ubuntu container and manually install all of their software in that? Or should we start with a Python or Node.js container? We don't know, you didn't show us an example. Do we do our development work from ins

**Comment 3** (score: 12): >You application runs only on Windows or macOS. Till the time of this writing, Docker can only be used to containerize applications that run on Linux kernel. This means that you cannot convert a native Windows or macOS application and run it elsewhere. You can, however, run a Linux container on Linux, Windows, or macOS.

Incorrect. Microsoft provides a number of Windows based images (e.g. [https://hub.docker.com/r/microsoft/dotnet-framework/](https://hub.docker.com/r/microsoft/dotnet-framework/)

**Comment 4** (score: 2): As a developer who went from working on a desktop app that used our company's API to getting thrown onto a project to containerize said API, thank you for this post. You really did a good job explaining things in my opinion. This article helped clear up some things for me that have been a major sticking point. The only thing I would say is that a longer discussion of how Kuberneties (or docker swarm, or whatever orchestration you use), Docker, and Chef/Ansible/Puppet/etc. are used in tandem or r

**Comment 5** (score: 2): Very well written. 

---
### Post 8: Docker for Mac - near-native filesystem caching performance coming soon!
- Score: 117, Comments: 24
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/grtar3/docker_for_mac_nearnative_filesystem_caching/
- Body: I'm finally sold on the new caching implementation in Docker for Mac, currently available in some Edge builds; [details here](https://github.com/docker/for-mac/issues/1592#issuecomment-634960996). If you've been put off by `osxfs` slowness or the complexity of using NFS for Docker volumes on macOS, this should be a huge improvement.

There are still some bugs to iron out (like having to enable it in the UI, who does that? I didn't even realize Docker for Mac had a running container dashboard UI until last week...), but it's extremely promising!

#### Top Comments:

**Comment 1** (score: 16): Is HyperKit back to not running at 100% cpu at all times?  Hard to care about the file system when it won’t run anything at all on my system right now

**Comment 2** (score: 4): [deleted]

**Comment 3** (score: 4): Oh that's wonderful to hear. Coincidentally I bit the bullet this past weekend spending a few hours setting up a docker-compose environment working with [docker-sync](http://docker-sync.io/). The performance difference was absolutely night and day! Unfortunately there were so many hitches and roadblocks with permissions and sync consistency that I'll just wait for this.

**Comment 4** (score: 8): Thanks for sharing, this has been a huge pain point for me. I just recently started running my rails app on metal instead of in the container to avoid the slowness during development.

**Comment 5** (score: 2): I’ve been using mutagen for over a year now and it was great. Nice to see that the official support will allow me to reduce some boilerplate required to set it up

---
### Post 9: Servarr : One docker compose file to rule them all (Jellyfin, radarr, sonarr, firefox, duplicati...)
- Score: 114, Comments: 90
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/14lbvth/servarr_one_docker_compose_file_to_rule_them_all/
- Body: Hi everybody,

I wanna share with you my one Docker Compose file that I use to spin up (update, maintain...) all of my media file including these services :

* Jellyfin : media streaming service
* Jellyseerr (a fork of Overserr)
* Prowlarr
* Bazarr
* Radarr
* Sonarr
* Flaresolverr
* Qbittorrent
* Readarr
* Firefox (yes, the browser)
* Duplicati (for configuring automated backups - local or in the cloud)

In this post, I will not explaining how any of it works really, but only how I maintain them via docker (compose), we will be discussing :

* Docker compose networking
* Folders and files structures

What we will NOT be discussing : piracy, hardware acceleration, Duplicati...

As prerequisite, please do not this is my setup :

* Path to docker configs : /home/myname/docker :
   * docker-compose.yml
   * /configs
      * /duplicati
      * /jellyfin
      * /firefox
      * /mediarr/bazarr
      * /mediarr/jellyseerr
      * /mediarr/prowlarr
      * /mediarr/qbittorrent
      * /mediarr/radarr
      * /mediarr/readarr
      * /mediarr/sonarr
* Path to media files (mounted from NAS via NFS v4) : /mnt/media
* Path to "external" hard drive for all my downloads : /mnt/HDD/downloads
* Path to graphics card (it's an iGPU) : /dev/dri/renderD128
* My render group ID : 109
* Networking :
   * Jellyfin is connected directly to the HOST (for DLNA)
   * Bridge "firefox" for firefox
   * Bridge "duplicati" for duplicati
   * Bridge mediarr for everything else (these services communicate a

#### Top Comments:

**Comment 1** (score: 26): Now add a top level VPN to tuck some of those behind while maintaining cross app communications per normal. 👍

I'll share mine tonight if anyone wants. But it's purely "servarr" apps, no streaming because those are independent, not needed but they are.

(Edit) No  additional details, just raw unabridged YAML (as it presently is on my servarr)  
https://pastebin.com/GVu2L5ia

**Comment 2** (score: 11): I'll point out that YAML Anchors are a thing and help reduce duplication. 

There's examples here: https://docs.docker.com/compose/compose-file/10-fragments/


I think this should do the trick: 

    ---
    version: 2.1
    
    # Setup default propreties we want on all/most containers
    x-default-container &default-container:
      user: 1000:1000
      group_add: 
        - "109"
      environment:
        - PUID=1000 
        - PGID=100 
        - TZ=Africa/Casablanca 
      restart: unles

**Comment 3** (score: 8): some common mistakes are appearing in here. 

Sonarr has these volumes:

    volumes: 
      - ./configs/mediarr/sonarr:/config 
      - myMedia:/mnt/media 
      - myDlFolders:/mnt/downloads 

whereas qbit has these volumes:

    volumes: 
      - ./configs/mediarr/qbittorrent:/config 
      - myDlFolders:/downloads 

that means that:

1. you need a remote path mapping in sonarr to change `/downloads` to `/mnt/downloads` - whereas you'd be better being consistant and mounting
this to qbit: `   

**Comment 4** (score: 3): You should/could use fragments and extensions to shorten the compose file. This would also allow cascading changes without worrying about missing a container (eg. Changing your uid from 1000 to 999 in the fragment means all things using that fragment now have uid=999).

You could also create docker volumes and reference that instead of creating it within the compose.

On Flaresolverr, unless you're actually setting variables in the .env, you can remove the "${question:-answer}" with just "answer

**Comment 5** (score: 4): You should paste your compose in like paste bin or something

---
### Post 10: Free Course on Docker for Beginners, Learn The Basics of Docker Networking, Complete Docker Container Overview, Learn How to Install Docker on Ubuntu and CentOS, Docker Volumes and Storage Explained, Create Docker Swarm Cluster Step by Step,
- Score: 112, Comments: 5
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/iotixa/free_course_on_docker_for_beginners_learn_the/
- Body: Please find the complete 5-part tutorial series in this [**playlist**](https://www.youtube.com/playlist?list=PLlEyMvUZ31GDw2G2g3GgXdH0AMGsR37BX). I hope you are going to enjoy it. Please share your thoughts /comments on this.

#### Top Comments:

**Comment 1** (score: 3): Saved for later! Thanks!

**Comment 2** (score: 1): Thank you.

**Comment 3** (score: 1): Saved. Thanks! Interested in the swarm video, though I am in Podman these days. Cheers!

**Comment 4** (score: 1): Here's a [5-hour Docker course from Edureka](https://youtu.be/RSIstPUiEjY)

---
