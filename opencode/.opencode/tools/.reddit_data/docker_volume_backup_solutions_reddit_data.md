# Reddit Data - docker volume backup solutions

## Collected Posts and Comments

### Post 1: How do redditors do off-site backup?
- Score: 14, Comments: 60
- Subreddit: r/AskReddit
- URL: https://reddit.com/r/AskReddit/comments/aiasp/how_do_redditors_do_offsite_backup/
- Body: With pretty much every belonging I care about at this point being in digital bit form, I figure I really should start getting off-site backups to be part of my backup story. What's the best way these days to back up about 3TB?

For what it's worth, here's the setup I have so far:

* All my Dreamhost files (in LA) get rsynced to a hard disk A at home, connected to a Mac mini.

* All my media (music and TV shows from iTunes) is on a 1TB Drobo B at home, on that Mac mini.

* The Mac mini has internal disk with data C.

* My partner has data D on a laptop.

* The data on A, B, C, and D all get backed up to a second Drobo on that Mac mini using Time Machine.

Unfortunately, with the exception of the data from Dreamhost, that means that all the copies of the data are nicely and redundantly backed up with in about a 1m³ volume of space, in an earthquake zone.

I've had really bad luck with hard disks. I literally have about 2TB of dead hard disks sitting in a box somewhere here. That's why I'm now using Drobos — at least I'm protected against disk deaths. So I'm not willing to back up to disk — I wouldn't trust it.

I've considered burning DVDs or even BluRays, but both simply make backing up 3TB impractical — even BluRay's maximum capacity seems to be only about 400GB per disk. Ideally I'd like to at least semi-automate this, and having to switch disks every few hours when making a backup is rather suboptimal.

I've considered networked off-site backup like Carbonite (which doesn't

#### Top Comments:

**Comment 1** (score: 3): Choose a friend or family member you implicitly trust that has a good internet connection, and lives far enough away any natural disaster that hits you isn't likely to hit them.  Chances are they will not have an offsite backup plan.  Offer to fully back them up offsite if they let you keep a machine and drives at their place.  (If backing up is completely unimportant to them, maybe offer to pay half or all of their internet connection?)  


This offers the same price as you'd pay for local stor

**Comment 2** (score: 2): I hear mozy can protect you from falling [appliances](http://www.youtube.com/watch?v=w_F_6xOlke0)

**Comment 3** (score: 2): S3 is cheap, use it with duplicity for encryption.

rsync.net is more expensive, but you can count on it being sent to multiple data centers that are geographically separated. 

you could probably rig something like that up using the new n. california or ireland s3 availability zones, but rsync.net is automatic. 

i used to use rsync.net until i had too much data for it to be cost effective. now i use duplicity + s3. i have just shy of 100g encrypted on s3, which makes for about a $14/mo bill.

**Comment 4** (score: 2): [deleted]

**Comment 5** (score: 1): Buy a VPS an do frequent backups to it. That's pretty easy.

---
