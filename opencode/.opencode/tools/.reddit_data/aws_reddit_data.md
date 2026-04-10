# Reddit Data - aws

## Collected Posts and Comments

### Post 1: Another AWS/O365 Outage
- Score: 1000, Comments: 292
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1oj9h2i/another_awso365_outage/
- Body: Here we go again. Midwest USA here. If you look at AWS and O365 in DownDetector the outage spike is pretty much the same. Glad Amazon's stock prices are up with the most recent round of firings.... /s

#### Top Comments:

**Comment 1** (score: 997): Microsoft discovering the pain of relying upon their own support.

**Comment 2** (score: 303): Can we go home? Or do we just have to twiddle our thumbs till 5pm?

**Comment 3** (score: 195): Yeah,Azure and AWS apparently, it’s some sort of DNS issue from what I’m hearing

---
### Post 2: Moving from AWS to Bare-Metal saved us 230,000$ /yr.
- Score: 2163, Comments: 580
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/17y6zbi/moving_from_aws_to_baremetal_saved_us_230000_yr/
- Body: Another company de-clouding because of exorbitant costs. 

[https://blog.oneuptime.com/moving-from-aws-to-bare-metal/](https://blog.oneuptime.com/moving-from-aws-to-bare-metal/)

Found this interesting on HackerNews the other day and thought this would be a good one for this sub. 

#### Top Comments:

**Comment 1** (score: 1340): This is also a classic scenario where a start up needs capacity and the flexibility the cloud provides. However over time the company matures and has a much better forecast on demand and needs so they can predict onprem costs.

**Comment 2** (score: 95): I also think it is a lot about workload types. We have servers that needs to run 24/7 and we have servers that needs to be booted up, worked on for a while and then turned back off.

&nbsp;

I think that adjusting the cloud infrastructure according to needs also saves a lot of money. But obviously there would be scenarios where on-prem is favorable. However for us to stay compliant, we need to have at least 3 locations for servers and having to maintain all that infrastructure is just such a pai

**Comment 3** (score: 364): Me listening to engineering team say that a client should move 200+ VM's + 50 servers that are comprised of a 6 host cluster, to the cloud because "It'll be cheaper".

Somedays, I regret my decision to not bathe with my toaster.

---
### Post 3: If you were the AWS server guy
- Score: 591, Comments: 354
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1obqkfa/if_you_were_the_aws_server_guy/
- Body: If you were the AWS server guy after a day like today. What's the first thing you're doing when you clock out ?

#### Top Comments:

**Comment 1** (score: 1210): Chatting with the CrowdStrike guy.

**Comment 2** (score: 821): Definitely a "drive home with the radio off" day.

**Comment 3** (score: 529): Settle down and unwind with a nice relaxing game of Fortnite


Wait... 

---
### Post 4: My company wants to update 1500 unsupported devices to W11 how do I make them realize it's an awful idea
- Score: 824, Comments: 463
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1k5s97r/my_company_wants_to_update_1500_unsupported/
- Body: Most of the devices are running on 4th Gen I5s with Hard drives and no SSDs, designed for W7 running legacy boot (Although running on 10 now)

Devices are between 10-12 years old

Apparently there is no budget to get new devices and they want to be on a supported Windows version post Oct.

How do I convince them it's a bad idea? I've already mentioned someone needs to touch every devices BIOS and change it to UEFI, Microsoft could stop a unsupported upgrade in a future feature update leaving us in the same EOL situation ect.





#### Top Comments:

**Comment 1** (score: 1435): That's the neat part - you don't.


> Devices are between 10-12 years old Apparently there is no budget to get new devices


Be polite, professional. Document your concerns to include that the age of the hardware is likely already costing more in support and lost productivity than it would to simply replace them. Document that Microsoft has more than once released an update that changed workarounds. Any future update on unsupported hardware might be trouble. Lost data from failing drives, etc.



**Comment 2** (score: 406): I hate to say it OP but if they have no budget to replace old kit that's 10-12 years old the governance of your organisation is questionable to begin with. They are sweating assets, why would they care if it's on unsupported hardware if it works?

Strategically your C-Suite are muppets.

**Comment 3** (score: 59): How many hours will you be looking at to touch every device and get everything to windows 11 and perhaps stick an SSD in each for good measure?

VS

How much will it cost to get new machines, already on win 11, and plug them in? Also, depending on the old pc’s and new pc’s, will they have monitors with the right connections?

Hope you can get them to see reason and go down the new pc path.

---
### Post 5: Spent 5 hours debugging AWS Elastic Beanstalk… turns out my client just hadn’t paid the bills.
- Score: 950, Comments: 78
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1p10mv9/spent_5_hours_debugging_aws_elastic_beanstalk/
- Body: So today I learned a very important lesson about AWS:  
It won’t tell you *why* it’s ruining your life.

I’m working for a client, right?  
Simple task: **“Can you deploy this updated Node backend on EB?”**  
Cool, no problem. I’ve done this a hundred times.

Except today EB woke up and chose violence.

* Stuck at “Updating environment”
* Stuck at “No Data”
* Rebuild fails
* Auto Scaling group refuses to exist
* Logs won’t download
* Node 22 acting like it hates me
* Even a brand new environment wouldn’t launch
* EC2 keeps screaming “vCPU limit exceeded”
* Support rejects quota increase in 30 seconds flat

At this point I’m sweating thinking I corrupted their entire environment.  
I’m googling every possible error under the sun.  
I'm blaming my ZIP file, my code, my past life sins, everything.

**FOUR HOURS later…**

I open the billing section and see:

>

BRO.  
AWS basically put the entire account into **timeout mode**, silently.  
Didn’t tell me upfront.  
Didn’t show a warning in EB.  
Didn’t say “Hey genius, your client didn’t pay the bills.”  
Just let me fight ghosts for half a day.

The whole infrastructure was literally **blocked** because the client hadn’t paid MONTHS of invoices.

And here I was debugging like I broke production.

*Me:* Why won’t EC2 launch??  
*AWS:* 😐  
*Me:* Why is my quota suddenly 1 vCPU??  
*AWS:* 😐  
*Me:* Why did you reject my quota request in 0.2 seconds??  
*AWS:* 😐  
*Billing page:* “Past due: ₹23,659.”  
*Me:* OH.

Anyway, client is li

#### Top Comments:

**Comment 1** (score: 459): Don’t forget to invoice the client ;)

**Comment 2** (score: 135): Shouldn't the admin portal has a red banner on top that reminds you there are pending invoices?

**Comment 3** (score: 148): Our first step of troubleshooting at my current job is verify the vendor has been paid.

---
### Post 6: AWS Outage?
- Score: 1523, Comments: 526
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/rb226w/aws_outage/
- Body: Hi all.

Starting to see some sort of AWS outage.  Currently experiencing issues getting to the console, connecting to the KMS and Dynamo APIs.  Nothing on their status page ATM, but DownDetector is starting to report issues.

Anybody else experiencing this?

EDIT 11:35am EST: AWS finally updated their status page.

>8:22 AM PST We are investigating increased error rates for the AWS Management Console.  
>  
>8:26 AM PST We are experiencing API and console issues in the US-EAST-1 Region. We have identified root cause and we are actively working towards recovery. This issue is affecting the global console landing page, which is also hosted in US-EAST-1. Customers may be able to access region-specific consoles going to [https://.console.aws.amazon.com/](https://.console.aws.amazon.com/). So, to access the US-WEST-2 console, try [https://us-west-2.console.aws.amazon.com/](https://us-west-2.console.aws.amazon.com/)

Edit 2 9:30am EST : AWS sounded the all-clear at about 5:30am EST.  All said and done 19 hours of issues! 

&#x200B;

#### Top Comments:

**Comment 1** (score: 670): Talking to users these days I feel more like an Internet Meteorologist than a Network Administrator.

**Comment 2** (score: 449): Why do I always learn about AWS outages here first?

**Comment 3** (score: 720): The building's music relied on Amazon Music and now everything's quiet lol.

Not to worry, we'll just start using SiriusXM like the other branch uses. Oh that's hosted on AWS too.

---
### Post 7: So, you want to learn AWS? AKA, "How do I learn to be a Cloud Engineer?"
- Score: 3983, Comments: 221
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/8inzn5/so_you_want_to_learn_aws_aka_how_do_i_learn_to_be/
- Body: **Introduction**

So many people struggle with where to get started with AWS and cloud technologies in general. There is popular "[How do I learn to be a Linux admin?](https://www.reddit.com/r/linuxadmin/comments/2s924h/how_did_you_get_your_start/cnnw1ma/)" post that inspired me to write an equivalent for cloud technologies. This post serves as a guide of goals to grow from basic AWS knowledge to understanding and deploying complex architectures in an automated way. Feel free to pick up where you feel relevant based on prior experience.

Assumptions:

- You have basic-to-moderate Linux systems administration skills
- You are at least familiar with programming/scripting. You don't need to be a whiz but you should have some decent hands-on experience automating and programming.
- You are willing to dedicate the time to overcome complex issues.
- You have an [AWS Account](https://portal.aws.amazon.com/billing/signup#/start) and a marginal amount of money to spend improving your skills.

How to use this guide:

- This is not a step by step how-to guide.
- You should take each goal and "figure it out". I have hints to guide you in the right direction.
- Google is your friend. [AWS Documentation](https://aws.amazon.com/documentation/) is your friend. Stack Overflow is your friend.
- Find out and implement the "right way", not the quick way. Ok, maybe do the quick way first then refactor to the right way before moving on.
- Shut down or de-provision as much as you can between learni

#### Top Comments:

**Comment 1** (score: 508): Woah, woah, woah.

Are you trying to tell me that there's more to being a 'cloud engineer' than spewing buzzwords like the turboencabulator?

**Comment 2** (score: 154): If you don't have money to get started, this site has some free labs that let you spin up real aws resources.  
  https://qwiklabs.com/

**Comment 3** (score: 142): This would also look great somewhere on the wiki. ;D

---
### Post 8: What was your funniest moment in IT work? Let’s write down something positive, instead of reading awful tickets.
- Score: 1122, Comments: 903
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/h12x1w/what_was_your_funniest_moment_in_it_work_lets/
- Body: I have had my share of laughs here in Germany and I will share with you my favorite three:

&#x200B;

Once I got a call from a physicaltherapist: „My PC is very slow, I assume there is a bacteria on my harddisk.” I’m pretty sure you realize, she was talking about a virus.

&#x200B;

A friend of mine owned a computer store once and an old gentleman bought a printer. The next day he returned.

Elder gent: ”The printer isn’t working!”

My friend: ”Have you connected the power supply?”

Elder gent: “Yes!”

My friend: ”Have you connected the other cable to your PC?”

Elder gent: “PC? I don’t own a PC, I only want to print!”

&#x200B;

Once I visited a woman: Her PC lost the internet connection and the printer wasn’t working. When I was crawling under the office desk she said in German “Ich hatte noch nie einen Professionellen in meinem Haus.” Translation: ”I have never had a professional in my house.” I jumped up and hit my head very hard. You are asking me why?

Well, when you talk in Germany about a professional worker, we just say “Profi” or "Experte". The term “Professioneller” is only used for male sex workers.

Edit 1: Typo

Edit 2: Thanks for your great stories and your questions. I will follow up, I promise. But here the sun is set and I have to go to bed... Oh: and thank you for my first award. CU

Edit 3: I will have a lot of reading to do this weekend. Thank you! Some people were asking about the ending of the third story: I got up, holding my head and turned around. Th

#### Top Comments:

**Comment 1** (score: 654): There's been lots of funny moments but my favorite to date is probably The Fireball.  


IT Office was also the datacenter and MDF.  


One of the 15 year old switches was making a giant whine sound. You could hear that exhaust fan just grinding away. Helpdesk Tech gets up, grabs a can of air, sprays it into the switch--- right as I'm saying "hey don't do...." ---- POOF  


Fireball. Out the back of the switch. Switch is dead.  


Called him Fireball Jim for about 4 months.

**Comment 2** (score: 451): [deleted]

**Comment 3** (score: 403): Back in the day I went to power down a server and realized when the button was pushed in, it was the wrong server. This was back in the day of mechanical switches. As long as I didn't let my finger up, the server wouldn't go down.

This was for a payroll company and there were about 100 people entering data. The server going would mean many people would probably not get paid that day.

I held that button in for 45 minutes before we got everyone out and gracefully downed the server.

---
### Post 9: Huge spike in DownDetector for X, AWS, Cloudflare.
- Score: 373, Comments: 89
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1r6agfw/huge_spike_in_downdetector_for_x_aws_cloudflare/
- Body: Nothing to see here, folks. Just another day with cloud problems.

#### Top Comments:

**Comment 1** (score: 445): Oh well, I’m off today.

**Comment 2** (score: 141): Just restart DNS please. Thanks

**Comment 3** (score: 91): AWS and Cloudflare are barely 'huge' spikes. There's about 30 reports for those versus 10k for X. Nothing to see here.

---
### Post 10: AWS Outage?
- Score: 1951, Comments: 219
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/opgjk5/aws_outage/
- Body: **EDIT** : On our end we've confirmed it's anything with an Akamai cname so far.

**EDIT 2** : Akamai DNS was the problem. They appear to have fixed it. For those who know nothing about CDNs and curious at a high level how this outage worked from a client perspective here is a quick blurb https://www.reddit.com/r/sysadmin/comments/opgjk5/aws_outage/h65dj90/

Anyone experiencing issues with AWS? We have 10 AWS accounts all hosting 100+ various websites and all of them just went down and are inaccessible. Anyone else hving issues?

So far looks like possibly route 53 but don't have anything to support that.

#### Top Comments:

**Comment 1** (score: 245): [deleted]

**Comment 2** (score: 838): [deleted]

**Comment 3** (score: 73): https://downdetector.com/

Issues with Fidelity Investments, Home Depot, Steam, etc... Huge DNS issue.

---
### Post 11: AWS Outage 2021-12-22
- Score: 1143, Comments: 384
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/rm49er/aws_outage_20211222/
- Body: **As of 2021-12-22T18:52:00 UTC, it appears everything is back to normal. I will no longer be updating this thread. I'll see y'all next week. I'll leave everything below.**

Some interesting things to take from this:

- This is the third AWS outage in the last few weeks. This one was caused by a power outage. From the [page on AWS' controls](https://aws.amazon.com/compliance/data-center/controls/): "Our data center electrical power systems are designed to be fully redundant and maintainable without impact to operations, 24 hours a day. AWS ensures data centers are equipped with back-up power supply to ensure power is available to maintain operations in the event of an electrical failure for critical and essential loads in the facility."

- It's quite odd that a lot of big names went down from a *single* AWS availability zone going down. Cost savings vs HA?

- /r/sysadmin and Twitter is still faster than the AWS Service Health Dashboard lmao.

--- 

As of 2021-12-22T12:24:52 UTC, the following services are reported to be affected: Amazon, Prime Video, Coinbase, Fortnite, Instacart, Hulu, Quora, Udemy, Peloton, Rocket League, Imgur, Hinge, Webull, Asana, Trello, Clash of Clans, IMDb, and Nest


First update from the AWS status page around 2021-12-22T12:35:00 UTC:

> Amazon Elastic Compute Cloud (N. Virginia) (ec2-us-east-1)

> We are investigating increased EC2 launched failures and networking connectivity issues for some instances in a single Availability Zone (USE1-AZ4) in th

#### Top Comments:

**Comment 1** (score: 486): That makes three times in as many weeks?

Slack media uploads and status updates are broken as well.

**Comment 2** (score: 136): Oh god not Clash of Clans

**Comment 3** (score: 128): [deleted]

---
### Post 12: VMware now threatening outages to perpetual license holders
- Score: 3182, Comments: 473
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1pzp3eo/vmware_now_threatening_outages_to_perpetual/
- Body: # The saga with VMware continues!!!

**Backstory:**  
We've been a VMware shop for 10+ years with multiple data centers globally. We decided to let our service/support contract expire this year after we found out it jumped from $43k to $99k. We have perpetual licenses so there's not much concern in the department about things breaking. We are already in the process of migrating to AWS (we already have a large AWS presence) and Hyper-V. We're also evaluating Proxmox as a potential replacement for Hyper-V as well but that's a 2026-2027 initiative.

**Today's Communication:**  
Our license expires on (Dec 31st, 2025). Our VMware rep was already being pushy but today it escalated when the rep sent this email:

>Your licenses expire today and you will face environment disruptions as well as penalty fees if a PO is not submitted today. Please let me know if you need anything else from me. 

> Happy New Year!

><name of rep>


I would normally just ignore this email but it really upsets me that they're trying to use scare tactics by straight up lying to people. There will be no outage unless they decided to deactivate our perpetual license or some other malicious action which I'm sure would violate our sales contract and terms of agreement. I realize this is most likely just a scare tactic by a sales rep but damn this really irks me that instead of saying something like "IF there's an issue you won't have support" they said "YOU WILL" have outages. Trying to figure out how I want to

#### Top Comments:

**Comment 1** (score: 459): Don't reply. Get your legal team involved to assess.

**Comment 2** (score: 727): You got upgraded from “customer” to “hostage”

**Comment 3** (score: 1368): Ya need to get legal involved

---
### Post 13: Sysadmins that work for Game Studios: is it as fucking awful as it seems?
- Score: 363, Comments: 223
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1bwr45h/sysadmins_that_work_for_game_studios_is_it_as/
- Body: Every day it seems like there's news about a game studio having a massive data breach due to something that could've been wholly avoided if management actually invested in IT.

&#x200B;

I was on /r/games reading about how Nexon apparently let a developer keep source code/other assets on a private server at his home while WFH (wtf?????)

&#x200B;

Are all game studios like this or are studios like CD Project, Insomniac, or Sony just particularly shit?

#### Top Comments:

**Comment 1** (score: 293): I've been doing it for many years across several companies. It varies greatly on the size and the culture of the company.
 
Video game IT has all the standard pain points of other IT, with a few extra things to consider:
- technical users (there are fewer L1 tickets but also more opportunities for people to get themselves in real trouble - like hosting a whole project at home)
- creative users (the core of the business is creativity - oftentimes everything takes a back seat to creativity, includ

**Comment 2** (score: 350): Checking out source code to your work laptop is the norm. Remoting into AVD, Citrix or whatever and only working on code hosted there is the exception.

And not just in the games industry.

**Comment 3** (score: 46): IT at game studios is great if you are at the right studio with the right budgets ;). Security is taken very seriously. 

I've been in game studio IT for 25+ years and suspect I would not be able to work at a 'normal' business any longer.

---
### Post 14: It's time to rally around the AWS folks...
- Score: 184, Comments: 86
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1ohkk0v/its_time_to_rally_around_the_aws_folks/
- Body: To the AWS folks,

It's another Monday, we're seeing AWS-dependent services go non-responsive or significant delays, and we're not the only ones: [https://downdetector.com/status/aws-amazon-web-services/](https://downdetector.com/status/aws-amazon-web-services/) 

I doubt you're watching Reddit at a time like this but know that we're all here for you if you need us.

#### Top Comments:

**Comment 1** (score: 67): \+1 Seeing at least one web app that is known use AWS having performance issues.  US Midwest.

**Comment 2** (score: 24): And a MS365 issue just before this.

**Comment 3** (score: 20): ![gif](giphy|OCu7zWojqFA1W)

Oh boy.

---
### Post 15: Migrating off AWS for political reasons?
- Score: 283, Comments: 122
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1iwce06/migrating_off_aws_for_political_reasons/
- Body: Is this on anyone's radar?  Will EU governments and orgs start looking for alternatives, and if so what.  

https://berthub.eu/articles/posts/you-can-no-longer-base-your-government-and-society-on-us-clouds/

#### Top Comments:

**Comment 1** (score: 180): Er, didn't they start doing this when GDPR was passed in 2016?

GDPR says you can't give data to people the owner doesn't authorize. US law has said (for a very long time) that US companies must comply with data requests, even if the data resides on servers physically outside the US. They've been incompatible since day 1, and day 1 was almost 10 years ago.

**Comment 2** (score: 62): This is not really remotely a new problem. When I meet with European customers American bases public cloud is pretty much a dirty word. 

Microsoft gets around it by having a German company who runs Office365 in Germany. Several of the hyper skiers have tried various initiatives to run sovereign clouds at arms length like this but:

1. They tend to offer 1/100th thr number of services. Without that American SREs it’s hard to manage more than basic IaaS, object storage as these cloud platforms we

**Comment 3** (score: 12): OVH is European, and I don't think they have a US location yet, they do have a Canadian data center.

---
### Post 16: Is anyone experiencing issues with AWS right now? (US East coast)
- Score: 88, Comments: 55
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1rlsb1h/is_anyone_experiencing_issues_with_aws_right_now/
- Body: I'm seeing a lot of wierd degredations of service and looked at downdetector. Seeing AWS reports, now I'm wondering if anyone know anything.

EDIT: seems to be back up for the Amazon store. Not sure about other services.

#### Top Comments:

**Comment 1** (score: 40): Even Amazon (the store) itself is down, or at least a lot of its backend services are non-functional ATM. Someone's having a very bad day.

**Comment 2** (score: 30): Gotta love when Reddit beats their service bulletins. 

Amazon store is having severe issues as well so I assume fire alarms are getting triggered there.

**Comment 3** (score: 7): Yeah. Reddit keeps shitting itself sometimes. Has periods of just timeouts. But comes back eventually.

---
### Post 17: And it's AWS again..
- Score: 240, Comments: 61
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1obewvg/and_its_aws_again/
- Body: And again some services are at a standstill. US East-1 region outage affecting several services such as Atlassian, Slack and more.

#### Top Comments:

**Comment 1** (score: 75): DNS  
[https://health.aws.amazon.com/health/status](https://health.aws.amazon.com/health/status)

**Comment 2** (score: 54): Ah the cloud.  Where it’s just someone else’s servers you trust they keep running.

**Comment 3** (score: 45): It's fun to see all the eggs in one basket and oddly Reddit is still going lol

---
### Post 18: FortiClient is FortiAwful - Alternatives your Using?
- Score: 147, Comments: 139
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1jb3j2v/forticlient_is_fortiawful_alternatives_your_using/
- Body: Forticlient 7.X + has been *awful*.

For dozens of users, we've been having completely undefinable FortiClient issues, in that the connection issues have nothing to do with anything we can control, and I've had MORE than enough of this.

Apparently this is just par for the course with FortiClient, has anyone replaced FortiClient with anything else more effective?

We're looking at Cisco AnyConnect at the moment, it's a bit pricey but if it just works, it will be worth it. 

*(I admit I'm a bit traumatized by the CEO yelling at me from Florida that he can't access our Network drives, and me not being able to do anything with FortiClient to fix that)*



#### Top Comments:

**Comment 1** (score: 19): I find as long as we test a version on a few computers we are good. Do you get the installer from [http://support.fortinet.com/](http://support.fortinet.com/) so you can pick what version you install?  Are you on 7.2 or did you make the leap to 7.4?

The only time we were on the latest release was early on with 7.0 because of improvements in saml cookie handling.

**Comment 2** (score: 75): Have 50k users on Forticlient for over 2 years.

After initial teething problems I can count the number of genuine issues on one hand 🤷‍♂️

**Comment 3** (score: 13): While FC is indeed crappy, I have not seen any major issues since 7.2.5 (.4 had a stupid certificate bug)

FC EMS  is also great to remotely grab the client logs without effort, so I am pretty happy with that.

---
### Post 19: Task Failed Successfully: I Automated Myself Out of Work
- Score: 1458, Comments: 396
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1riwvyv/task_failed_successfully_i_automated_myself_out/
- Body: (Please help with advice)

About 9 months ago I joined my current company. At the beginning I was busy all the time. I focused heavily on automation and over time I basically automated almost everything critical:

* AWS cost optimization and monitoring
* Patch management
* Backups and automated backup restore testing
* Custom metrics for monitoring websites, networks and databases
* Server cleanup tasks
* Critical log tracking
* Performance monitoring and alerts
* Daily log reports
* Documentation

The problem is… now there’s barely anything left to do.

For the past couple of months, my actual workload has been maybe 1 hour per day at most. During daily standups I honestly feel like I have to “invent” updates just to justify my existence. If it wasn’t for the dailies, my team probably wouldn’t even remember I’m there. Everyone kind of works on their own anyway.

I’ve tried talking to my manager and dropping hints that I need more responsibility or asking if there’s anything else I can take on. He either ignores it or brushes it off. It feels like he knows there’s not much for me to do, but nothing changes. And I’m not getting fired (At least for this month XD)

At first it felt like a paid vacation. But after about 3 months of this, I’m starting to feel uncomfortable. I’m worried I’m getting rusty. I feel like I’m losing practice and momentum.

I’ve even thought about getting a second job, but the market feels tough right now. It’s hard enough to find roles, even help desk p

#### Top Comments:

**Comment 1** (score: 2035): first, do not tell anyone else that you have automated everything. find some project that brings value to the business but might take you a lot of time, work on that. everyone will be impressed at how you juggle so many tasks, and at the same time you're still bringing value. 

plan b is open a consulting company helping admins automate their tasks and target it toward the people in this thread. think of it like those executive life coaches except you help us fix our inbox to do what yours does.

**Comment 2** (score: 97): [deleted]

**Comment 3** (score: 654): [deleted]

---
### Post 20: Amazon is cutting hundreds of jobs in its cloud computing unit AWS
- Score: 429, Comments: 116
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1bv91re/amazon_is_cutting_hundreds_of_jobs_in_its_cloud/
- Body: Amazon said it’s cutting “several hundred roles” in the AWS sales, marketing and global service organization. Most of those cuts are related to business changes in AWS training and certification programs as well as sales operations. The tech giant said it was also making cuts elsewhere so it can invest in other business priorities.

https://finance.yahoo.com/news/amazon-cutting-hundreds-jobs-cloud-152552547.html

&#x200B;

#### Top Comments:

**Comment 1** (score: 427): US-East-1 gonna be shitting the bed even more often, I guess...

**Comment 2** (score: 145): [deleted]

**Comment 3** (score: 140): Built market share, now scaling back to profitability, and then ramp up prices...

---
### Post 21: Tools & Info for SysAdmins - Mega Summary (85 Items)
- Score: 1631, Comments: 194
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/9ir451/tools_info_for_sysadmins_mega_summary_85_items/
- Body: Hi [r/sysadmin](https://www.reddit.com/r/sysadmin)

Each week I thought I'd post these SysAdmin tools, tips, tutorials etc with [just one link to get it in your inbox each week](https://www.everycloud.com/it-pro-tuesdays). Let me know any ideas for future versions in the comments.

This week is a mega list of all the items we've featured to date, broken down into categories, for you to explore at your leisure. I hope you enjoy it. 

&#x200B;

**Free Tools**

[mRemoteNG](https://mremoteng.org/) is the next generation of mRemote, open source, tabbed, multi-protocol, remote connections manager. This was recommended to us by 'Oliviamcc’ who firmly believes "it is much better than Putty (SSH), Citrix, VNC, RDC, etc. "Make sure you figure out the credentials hierarchy, it works a treat and saves time every day".

[MailFlow Monitor](https://www.everycloud.com/free-mail-flow-monitor) is EveryCloud's free, cloud-based, round-trip tool that sends you an alert as soon as there is an issue with your email flow. Settings are adjustable to allow you to choose how much of a delay is acceptable and which types of bounce alerts you want to see. Helps you get to the bottom of a problem before users have even noticed it.

[TreeSize Free](https://www.jam-software.com/treesize_free/). Find and free up your or your user's free space. TreeSize Free tells you where precious disk space has gone. I've seen this recommended in too many places to mention. 

[PDQ Inventory and Deploy](https://www.pdq.com

#### Top Comments:

**Comment 1** (score: 63): *sigh*  Well I was gonna get some work done....

*browsing intensifies*

**Comment 2** (score: 34): What a great and comprehensive list.  It's folks like you who make the global community of sysadmims better.

**Comment 3** (score: 64): You mentioned /r/Powershell but I'd like to mention /r/Powershell's favourite book and for anyone learning or wanting to learn Powershell it will be their favourite book too: "Learn Windows Powershell in a month of lunches". 

Great list by the way!

---
### Post 22: For you future Architects / DevOps out there, a reminder of why SysAdmins are here to stay even in the world of Cloud
- Score: 973, Comments: 244
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/mtn2e4/for_you_future_architects_devops_out_there_a/
- Body: Hi everyone! Just posting this as I replied to a recent DevOps thread in regards to something about how SysAdmins will be slowly phased out over the coming years, and I thought that for this sub it might help one some of the aspiring architects and other people that are wondering what path they should take in the upcoming DevOps journey. More importantly how you should argue that you can't just "sprinkle a little bit of DevOps" on everything and hope it works without some sort of Systems Administrator stuck at the helm of it all.

Depending on what path / silo you're on in the DevOps chain, especially in an Enterprise environment, I cannot stress the importance of having a good SysOps team that stands at the top. Having Developers / Engineers design most of the workflow around GitOps and the SDLC is fine, but having them design the overall fit of the infrastructure is a terrible idea IMO.

#Why You're Important
There are many things that SysAdmins (Network Admins too!) are exposed to that Developers really don't need to deal with and probably don't want to deal with on a daily basis. Things like User Account policies, Backups, Compliance, User Auditing, Security, Firewalls, Subnets, VLANs, etc. that honestly a developer could really give two shit$ about when it comes to things you do and practice on a daily basis. Let me add to that the extent that most Developers will look at SSL Certificates is "LetsEncrypt generates a cert and I attach that cert", which is fine... because 

#### Top Comments:

**Comment 1** (score: 100): [removed]

**Comment 2** (score: 74): [deleted]

**Comment 3** (score: 199): True story. Developers have been trying to eliminate admins for at least 15 years. Mostly it drives the skilled sysadmin to learn enough development to eliminate developers who are terrible and better guide the ones who know their program and want to work with the admin. 

There is room for both disciplines and a need for both. Expertise can only run so deep and even with IAAC abstraction someone ultimately had to know what the underlying I you are doing As Code does.

---
### Post 23: What is a AWS Solution Architect and SysOps Administrator Career Path
- Score: 18, Comments: 8
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/6b53iz/what_is_a_aws_solution_architect_and_sysops/
- Body: I'm currently a junior Systems Administrator in a all windows shop. Seeing that many companies are moving their infrastructure off prem and into the cloud, I want to learn AWS. To at least be ahead of the curve. What would be the steps to make this transition into these careers?


#### Top Comments:

**Comment 1** (score: 12): Get a book/training video, open up a free* account, make a VPN tunnel between you and AWS, and go to town.

Certain features are not available for AWS free.

If you know virtualization, then AWS EC2 is 100% exactly the same time from an instance/vm level. It's virtualization with permissions restricting you to the VM level.

The difference that will get you if you're not paying attention is their networking. They've modified their networking to work a bit differently in the cloud. For example, E

**Comment 2** (score: 6): Acloud.guru courses are invaluable in getting the certs, but a very good resource for learning the fundamentals of AWS as well. They definitely gear the courses to passing the exams, and you'll hear them repeat that several times over, but you'll go from zero knowledge to having really good working knowledge just by going through the CSA and Sysops courses.

In terms of career path, unless you can get exposure at your current place to AWS, you'll want to transition to an org that uses it or star

**Comment 3** (score: 2): Pick a project and build it.  I set up a Terraria server for my friends and I to use in AWS when I was learning it.  If you're all windows you also might want to look at Azure - I believe MCSE's get some sort of free $$/month.

But yeah, build something in the cloud - something [i]useful[/i] so that you have some hands on concept of what is doable and what isn't.  That'll give you something to talk about in an interview as well (I'd rather hire someone who built his own game server in AWS over s

---
### Post 24: What is the future? Does nobody knows?
- Score: 44, Comments: 69
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1o7x38j/what_is_the_future_does_nobody_knows/
- Body: I’m hitting 42 soon and thinking about what makes a stable, interesting career for the next 20 years.
I’ve spent the last 10 years primarily in Linux-based web server management—load balancers, AWS, and Kubernetes. I’m good with Terraform and Ansible, and I hold CKA, CKAD, and AWS Solutions Architect Associate certifications (did it mostly to learn and it helped). I’m not an expert in any single area, but I’m good across the stack. I genuinely enjoy learning or poking around—Istio, Cilium, observability tooling—even when there’s no immediate work application. 

Here’s my concern: AI is already generating excellent Ansible playbooks and Terraform code. I don’t see the value in deep IaC expertise anymore when an LLM can handle that. I figure AI will eventually cover around 40% of my current job. That leaves design, architecture, and troubleshooting—work that requires human judgment. But the market doesn’t need many Solutions Architects, and I doubt companies will pay $150-200k for increasingly commoditized work.
So where’s this heading? What’s the actual future for DevOps/Platform Engineers?​​​​​​​​

#### Top Comments:

**Comment 1** (score: 42): >I’m hitting 42 soon and thinking about what makes a stable, interesting career for the next 20 years.

No one knows the answer to that question until they have access to time travel.

That's not how careers work.  You try and make decisions for the next 1-2 years, and adjust as life changes with and around you.

There's no way to reasonably predict all the things that will be going on in the early 2030s, and how they will affect employment options.

  
DevOps isn't going anywhere soon, and what

**Comment 2** (score: 45): I heard goat farming is lucrative.

**Comment 3** (score: 12): I learned to stop worrying and just take it a day at a time. No one knows the future, so it’s best to not stress over it. As much as I don’t like AI, it’s a tool that I’ve learned to used to cut down time, if it’s here to stay, might as well learn to use it properly.

---
### Post 25: AWS Solutions Certified (full collections of useful resources)
- Score: 14, Comments: 5
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/3j47m9/aws_solutions_certified_full_collections_of/
- Body: Here's a little list of useful learning material I put together for myself, hope it's worth even for you:

**AWS Solutions Architect - Associate**
https://cloudacademy.com/certifications/aws-solutions-architect/

**AWS Solutions Architect - Professional**
https://cloudacademy.com/certifications/aws-solutions-architect-pro/

**AWS SysOps Administrator - Associate**
https://cloudacademy.com/certifications/aws-sysops-administrator/

**AWS Certified Developer - Associate**
https://cloudacademy.com/certifications/aws-certified-developer/

**AWS Certifications Study Guide**
http://cloudacademy.com/blog/aws-certifications-study-guide-2/

#### Top Comments:

**Comment 1** (score: 3): Thanks for sharing!

**Comment 2** (score: 3): Has anyone done any of these? Were they worth the cost/help career in anyway?

**Comment 3** (score: 2): Here's an even better resource for actual certification:  [AWS Certs](https://reinvent.awsevents.com/certification.html)



---
### Post 26: Do you have anxiety regarding tasks which you are not familiar with?
- Score: 54, Comments: 79
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1e4iblj/do_you_have_anxiety_regarding_tasks_which_you_are/
- Body: When I started my IT career 4 years ago, I was excited to start to work in in this field. I started with L1 support, helpdesk, desktop support and currently I am a junior cloud engineer working with Azure / AWS. Got an AZ-104 and an AWS Solutions Architect cert. 

What I noticed that every time I receive a task which I am not familiar with (which is very common in IT ) it makes me anxious that I am not going to able to do it, despite the endless resources on the internet. And this makes me procrastinate which is obviously not good. 

Is this common working in IT or it is just me? 

If this topic is not relevant to this sub, MOD please remove it. 

#### Top Comments:

**Comment 1** (score: 33): Happens to the best of us. When I get hit with a task that I'm not familiar with I seek help of other professionals, this is the only way!

**Comment 2** (score: 25): Depends on the task:

- a project I can take my time to think about - cool! Let's do it!

- something's on fire and I have absolutely no idea how that particular system works - crapcrapcrapcrapcrapcrap

**Comment 3** (score: 16): I learned in IT: Attack the task, find help if you are unsure. Never surrender! 

My first boss was a cool dude (back in the 90's)! 
He had an Position in his Budget called "Mercenary Support". 

So if i had such a task he said: Search an Mercenary and learn from him!
Gues who has now a same position in the Budget today. Still works :)

---
### Post 27: Looks like VMware leaked their own AWS announcement
- Score: 424, Comments: 125
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/57ake7/looks_like_vmware_leaked_their_own_aws/
- Body: Looks like they posted the article and took it down, but not fast enough for google cache! http://imgur.com/a/rklVm

https://webcache.googleusercontent.com/search?q=cache:HWHvJLLZadoJ:https://blogs.vmware.com/vsphere/2016/10/vmware-aws-announce-strategic-partnership.html+&cd=4&hl=en&ct=clnk&gl=us

Full text:

Today, VMware and AWS are announcing a strategic partnership that brings the two leaders in Enterprise IT together to deliver a vSphere-based cloud service running on AWS. This service will make it easier for customers to run any application, using a set of familiar software and tools, in a consistent hybrid cloud environment.
The Power of VMware on AWS

Currently in Technology Preview, VMware Cloud on AWS, will bring VMware’s enterprise class Software-Defined Data Center software to the AWS cloud, and will enable customers to run any application across vSphere-based private, public and hybrid cloud environments. It will be operated, managed and sold by VMware as an on-demand, elastically scalable service and customers will be able to leverage AWS services such as developer tools, analytics, databases, and more.

This jointly architected service represents a significant investment in engineering, operations, support and sales resources from both companies. Designed to deliver a great customer experience, the service will be optimized to run on dedicated AWS infrastructure purpose-built for this offering. It will deliver the power of VMware’s SDDC infrastructure software 

#### Top Comments:

**Comment 1** (score: 115): Funny, we had an AWS sales guy and architect visit us a few months ago.  After the meeting I said to them, "Hey, you know how you could get me to migrate my entire environment to AWS tomorrow?  Start supporting ESXi."  The architect kind of got a disgusted look on his face and said "Uh, no."


**Comment 2** (score: 58): Here's a key item from the press release:

> Operated and supported by VMware: The service will be operated, **sold** and supported by VMware. All software components of the service will be fully certified and supported by VMware.

Particularly the **sold** portion. You won't go to AWS and buy VMware.  You go to VMware and buy VMware that's deployed on AWS.  

I'd expect them to entirely wind down their own vCloud Air offering, migrating customers to AWS, where you can get exactly the same thing

**Comment 3** (score: 15): SON OF A *^%($*^$. I **JUST** got finished deploying my whole entire DR to AWS with AWS ZERTO licensing because I couldn't use my existing vmware licensing, dealing with AWS' non-traditional networking and their quirks to find this out?


---
### Post 28: The software dev here is trying to get me out of help desk. How can I answer the call?
- Score: 69, Comments: 46
- Subreddit: r/sysadmin
- URL: https://reddit.com/r/sysadmin/comments/1dwvmo9/the_software_dev_here_is_trying_to_get_me_out_of/
- Body: Situation: I graduated few years back in Cyber Security. I have the CompTIA trifecta and right now I'm working help desk, but really is like jr admin at this point. Since I touch everything. Security, networking, spin up servers sometimes, upgrade servers. 

Right now I'm working on my AWS certifications. Because I am doing an AWS project for my job. I was planning to ask my boss for a role change for be a solutions architect or something of the sort. My boss even said me getting these AWS certs would be a good thing.

My boss said before I could be the "Systems Engineer" whatever that means, and they can hire someone to be below me. 

I'm close with a software dev here. He mentioned how he's trying to start a new project team here and he wants to bring me in on it. I've had to work with him to setup servers and make appropriate firewall changes and such. He is having a meeting with my boss about it cause he wants me in on it. 

He mentioned how I could do devops. I'm not ready to do dev ops. I need to work more on programming to be ready for a role of that nature but I didn't say no. But Maybe I could be a solutions architect or Systems engineer like my boss said. 

Either way he's trying to get me out of my current position and I want to know how I can be of value for him. I know a bit of everything but I don't specialize in anything. I touch networking, servers etc.

The security team also said they would take me in their department.

#### Top Comments:

**Comment 1** (score: 176): I find that the people who wait until they’re completely “ready” often get left behind. Don’t jump into something without having a clue, but be open to starting without knowing everything or feeling completely comfortable. Learning on the job is part of devops/dev regardless of how much experience you have, and it’s ok to feel like you don’t know everything.

**Comment 2** (score: 18): If someone you trust and has more knowledge or a higher role than you says you can do a great job there it's highly possible that is true and you deserve it.
Another thing is how afraid you are about a move like that in your career, that's normal, but many changes like this are for better.

**Comment 3** (score: 54): I promise you getting a certification in DevOps will make you even less qualified than you are now. 

If you go though my posts, you'll see I have nothing but contempt for programmers and developers, so it pains me to say this attach your wagon to this software developer guy. Look at what your degree and certifications have gotten you, two years as a help desk monkey and while you've been increasing your responsibilities, your boss is being wishy washy with a promotion if you get this or that ce

---
