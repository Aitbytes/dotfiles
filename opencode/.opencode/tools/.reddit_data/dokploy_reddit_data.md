# Reddit Data - Dokploy

## Collected Posts and Comments

### Post 1: One script to secure your VPS and deploy Dokploy - open source, feedback welcome
- Score: 42, Comments: 2
- Subreddit: r/dokploy
- URL: https://reddit.com/r/dokploy/comments/1rstqcg/one_script_to_secure_your_vps_and_deploy_dokploy/
- Body: I got tired of spending hours manually securing every new VPS, so I built a script that does it all in \~10 minutes. It takes a bare Ubuntu 24.04 server through 9 interactive steps — SSH hardening, firewall, Fail2Ban, kernel tuning, Docker, and Dokploy deployment. No config files, just guided prompts. Claude Code helped me write and refine the whole thing. Feedback welcome!

GitHub: [https://github.com/alexandreravelli/vps-ubuntu-24-04-hardening-dokploy](https://github.com/alexandreravelli/vps-ubuntu-24-04-hardening-dokploy)

#### Top Comments:

**Comment 1** (score: 2): good job

**Comment 2** (score: 2): Great work, thank you. 

---
### Post 2: Monero Miner found
- Score: 20, Comments: 26
- Subreddit: r/dokploy
- URL: https://reddit.com/r/dokploy/comments/1pfbgoa/monero_miner_found/
- Body: I got an email today from my VPS (Hostinger) that they found a monero miner in one of my Docker containers. It looks like it was in a NextJS-starter container that contained nothing but React and NextJS that I forked a while back and deployed as a test, but the miner seems very recent. I’m trying to understand how this happened. I’m assuming the React/Next dependency chain wasn’t poisoned? Has anyone else seen this? Is there a chance it was some sort of drive-by malware install of some sort? I’m not understanding how that would have occurred.

#### Top Comments:

**Comment 1** (score: 2): https://preview.redd.it/z6rafi76bh5g1.jpeg?width=1179&format=pjpg&auto=webp&s=442d0d4c3ead02229b6595551a21f4eca6334e5d

This is my entire package.json for that container, and hostinger found xmrig at this path (which seemed to be inside this container):

/var/lib/docker/overlay2/e637ec2731cf2e d08c3c97a279091aefe82b40d7ccfdOd4 36a70c6c17c255466/diff/root/c3pool/xmrig

**Comment 2** (score: 2): This is scary tbh. 
I have no idea how to help you, but good luck fixing it and I hope you make an update.

**Comment 3** (score: 2): [deleted]

**Comment 4** (score: 2): Nextjs exploit, zero-day. Upgrade your nextjs then.

**Comment 5** (score: 2): There's a new NextJS vulnerability that is being used to execute remote code on lots of machines with vulnerable nextjs installations. Please run npm audit , you will see the critical vuln, afterwards update your install and add a WAF too your docker stack!

---
