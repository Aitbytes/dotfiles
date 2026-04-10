# Reddit Data - docker

## Collected Posts and Comments

### Post 1: New to Docker – best way to learn? Need Linux first?
- Score: 18, Comments: 31
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/1r1zyu3/new_to_docker_best_way_to_learn_need_linux_first/
- Body: Hey all,

I’m just starting with Docker and want to learn it properly and professionally (not just copy-paste configs).

  
Couple quick Qs:

* Best resources? (YT, courses, docs, etc.)
* Do I need solid Linux basics first?
* How deep should I go into networking/sys concepts?
* Any good hands-on project ideas?

Main goal is using it for real-world web apps.

  
Appreciate any recs 🙌

#### Top Comments:

**Comment 1** (score: 17): Learn Linux first, then build on top of that.

**Comment 2** (score: 5): Honestly. Best thing to do is to memorise the cli and also just memorise how compose files work

**Comment 3** (score: 3): You need basic Linux skills. Then, they have a tutorial on their website in the docs.

**Comment 4** (score: 2): do u plan on actually hosting ur apps urself or just using it for dev? tbh u dont need to be a linux wizard but knowing basic bash and file permissions is a life saver. best way to learn is just trying to dockerize a simple api with a postgres database. figuring out why the connection fails the first time is where u actually learn how the networking works lol

**Comment 5** (score: 1): The thing that I am learning is that the docker desktop program will work in windows, mac, and Linux of course ... And the container basically inherits the OS of the computer you're using which would most likely be windows or Linux. 

How familiar are you with command line interfaces (CLI)?

Having messed around in MS-DOS 25 years ago I'm sort of familiar with CLI. It took me a second to understand what sudo and ls are doing. But honestly I feel pretty comfortable with screwing around on a Linux

---
### Post 2: We just got breached because of vulnerabilities in our docker images that have been public knowledge for 8 months
- Score: 728, Comments: 90
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/1ru2xsk/we_just_got_breached_because_of_vulnerabilities/
- Body: Woke up at 4am to a call. Our database got hit, customer info was accessed. Some attacker used a known exploit in one of our container images. CVE’s been out since last summer.

Yeah we never scanned. Never updated. Just kept redeploying the same images over and over. Now legal’s in it, customers are hearing about it. This is gonna be messy.

Honestly if you aren’t scanning your containers in prod do it. Don’t end up like us.



#### Top Comments:

**Comment 1** (score: 113): Yeah so honestly you kinda gotta hit this on two fronts. First like the first 48 hours scan all your prod containers with whatever free stuff you can grab trivy grype anchore whatever. Make a list of CVEs that actually have exploits check cisa gov or KEV. Patch or swap anything getting actively used even if it breaks some stuff. Keep track of what you did somewhere.

Then over the next couple weeks rebuild images off updated bases. Stop rolling with latest tags pin versions instead. Add vuln sca

**Comment 2** (score: 66): One time when I worked for a Hospital System, I got a shitty call at 2 AM... It was not for a data breach or an exploit, it was because a sewage pipe bust open and was filling our server room with poop water. 

**Comment 3** (score: 34): [removed]

**Comment 4** (score: 12): What was your architecture like? Most CVEs wont be exploitable on most well architected systems. Otherwise /u/FunAd6672 hits most of the main points, you can catch most of this stuff in CICD if its being deployed relatively frequently. Just make sure you catch anything that doesnt get deployed super often and look around for the near 0 CVE base images if you can

**Comment 5** (score: 12): Are your containers exposed directly to the world? Any gateway or WAF out front? If so, how did they get at the containers?

---
### Post 3: Docker banned - how common is this?
- Score: 522, Comments: 191
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/1owvigi/docker_banned_how_common_is_this/
- Body: I was doing some client work recently. They're a bank, where most of their engineering is offshored one of the big offshore companies.

The offshore team had to access everything via virtual desktops, and one of the restrictions was no virtualisation within the virtual desktop - so tooling like Docker was banned.

I was really surprsied to see modern JVM development going on, without access to things like TestContainers, LocalStack, or Docker at all.

To compound matters, they had a single shared dev env, (for cost reasons), so the team were constantly breaking each others stuff.

How common is this? Also, curious what kinds of workarounds people are using?



#### Top Comments:

**Comment 1** (score: 260): It’s more common then you think… last three finance companies I have been at are not doing docker or anything

**Comment 2** (score: 111): Yep. When I worked at one of Australia’s “big 4” banks, no docker. It was extremely frustrating as every dev machine setup could have been streamlined. I tried to fight for it, but no luck.

**Comment 3** (score: 34): I'm a security guy and the designated docker person for my team

Banks and financial institution are held to high standards and must audit very often

Whenever you get audited and you use docker it will come up on the report and the guy who manages it (you) will need to prove to the designated docker guy of the audit team (me) that the implementation of every single image you use is immune to breakouts

Save us both a load of time and run your OCI images on podman

In a normal environment breako

**Comment 4** (score: 32): Pretty common for banks. Even at NASA docker is not allowed. Only Podman. For self hosting stuff, a simple docker/podman compose up and I'm done. But in prod, and especially for a bank, I wouldn't even mention the word docker lol.

**Comment 5** (score: 90): Just google “Docker Security Concerns”.

---
### Post 4: Docker isn’t magic — it’s just Linux. I traced how containerd, runc, namespaces & cgroups make it all work
- Score: 736, Comments: 86
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/1nx7u37/docker_isnt_magic_its_just_linux_i_traced_how/
- Body: Big thanks to the mods for letting me share this! 🙌 you guys are OG!!!

Most tutorials show you how to use Docker… but very few explain what happens behind the scenes when you type docker run.

In this tutorial I break it down step by step:
	•How regular binaries turn into images
	•How Docker delegates to containerd & then to runc
	•How namespaces & cgroups actually isolate processes

If you’ve always used Docker but never peeked under the hood, this will connect the dots.

Docker Containers Are Just Linux?
https://youtu.be/l7BjhysbXf8


#### Top Comments:

**Comment 1** (score: 66): Some of us remember chroot jails :)

**Comment 2** (score: 139): Never done a real under the hood peek. But the realization that containers are just linux made my entire life so much easier.

**Comment 3** (score: 27): (Still) relevant oldie but goodie, if you wish to be more hands-on: [https://github.com/p8952/bocker](https://github.com/p8952/bocker)

**Comment 4** (score: 19): Dammit, I'm not even 40 yet and y'all making me feel old.. I thought this was common knowledge and really well documented so a bit surprised by someone needing to trace it. Maybe that's just a different way of learning it but docker is super well documented it

**Comment 5** (score: 12): Cool, I’ll give it a look. Containers were how I started becoming familiar with Linux and eventually became comfortable enough to set up Proxmox and run full Linux VMs for my containerized services. 

Containers have probably done more for Linux popularity than almost anything else, since so many small and large projects get distributed like this.

---
### Post 5: Why Is Nobody Talking About Docker Swarm?
- Score: 227, Comments: 169
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/1m3swyh/why_is_nobody_talking_about_docker_swarm/
- Body: I just set up my first Docker Swarm cluster. I might sound like I'm from another planet, but something this brilliantly simple that just works - I can't believe I didn't try it sooner. Why does it get so little attention? What's your production experience with it?

#### Top Comments:

**Comment 1** (score: 525): Nobody talks about swarm because Kubernetes won the production workload orchestration game years ago.

**Comment 2** (score: 36): What is *your* use case? 

I'll tell you from my own experience, running from a multi-node, multi-cluster homelab environment that emulates my production workload, Swarm appeared like a solid option -- I didn't need Kubernetes... Until I realized the gap between Swarm and Kubernetes -- a solution I'd ruled out as a homelab environment seemed like the wrong place for that complex of an orchestration tool -- was small, while the margin between features, QoL, community support, and developer/devops

**Comment 3** (score: 102): The original swarm was deprecated. So I guess most people moved to mainly Kubernetes. I had no idea until just now Swarm still existed.

**Comment 4** (score: 23): We use swarm mode for our 3-5 server clusters. Handles everything we need while being minimal complexity- if you can write a docker compose file you are 90% of the way there.  1 and a half person shop on the devops side and just finished migrating the last of the vm based apps over.  It’s been solid so far.  
Previous gig had a k8s cluster and 5 guys to keep it running.  Our needs just aren’t that high for the potential payoff.

**Comment 5** (score: 13): Docker swarm is still great for small clusters with minimal overhead. I use it over kubernetes for personal few node clusters as it’s a lot lot less hassle to setup than kubenetes, so if all you need is high availability and running a few containers like dbs and web apps it’s perfect

---
### Post 6: Need advice: how to hide Python code which is inside a Docker container?
- Score: 65, Comments: 101
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/1qoqs89/need_advice_how_to_hide_python_code_which_is/
- Body: We deploy robots in manufacturing companies, and hence need to run code on-premise as low latency, lack of internet and safety are concerns.

Our code is in Python and containerised in Docker. It’s basically a server with endpoints. We want to ensure that the Python code is not visible to the client to protect intellectual property.

We need the users to launch the Docker images without seeing the code inside. Once launched, they can interact with endpoint.

Is there a way to ensure that the user cannot see the Python code inside the Docker container? 

#### Top Comments:

**Comment 1** (score: 121): You can't. You could compile to an exe and run in the container but someone with technical skill could reverse it.


The only sure way to protect it is a client-server separation where the server holds your IP and is not on site. 

**Comment 2** (score: 37): Are you shipping the containers to a company in a country that doesn't enforce international copyright? Otherwise I wouldn't worry about it. I've worked for a couple and consulted for more B2B startups - none of them really worried about obfuscating the code in docker images. Your legal team should have pretty strict NDA wording in the contract regarding your IP.

Even if the code does leak, would that be a big deal? For 99% of software companies - no. Folks aren't typically out there running pi

**Comment 3** (score: 18): Oh, forgot one thing: If you need on-prem, the easiest solution could be to use put one of your own servers managed by your company but located in client datacenter. It's costly because that's a lot of system administration to do if you have a lot of clients, but depending on the situation that can do the trick and be cheaper than other solutions.

That's basically what big companies that run proprietary sensitive stuff on prem do. When I was working for a banking company, they had Google (for g

**Comment 4** (score: 36): **Edit**: I forgot to mention the good old physical security (see [https://www.reddit.com/r/docker/comments/1qoqs89/comment/o23ftwj/?context=3](https://www.reddit.com/r/docker/comments/1qoqs89/comment/o23ftwj/?context=3) )

If your containers runs on servers owned by the client, the only thing you can do is obfuscating your app.

Either something soft, like compiling it in C code so they need one skilled reverse engineer to understand the code, or something stronger using a real obfuscator, so t

**Comment 5** (score: 8): Nuitka: [https://github.com/Nuitka/Nuitka](https://github.com/Nuitka/Nuitka)

---
### Post 7: How I Reduced Docker Image Size from 588 MB to Only 47.7 MB - A whomping 91.89 %
- Score: 675, Comments: 104
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/1f1wqnb/how_i_reduced_docker_image_size_from_588_mb_to/
- Body: To begin with, there is no secret here if you already know about the multi stage builds.

We all know minimizing docker image sizes accelerates container deployment, and for large-scale operations, this can lead to substantial savings in storage space.

1. For a flask app, I picked up **Python 3.9-alpine which is a whomping 95.2% smaller than Python 3.9**

This minimal images contain **only the essentials**, significantly reducing the image size.

2. I minimized layers - every command in a Dockerfile (like `RUN`, `COPY`, etc.) generates a separate layer in the final image. Grouping similar commands together into one step makes sense, which decreases the total number of layers, leading to a smaller overall image size.

**Instead of doing this:**

    RUN apk update
    RUN apk add --no-cache git
    RUN rm -rf /var/cache/apk/RUN apk update
    RUN apk add --no-cache git
    RUN rm -rf /var/cache/apk/*  *

**Do this:**

    RUN apk update && apk add --no-cache git && rm -rf /var/cache/apk/*

3. Used .dockerignore File - Docker transfers all the files from your project directory into the image by default. To avoid including unneeded files, used a `.dockerignore` file to exclude them.

    __pycache__
    *.pyc
    *.pyo
    *.pyd
    venv/

4. Multi-Stage Builds - Here all the magic happens !

**Single Stage Vs Multi-Stage Builds Comparison:**

Take an example of a Flask app built using the `python:3.9-alpine` image with a **single-stage Dockerfile** like:

    # Use an official

#### Top Comments:

**Comment 1** (score: 83): (From the Docker DevRel team)

Just saying... congrats and whale done! Funny enough, this is some of the most common content we get asked to present on when interacting with customers. And, you covered most of the best practices we talk about. Folks want smaller images and faster builds!

You're already doing it, but the only other thing I'd call out is to be mindful of the _order_ of the commands to help speed up builds. You're copying in the `requirements.txt` file and then installing the Pyth

**Comment 2** (score: 65): Just use `dive` to examine your layers and look for stuff that's being captured along the way but isn't needed in the final image for your app to run, that's what this all pretty much boils down to: https://github.com/wagoodman/dive

Edit: and I mentioned this in another comment—number of layers doesn't really matter at all and more layers can be good if it increases reuse of cached lower layers between builds. 

The advantage of consolidating layers is to remove everything you can that was adde

**Comment 3** (score: 40): ```
# Copy the requirements file and install dependencies
COPY requirements.txt ./

# Copy the rest of the application code to the working directory
COPY . .

RUN <<EOR
pip install --no-cache-dir -r requirements.txt

# Uninstall unnecessary dependencies
pip uninstall -y pandas && apk del build-base gfortran musl-dev lapack-dev
EOR
```

Why were you uninstalling things in a separate layer? That will leave the files in the docker image still, reduce the size by doing it in the same layer.

**Comment 4** (score: 15): Why did you install pandas in the first place if it's unnecessary?

**Comment 5** (score: 12): Great post! Just because some may know this already doesn’t take away from the benefit of those who didn’t. I’ve been using docker for years and can DEFINITELY benefit from shrinking my images, thanks for sharing!

---
### Post 8: Docker just made hardened container images free and open source
- Score: 422, Comments: 38
- Subreddit: r/docker
- URL: https://reddit.com/r/docker/comments/1poxrss/docker_just_made_hardened_container_images_free/
- Body: Hey folks,

Docker just made **Docker Hardened Images (DHI)** free and open source for everyone.  
Blog: [https://www.docker.com/blog/a-safer-container-ecosystem-with-docker-free-docker-hardened-images/](https:)

Why this matters:

* Secure, minimal **production-ready base images**
* Built on **Alpine & Debian**
* **SBOM + SLSA Level 3 provenance**
* No hidden CVEs, fully transparent
* Apache 2.0, no licensing surprises

This means, that one can start with a hardened base image by default instead of rolling your own or trusting opaque vendor images. Paid tiers still exist for strict SLAs, FIPS/STIG, and long-term patching, but the core images are free for all devs.

Feels like a big step toward making **secure-by-default containers** the norm.

Anyone planning to switch their base images to DHI? Would love to know your opinions!

#### Top Comments:

**Comment 1** (score: 34): [deleted]

**Comment 2** (score: 19): How do I use them without logging in to see what's available?

**Comment 3** (score: 10): We are currently using Debian 13 distroless as base image. We copy some Debian .so dependencies over from the build image. Can someone explain the advantages we would have from using these docker hardened images?

**Comment 4** (score: 8): > SBOM + SLSA Level 3 provenance

OK, but what does this mean? They don't even say in the blog post.

**Comment 5** (score: 2): Waiting to find out what’s the trap about it…

---
