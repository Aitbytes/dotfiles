# Reddit Data - gitlab

## Collected Posts and Comments

### Post 1: Will GitLab last?
- Score: 14, Comments: 49
- Subreddit: r/gitlab
- URL: https://reddit.com/r/gitlab/comments/1n02t3l/will_gitlab_last/
- Body: If you go to about.gitlab.com it heavily promotes AI/ML.

If the AI bubble ends up popping (which it probably would), would GitLab still last? Would GitLab go bankrupt or get discontinued?

#### Top Comments:

**Comment 1** (score: 108): Yes. GitLab is way more than its AI Features. Most customers probably treat its AI Features as a "cherry on-top" as opposed to a core necessity. There's a real chance if the AI Bubble pops, it might be better for GitLab, because the core product is so solid.

**Comment 2** (score: 34): Yeah, they'll still be around. GitLab grew to a $7 billion valuation before AI was even part of the discussion. If the AI bubble pops then they'll keep going strong on the DevOps fundamentals that built the company.

**Comment 3** (score: 17): I'm self-hosting it, and yes, it's absolutely worth it, in every single respect.

It's so convenient for me to host my version control and my container registry, I can't even think about a better solution on the market right now. Its convenience is proven and some big companies in my country are in the midst of a migration towards it.

On top of it, GitLab CI is excellent, for the DevOps guys.

They might want to attract people with AI features on their side and I'm OK with it, as you can't mark

**Comment 4** (score: 14): My whole company is using their saas offering it’d be tough to move elsewhere probably take like 6-12 months

**Comment 5** (score: 12): This is kinda like asking if Ford will go bankrupt because a new type of tire is making waves and current model cars ship with it.   
  
Gitlab is an amazing product that was well positioned to take advantage of the AI craze however whether it goes nuts or dies at the end of the day it's just a set of features that compliment foundational excellence. 

I say get that $$ while it's flowing and I'll continue using the core product that has served me and my team(s) well for years at this point.

**Comment 6** (score: 8): Gitlab has been around for a lot longer than the AI stuff, plus I think all of the AI is locked behind the paid tiers, which probably explains why it's promoted on the about page but you certainly don't need it.

Gitlab CE is open source, so even if something did happen to the parent company it's not necessarily the end of the platform.

**Comment 7** (score: 4): Have you used Gitlab Duo or Gitlab Duo Agent yet?

Gitlab Duo is a pretty reasonable LLM. I'm having a rough time getting Agent to work the way I want it to work (as in work at all). Times out when I try and create a workflow to do something as simple as build my repo. It's still experimental (unlike Duo Chat) so I can give them BOD that it'll get better but it's effectively a "Free" agent using very good models for their backing and good tooling that integrates into basically every dev workflow

**Comment 8** (score: 3): AI/ML isn't the magic of it. We are.

**Comment 9** (score: 2): Who are the two biggest providers in the space, and if the AI bubble crashes, which one does it affect more?

**Comment 10** (score: 2): Gitlab offers a lot more than AI/ML.

---
### Post 2: What do you see as GitLab’s biggest advantages and disadvantages?
- Score: 27, Comments: 41
- Subreddit: r/gitlab
- URL: https://reddit.com/r/gitlab/comments/1ocp3ex/what_do_you_see_as_gitlabs_biggest_advantages_and/
- Body: Hey everyone,

I’m currently working on a project that involves evaluating GitLab from a developer and DevOps perspective. I’ve already read through the official documentation and corporate materials, but I’d love to hear from *actual users*.

From your own experience — what do you consider GitLab’s main **advantages** and **disadvantages** compared to other platforms (like GitHub, Bitbucket, etc.)?

Things I’m especially interested in:

* CI/CD performance and reliability
* Integration and automation capabilities
* Usability and UI
* Flexibility for self-hosting vs SaaS
* Cost/value ratio

Looking forward to your insights and honest opinions!

#### Top Comments:

**Comment 1** (score: 7): I don't have much experience in GitHub, so cannot compare. 

We use Gitlab CI for CI/CD, but without auto DevOps function. 

Some thoughts:

1. You will need to set up your own Gitlab runner to run the pipelines, shared runners have limited capacity and pretty unreliable. The good news it's quite easy to do. We have cheap EC2 instance for "normal" tasks and expensive GPU instance for CI tests: Gitlab supports this by specifying tags on jobs and configuring the runners to pick up jobs with those 

**Comment 2** (score: 9): The biggest advantage for Gitlab is that it is not owned by Microsoft and that you can self-host. 

Microsoft is famous for its [embrace, extend and extinguish](https://en.wikipedia.org/wiki/Embrace,_extend,_and_extinguish) strategy, so I prefer to minimize my use of GitHub.

**Comment 3** (score: 9): I think the UI is one of the selling points personally, the very point of gitlab over others is the way they put everything that matters to devs in a common UI, this is where they shine imo.

Obviously this depends how much you use the platform, if your just using gitlab as a source code repo only your missing out on most of its benefits, when you adopt it across the board it really shines Imo.

**Comment 4** (score: 4): 
CI - Brilliant but 
CD - not so much

**Comment 5** (score: 4): CICD, self hosting capabilities, how the runners all work are major pros.

The project management aspects and WIKI are garbage compared to JIRA and Confluence.  I really want to use them and like them especially with self hosted Atlassian going away.  I work in several industries where we are required to self host.  Gitlab project management components just are not a competitor and clunky causing us to look at other options as the 2029 deadline starts to approach.

**Comment 6** (score: 5): Advantages:
- best integrated CI/CD
- nice support for kubernetes
- I find the UI to be much nicer than anything else I've used
- built in editor mostly works, handy when you've got the pipeline all set up and can deliver changes from wherever you are
- it's everything all together in one package, minimal need for external integrations (aside from e.g. setting up an elasticsearch cluster for advanced search)

Disadvantages:
- CI/CD not well-suited for big builds like Yocto/OpenEmbedded, or AOSP.

**Comment 7** (score: 10): Pro It’s gitlab. Con it’s gitlab.

**Comment 8** (score: 3): What really stood out to me about GitLab is how everything is integrated in one place. I used to juggle multiple tools for code hosting, CI, issue tracking, and deployments. Switching between them slowed me down and caused context switching issues. With GitLab, having issues, merge requests, and pipelines all connected means I spend less time managing tools and more time actually building. It’s not perfect, but that tight integration helped our team move faster and keep everything aligned.

**Comment 9** (score: 3): Well… GitLab’s ambition to be an all-in-one DevOps platform has led to an overextended monolith that is difficult to operate, slow to start, and frustrating to debug. The HTTP 500s on simple permission errors and the sluggish rails console are not user mistakes but reflect architectural bloat and completely insufficient fault isolation. Opening a rails console or dbconsole taking about 50sec to open is a nightmare to work with in practice. It works from a developer perspective while introducing 

**Comment 10** (score: 3): I’d say the main advantage is in Gitlab you can structure your projects into groups and subgroups. This is really missing in GitHub. 

I find having to build out and maintain tooling in Gitlab is a pain vs GitHub actions is just nicer to use sometimes. 

It I was starting from scratch I’d to GitHub, copilot alone is a massive selling point vs Gitlab duo. At work we’re a Gitlab shop but also maintain a GitHub instance for copilot and iOS builds using Mac runners/ actions in GitHub.

---
### Post 3: GitLab UI just got way better 🚀
- Score: 18, Comments: 34
- Subreddit: r/gitlab
- URL: https://reddit.com/r/gitlab/comments/1r675bz/gitlab_ui_just_got_way_better/
- Body: I hadn’t used GitLab in a while, but I recently came back to it and the difference is obvious to notice. The UI feels much more modern,and productive compared to what I remember.

Navigation seems clearer and overall it just looks and performs better. Really happy with the direction it’s heading. :)  
  
Curious if others had the same experience after coming back to it, What do you think of the new GitLab?



#### Top Comments:

**Comment 1** (score: 23): Sus

**Comment 2** (score: 23): 8 day old account made solely to glaze the GitLab UI? 

A bit odd, I'll admit

**Comment 3** (score: 3): New UI reminds me of Supabase. On average, I found the UI update to be a net negative.

It IS better... perhaps marginally, but the negatives of destroying muscle memory outweigh the benefits.

That said, I adopted within a day, but the usual slowpokes in our org had particular trouble this round of upgrades. It pissed off the CEO, and the CEO pays the bills.

**Comment 4** (score: 2): Not a fan of the file tree showing when browsing the repo, need to see if that can be turned off.

Other than that, it’s pretty good.

**Comment 5** (score: 3): It’s quite a polarizing topic. Some people like the new UI, lots of people do not. That tells me it’s not clearly better.

**Comment 6** (score: 1): I still can’t get used to having to double click enter on search, but the UI is fine

**Comment 7** (score: 1): I did the same recently. I like the more modern look.

**Comment 8** (score: 1): I started using it ever since I found out that I can organise projects into folders.

**Comment 9** (score: 1): Not only is the new UI faster and cleaner but it is also configurable.  If you don't like the layout, you can change it.   My fav is VSCode in the browser.  I am a command line person and I like my IDEs but it is nice to be able to use Code in the browser for quick edits.

**Comment 10** (score: 1): Irrelevant because I can’t run that monster locally. Don’t have 16 GB RAM on the server. And I don’t use the online version much. But yes, the UI got better.

---
### Post 4: [Github enshittification] might see a (small?) influx of new people on Gitlab soon
- Score: 52, Comments: 29
- Subreddit: r/gitlab
- URL: https://reddit.com/r/gitlab/comments/1powy74/github_enshittification_might_see_a_small_influx/
#### Top Comments:

**Comment 1** (score: 23): It's especially this one that got people irked:

> beginning March 1, 2026, we are charging $0.002 per-minute across self-hosted runners

Just to be clear: it's not about Github-hosted runners, it's the self-hosted runners.

**Comment 2** (score: 8): [deleted]

**Comment 3** (score: 5): Gitlab is getting enshittified too unfortinately. Recently thei have mostly only made their UI worse or pushed more Duo "AI slop" features...

**Comment 4** (score: 4): Forgejo and it's runners are still free if you wanted to self host it all.

**Comment 5** (score: 3): I am still surprised why people host private repo on GitHub, if we use gitlab with gitlab runner we don’t need to anything to run.

**Comment 6** (score: 5): fyi: GitLab is not exactly loved more than GitHub ngl given its not a foundation and invests alot into AI. So who knows.

**Comment 7** (score: 2): Bitbucket now GitHub, makes me think gitlab will follow

**Comment 8** (score: 2): As much as I love gitlab and use it every day. I would recommend codeberg instead, as Gitlab is out looking for buyers

**Comment 9** (score: 1): Microsoft... all I've got to say.

**Comment 10** (score: 1): Gitlab has been enshitificating itself for years already. So busy trying to plug Duo that they forgot we need proper filtering on boards...

I used to be a big Gitlab fan... Now, not so much...

---
### Post 5: My Life as a Gitlab instance: How I use GitLab to manage almost everything
- Score: 91, Comments: 12
- Subreddit: r/gitlab
- URL: https://reddit.com/r/gitlab/comments/1ravlpc/my_life_as_a_gitlab_instance_how_i_use_gitlab_to/
#### Top Comments:

**Comment 1** (score: 7): Neat. The one thing I dislike with gitlab is its default search. But supposedly this can be tweaked,  haven't tried it yet, but something like this: https://github.com/phillipj/gitlab-search

**Comment 2** (score: 6): Nice work. It is great to see someone else who uses GitLab for so much. I have a self-hosted setup at work that drives my entire department and is integral to my job. Software development, but really almost project management now, as LLMs are starting to take over a lot of the work I used to have to do myself. The tech combined lets me be free to think, and I love to think.

**Comment 3** (score: 1): I was tinkering with the same idea!  But I hate the inconsistency in how to interact with item with glab or the python cli : you have some thing you can modify vía the api but others ( like end date, health and the new status system) goes via the widget system and you have to do some graphql mutation :(

**Comment 4** (score: 1): Love this! Using GitLab for personal organisation feels very “engineer brain”, versioned, automated, reproducible. Do you think this approach works long-term, or does it require constant maintenance to avoid becoming another system to manage?

**Comment 5** (score: 2): You need to spin elastic search

**Comment 6** (score: 1): I am also add some LLMs to my workflow. I would love to hear how do you use LLMs for your work.

**Comment 7** (score: 1): I use glab for few things here and there. But I am not there yet, I still want to add more automation with glab/API and maybe some AI.

**Comment 8** (score: 1): I've been doing this for more than 5 years now, I started using it mainly for learning (Mgoun). Then I started adding more things. My rule of thumb is to use markdown everywhere, so I don't have get locked in anywhere. Another thing is to always stay minimalist.

The workflow is most of the times: 

issue + internal conversation in comments -> commit changes somewhere (Either content behind a static site generator) or some code for a coding project. -> Publish/Share

**Comment 9** (score: 1): I'm pretty green so I'm still learning. My latest discovery is that Claude Code for desktop can SSH into machines for me and do the same work I used to have to do manually--compiling, flashing, and developing embedded systems, primarily, at least this month. I've got it testing and trial-and-erroring toward an automated production test system right now.

edit: [link](https://code.claude.com/docs/en/desktop-quickstart)

**Comment 10** (score: 2): Thanks! The portability angle (Markdown everywhere) + minimalism makes a lot of sense. Appreciate you taking the time to explain your workflow.

---
### Post 6: Gitlab Duo Agent Platform
- Score: 15, Comments: 23
- Subreddit: r/gitlab
- URL: https://reddit.com/r/gitlab/comments/1qlnt9t/gitlab_duo_agent_platform/
- Body: Looking to get thoughts on the rollout of Gitlab Duo Agent platform and see if it’s been useful to anyone who has begun to integrate it into workflows 

#### Top Comments:

**Comment 1** (score: 8): Bro gitlab duo req 5 million in funding before they give you access.


That being said, i use it. Its useful, not as useful as other things. The agent catelogue is ..mid 

But the hidden powehouse is that repo aware multi agent team. Yea bro. Duo is legit for that reason.

Better on self host tho agent gateway sucks

We use it here [gitlabs needs to give me more toys](https://gitlab.citadel-nexus.com/users/sign_in)

**Comment 2** (score: 3): They quoted us a grotesque number / seat. It ended up being cheaper in labor alone to just embed our code base, wrap a tool around it and build our own agent to do the things we wanted duo to do. YMMV

**Comment 3** (score: 2): RemindMe! 1 week

**Comment 4** (score: 2): I would just use the unofficial MCP on GitLab and then hook it up to Claude or something. Duo is a proprietery expensive sinkhole of money for GitLab's sales team. It feels 2 years too dated already. Can it even do internet searches? It can't even create a project for me.

**Comment 5** (score: 1): I use it since a few months, since it was in beta. Hate the new credits payment though...

**Comment 6** (score: 2): >Bro gitlab duo req 5 million in funding before they give you access.

Are you getting confused with another program? ([https://about.gitlab.com/solutions/startups/](https://about.gitlab.com/solutions/startups/))

**Comment 7** (score: 1): For a user base of 2000 what is the suggested AI gateway config ? (Resources and no of pods?)

**Comment 8** (score: 1): I will be messaging you in 7 days on [**2026-01-31 15:34:07 UTC**](http://www.wolframalpha.com/input/?i=2026-01-31%2015:34:07%20UTC%20To%20Local%20Time) to remind you of [**this link**](https://www.reddit.com/r/gitlab/comments/1qlnt9t/gitlab_duo_agent_platform/o1fugsz/?context=3)

[**CLICK THIS LINK**](https://www.reddit.com/message/compose/?to=RemindMeBot&subject=Reminder&message=%5Bhttps%3A%2F%2Fwww.reddit.com%2Fr%2Fgitlab%2Fcomments%2F1qlnt9t%2Fgitlab_duo_agent_platform%2Fo1fugsz%2F%5D%0A%0AR

**Comment 9** (score: 1): Can you do a quick review. We are looking to find funding and test it but any hands on experience upfront would be great

**Comment 10** (score: 1): No, duo specifically requires 5 million in funding tonger access, not gitlabs itself just duo. Thats what we had to aquire.

---
### Post 7: Purchased gitlab premium for our team of developers. Applied to self-hosted gitlab. Billable user count calculated by software does not match billable users as defined by gitlabs own documentation.
- Score: 12, Comments: 22
- Subreddit: r/gitlab
- URL: https://reddit.com/r/gitlab/comments/1qruiyl/purchased_gitlab_premium_for_our_team_of/
- Body: I'm the license and systems admin for dozens of systems at the company I run an IT department for. I only consume license "seats" for myself or my systems admin team in systems that I (or we) are a consumer of. This is standard. 

We have a software dev team with 6 members. We read the "billable users" documentation, which clearly states that a billable user is a user with assigned roles on the system.

We have 6 users that meet that definition. We also have a root user that was created by the system at initial creation by the software itself with no developer roles assigned on any projects, and I have a user account on the system with admin privileges but NO DEVELOPER roles assigned on any projects. My account is for license administration, the root account is break-glass. The user interface clearly shows "Roles : None" for these accounts. 

After applying the premium license to the server, the server is immediately displaying "8 billable users" and warning that we will be billed for the additional users. I am going rounds with gitlab support on this issue but getting nowhere. They seem to think I'm actually going to pay for these non-developer accounts. 

The price doesn't even matter, the principal of the thing is completely asinine. I have never heard of such a thing in any other system. 

At this point, I'm about ready to sic our lawyers on them for fraudulent billing practices. Who else is paying for premium seats on their gitlab server for the privilege of inject the l

#### Top Comments:

**Comment 1** (score: 11): All active users are billable in premium, no matter if a role is assigned in a project or not. Only in ultimate are active non-bot users at or below Guest role free.

https://docs.gitlab.com/subscriptions/manage_users_and_seats/#criteria-for-non-billable-users

**Comment 2** (score: 7): Here’s a quick point on the initial root user. 

https://about.gitlab.com/pricing/licensing-faq/#do-i-need-the-administrator-account-aka-root-that-came-installed-if-i-am-also-an-administrator

**Comment 3** (score: 2): Have you checked which user is billable? I remember under admin somewhere, you can see which is taking seat. I'm a bit confused.

**Comment 4** (score: 1): Billable users don’t always update right. You should validate the nightly job to calculate the users is running. There’s a note at the bottom of the pane saying when it last updated. I would check this first, as this job can get stuck and not calculate stuff right.

Billable users are calculated (per the docs) at a variety of levels. Only GitLab Ultimate users get free guest users. If they have a login to GitLab AND can access source code; at the premium level they’re billable. Including the roo

**Comment 5** (score: 1): Admin has an implicit role to everything - deactivate the default admin account, use your main account for admin work (there is a setting to require admin mode with a password), and contact GitLab about dropping those 2 from the bill as part of onboarding.

**Comment 6** (score: 1): The document contradicts itself. The statements made in the first part of the document, defining a billable user, is then contradicted in later paragraphs, however, subject to interpretation, the point about role assignment is never clearly made in any other part of the document.

Why should I have to pay "ultimate" pricing for my users, for the privilege of having a back-end admin and license administrator account that isn't billed, like every other software system on earth?

Why should I have 

**Comment 7** (score: 1): Thank you for this...

The thing that rubs me really wrong about this, is like, if I wanted to, I could just pay for 3 users and have my 6 developers share those accounts. They trust me to create a develop account for each actual developer, but then don't trust me when I don't assign a developer role to my break-glass admin or license admin accounts? The inconsistency here doesn't work for me. Either you trust me to buy the right number of licenses and ASSIGN them to users, or you don't. That's 

**Comment 8** (score: 1): I'm the license admin for Autodesk products and vault server admin. I do not USE the vault server, Inventor, Autocad, anything, I just host the services, assign licenses/users, and configure these things for my users; therefor my user account does not require any licensing. My job is to HOST the service for my users, not USE the service. If gitlab can't figure out how to have an admin account for the IT team on the back end that doesn't need licensing, then I have serious questions...

**Comment 9** (score: 1): On days like this you might like playing this one turned way up:

https://music.youtube.com/watch?v=6BNym9D--ao&si=Scf7prUSoQy-nNAV

**Comment 10** (score: 6): You need to double check Gitlabs documentation in most cases. As it is kind of mixed between Free, Premium and Ultimate, it is not always apparent directly, which tier even a feature in the same document applies.

That being said Gitlab is actually quite pleasant for us to deal with regarding licensing in even unusual circumstances. Granted we have about 2k users, that eases some disputes as well.

Some other vendors though…

---
s that you have to look out for. If you haven't already, look into the `forward` and `inherit` keywords.

To answer your title's question though, we love GitLab pipelines at my org.

**Comment 3** (score: 10): Regarding the second question: use caches for dependencies. Obviously depends very much on your language, but most often there's a nice split between what should go into a build image and what can go into the cache. If you use self-hosted runners, put the cache close to them.

**Comment 4** (score: 8): It depends on how you make your runner image and if your runner image has access to a preloaded container with all your builder components. 

If you’re doing things like using their DinD image, it will always take 30 seconds for it to do its startup process because that’s how they manage the service. 

You also don’t have to make everything multistage with artifacts passing from stage to stage. 

I have my gripes with gitlab’s ci process and organization but it’s such a breathe of fresh air comp

**Comment 5** (score: 8): I just use dagger which makes the specifics of each CI provider largely irrelevant.

**Comment 6** (score: 7): Somewhat related to CI aspects of Gitlab/Github.

I've worked with runners for both, and Github runners are a fucking bitch to start with. I would take Gitlab over Github every time.

**Comment 7** (score: 6): I'm using GitLab CI extensively at work and I love it. It's extremely powerful. Yes there are flaws and yes there are ton of feature request that had be really cool which don't get added but I had the "pleasure" to work with Jenkins and I think GitLab CI is superior in every way. I have also worked with Azure DevOps and GitHub Actions. It's nice for simple deployments but GitLab is much more powerful. I'm guessing for just building/uploading GitLab can seem confusing/overkill but if you need mor

**Comment 8** (score: 3): I have to deal with GitHub actions, bitbucket ci and Gitlab. I take Gitlab any day of the week.

**Comment 9** (score: 5): Harness CI is the best

**Comment 10** (score: 3): One thing that bothers me about gitlab ci is the inability to create a dynamic pipeline other than by dropping child pipelines... Why can this be done in CircleCI and GitHub but not in gitlab escapes me...
Other than that I kinda like it

---
### Post 8: How do I decide between Gitlab CI, Bitbucket Pipelines, Jenkins, and Azure Pipelines?
- Score: 42, Comments: 103
- Subreddit: r/devops
- URL: https://reddit.com/r/devops/comments/1co3k0c/how_do_i_decide_between_gitlab_ci_bitbucket/
- Body: Hi so I've seen a lot of posts discussing similar questions about the best CI/CD but what confuses me is that people a lot of times suggest GitLab CI and GitHub Actions, are they meaning that they should change SCM providers as well? Or are they saying they should create a copy of their repository in GitLab/GitHub and pay the costs of two providers just to use the pipeline? Currently I'm in a team using Jira and Confluence so I think it makes sense for us to go with BitBucket since code review can easily be done in a way that ties to user stories and it is discounted with our other Atlassian products. Why don't more people that use Jira use BitBucket? And what is the best option for a company using Jira? Do we copy our BitBucket repo to GitLab, do we use GitLab and use a Jira integration but still not have our code review be able to be tied to user stories, or do we use a CI/CD manager like Jenkins which most people agree is complex to manage? What are other people doing for this? Any advice would be greatly appreciated!

#### Top Comments:

**Comment 1** (score: 87): Don't use Bitbucket Pipelines, it's not up to par

**Comment 2** (score: 32): I’m a DevOps engineer and we use Gitlab. Highly recommend it. You can integrate with Jira and it will serve you well.

**Comment 3** (score: 13): What about dagger? 


Argo workflows? 

**Comment 4** (score: 11): Gitlab integrates incredibly well with Jira. Bitbucket (and Pipelines, for that matter) Are severely limited. If you have the choice, migrating the code base is absolutely worth it

**Comment 5** (score: 68): You can outright slap someone if they suggest Jenkins in 2024. I think it’s written into most countries laws

**Comment 6** (score: 13): [deleted]

**Comment 7** (score: 6): How many developers do you have? Having a consistent UX can be important between pipelines and source control and potentially issue management. It's one of the reasons I recommended Azure Dev ops, plus they had a pretty rapid pace of feature improvement in their product.

I know you don't list it but whatever you do, do NOT use AWS for your CI CD!! Horrible for anything but the most basic use case.

**Comment 8** (score: 12): You simply choose gitlab

**Comment 9** (score: 3): Bitbucket is a poor integration with Jira, and some of the valuable features cost extra. For example, if you want useful pull request policy rules, you'll have to pay extra. Also, the PR UI is clunky and has no dark mode. 

I love Azure Pipelines. It's inexpensive and has a strong UI with many options and color themes. It integrates with most other git providers, so you don't have to move your repos to Azure Repos, but if you do you'll get a better experience. It also has a very strong security 

**Comment 10** (score: 3): Don’t use azure pipelines!! Save yourself a headache. Gitlab CI is pretty good

---
### Post 9: Gitlab CI vs Jenkins vs GitHub Actions
- Score: 138, Comments: 125
- Subreddit: r/devops
- URL: https://reddit.com/r/devops/comments/105a2bn/gitlab_ci_vs_jenkins_vs_github_actions/
- Body: I want to focus on learning CI/CD Pipelines, and have been researching which tool to learn. However, after conducting my research online, I've seen lots of convincing evidence for choosing all 3 of the tools listed in the title.

\- 'Jenkins' seems to be mentioned the most in job postings, BUT have seen a number of people say it's outdated, on the way out of the industry, and requires an excessive amount of plugins to get it in a effective state 

\- 'Gitlab CI' seems to be the second most mentioned in job postings

\- 'GitHub Actions' has direct integration with GitHub (obviously a plus) and see people say that it's easy to start using, BUT it seems to be mentioned the least in job postings.

For my final round of research on which tool to use, I want to ask this forum and will most likely pick the one the most recommended one.

Thank you for your contributions.

#### Top Comments:

**Comment 1** (score: 40): Ideally, choose something newer and learn to build badass processes with those tools. (GitLab, GH by your example)

Realistically, use the tool the company who pays you is using (then slowly push change). I acknowledge this is hard. Jenkins reusability (libraries) leaves a lot to be desired.  

For context, I was a consulting engineer using Jenkins, CircleCI, Azure Pipelines, GitLab, GitHub actions, team city, and more.  

Frankly, they do more or less the same. Understand how to build solid pip

**Comment 2** (score: 61): I have used all 3 now throughout different jobs and have to say that I am team GitLab CI all the way. I dont even work for Gitlab but will always praise their products. 

Jenkins, well everyone already said what needed to be said about it in this thread. The ONLY benefit of Jenkins is there are a shitload of stackoverflow questions and answers out there so odds are someone had a similar issue as you. It is truly the jack of all trades but master of none. Managing Jenkins versions and plugins is 

**Comment 3** (score: 14): I have enterprise experience with all three.

Github Actions is much like Gitlab CI. There is no advantage over gitlab due to being connected to github, because gitlab is also a well known repository and is directly integrated with gitlab CI as well.

They operate similarly although they have many things in how they function which are different, but in general I'd say you can put these two in the same bucket. If you learn one, learning the other will be relatively trivial. 

Jenkins is an entire

**Comment 4** (score: 10): I migrated from Jenkins to GHA, thoroughly recommend it. You can self-host your runners to reduce cost but depending on use you may be fine with team package.

Fuck Groovy.

**Comment 5** (score: 7): Don’t sleep on CodeBuild if you happen to use AWS’ CodeSuite as well. I never thought I’d need to learn it until I started at my current post, where we use AWS CodeCommit and CodeBuild quite successfully. The interface needs work, but the tooling is solid.

**Comment 6** (score: 5): Gitlab. Was a Jenkins admin since 2015. groovy is pure evil.

**Comment 7** (score: 4): I would learn both GitHub Actions + GitLab CI and add Argo CD for k8s deployments.

**Comment 8** (score: 4): As you and others said, Jenkins is on its way out the door. Do not bother. Gitlab CI and Github Actions is the same Gitlab vs. Github argument. If the employer is using Github they will likely use Github Actions and vice versa. 

Github is still the clear winner in the SaaS space so companies okay with a SaaS git provider will _most likely_ have Github. To do even some more generalizing, it is likely going to be smaller companies that are trying to run more lean that will use a SaaS git provider

**Comment 9** (score: 3): Many people here swear by GitLab CI but I am frustrated with it and prefer GitHub Actions due to many reasons like the ones I've previously listed here: https://www.reddit.com/r/devops/comments/u4nw0x/im_implementing_devops_in_my_organization_which/i4xycyj?context=3

Yea you can make GitLab work but I do have to say it's not a universally enjoyable experience. The CI/CD is pretty jank despite what the general consensus here says.

**Comment 10** (score: 28): If you want to have a miserable life - jobkins.

If you want to have an easy life - anything else that ties your hands a bit to not shoot yourself into the foot with stupid ideas.

Out of tools that are popular:

- jenkins is just cancer but a lot of postings have it coz ppl quit from there ALOT

- gitlab - is overall the best pick period, it doesnt have shitty breaches background like CiecleCI for example and you can host it yourself

- azure devops, codedeploy etc are all cloud specific (or su

---
### Post 10: GitLab deprecates Terraform templates (and recommends using OpenTofu instead)
- Score: 224, Comments: 36
- Subreddit: r/devops
- URL: https://reddit.com/r/devops/comments/1fwtmpk/gitlab_deprecates_terraform_templates_and/
- Body: [https://docs.gitlab.com/ee/update/deprecations.html#deprecate-terraform-cicd-templates](https://docs.gitlab.com/ee/update/deprecations.html#deprecate-terraform-cicd-templates)

#### Top Comments:

**Comment 1** (score: 81): > GitLab won’t be able to update the terraform binary in the job images to any version that is licensed under BSL.

The importance of OSS

**Comment 2** (score: 96): All this means is GitLab won’t provide you a pre-built pipeline. You can build your own pipeline using Terraform without issue.

**Comment 3** (score: 28): Started the switch to OpenTofu some month ago and never looked back. Hopefully the momentum stays and OpenTofu's community keeps up the good work!

Also shout-out to https://gitlab.com/timofurrer for his amazing work with the official [component](https://gitlab.com/components/opentofu)! 🥰

**Comment 4** (score: 39): Welp that's a pretty strong sign I need to start using OpenTofu

**Comment 5** (score: 1): This was already announced 9 months ago or did something change ?

**Comment 6** (score: 1): I am in dilemma now 😞. Should I start learning Terraform from scratch or start with OpenTofu since I am new to Infra provisioning. 
Kindly advice 🙂

**Comment 7** (score: 26): Honestly I don't think HashiCorp cares. Their shortminded decision to cut out anyone who isn't the end customer is a "good" decision to them. They don't want other companies using their software as part of their products because HashiCorp wants to believe they should be paid for that.

**Comment 8** (score: 4): I’ve started using OpenTofu for my side projects. I like it well enough. Felt like I was just using Terraform.

**Comment 9** (score: 30): Ehhh you can always write your own templates and use your own custom image with newer version of TF. Gitlab just cant "sell" a product that uses TF binary anymore.

**Comment 10** (score: 3): just learn open tofu as its better and say that u know both

wont be far from the truth as they are legit the same thing

---
### Post 11: How exactly does Gitlab making money?
- Score: 97, Comments: 90
- Subreddit: r/devops
- URL: https://reddit.com/r/devops/comments/17ahsqa/how_exactly_does_gitlab_making_money/
- Body: Just curious if every user is hosting gitlab on their own server. How is the "open core" model making money for them exactly? 

I mean people can host gitlab themselves, they can host any tooling themselves right?

#### Top Comments:

**Comment 1** (score: 213): Enterprise licenses are not cheap, and enterprise level features require a paid license.

**Comment 2** (score: 88): Self hosting requires you to spend time/knowledge (=money) and server resources. The managed version might be cheaper and it also contains things the open source version does not. Most Open Core products works this way - utilizing open source to spread the product and increase adoption while still monetize some customers.

**Comment 3** (score: 37): Yes, you can host the open source version, but when the requirements become 99.9 availability, backups, etc... the cost goes up a lot... to the point that it's cheaper to use the paid cloud version. Corporate also usually have a rule not to use software without support, so they pay for the support.

**Comment 4** (score: 18): its cheaper to play few hundred bucks a month to GitLab versus hiring DevOps engineer to make sure its operational don't you think? its all boils down at their prices and what is the salary of persons who can safely maintain source control systems, and normally corporations would not want to cheap out on source control as loosing source is huge productivity hit, or even being delayed when its down.

**Comment 5** (score: 9): People can host the basic version of gitlab for free. Lot of features are premium only and you have to pay for them per user basis, even if you host gitlab.

**Comment 6** (score: 8): I'm convinced people on this forum have literally no concept of service SLAs and security policies at a company.

"Why not just self host?"

Are you actually good enough to keep it up 99.99, + backups + on-call + responding to tickets?

Basically anyone can set up a standalone host in very little time if you have basic IT skills, the best IT guys work for the best companies (debatable...) and the best companies didn't get their market status by throwing shadow IT up without support etc.

GitLab 

**Comment 7** (score: 7): The open core version is also missing quite a lot of features that a pro customer would want.  The free version is the gateway drug.

**Comment 8** (score: 8): They aren't making any money with self hosted stuff, but they aren't losing any money either. So it is best to look at it as a loss leader that doesn't cost that much. Like this it does a few things:

\- Free testing for their product. Keep in mind that their customers are coders who are used to making bug reports and sending PRs.

\- Free marketing and code control. This is also why they have a free service, but basically being the software that people manage their code with is simply considere

**Comment 9** (score: 3): I personally give them $1000 a year  for my account so I think they are doing fine :)

**Comment 10** (score: 4): damn I did not know these services were very expensive lol my company must be super rich then

---
### Post 12: GitLab 12.0 released with Visual Reviews, Project Dependency List, Access Limiting by IP Address
- Score: 102, Comments: 13
- Subreddit: r/devops
- URL: https://reddit.com/r/devops/comments/c3rjxl/gitlab_120_released_with_visual_reviews_project/
- Body: [https://about.gitlab.com/2019/06/22/gitlab-12-0-released/](https://about.gitlab.com/2019/06/22/gitlab-12-0-released/)

&#x200B;

The overview of the top 3 features:

**Visual Reviews**

GitLab review applications are a fantastic tool to enable stakeholders from Operations to QA to business owners to evaluate and approve application changes before production.

&#x200B;

In GitLab 12.0, it's easy to provide visual feedback directly from the review app. It’s simple and streamlined, no toggling between different tabs and typing your feedback, helping to shorten review cycles and accelerate delivery.   
[Documentation](https://docs.gitlab.com/ee/ci/review_apps/index.html#visual-reviews-starter)

&#x200B;

**Project Dependency List**

Projects typically include dozens of individual components, which can introduce vulnerabilities. Often, security and compliance teams need to be aware of the specific components included in a project.   
[Documentation](https://docs.gitlab.com/ee/user/application_security/dependency_scanning/#dependency-list)

&#x200B;

**Limit access based on IP address**

In GitLab 12.0, you can specifically prohibit traffic from outside IP addresses from accessing your GitLab data.   
[Documentation](https://docs.gitlab.com/ee/user/group/index.html#ip-access-restriction-ultimate)

#### Top Comments:

**Comment 1** (score: 11): The extends keyword improvement seems interesting, think this, together with include, can reduce lines in the main .gitlab-ci.yml (importing logic from other library like yamls).

We have a 400 line .gitlab-ci.yml today, would like to shorten this a bit.

I also hope this can help us make global library yamls, that is shared across projects - keeping the project .gitlab-ci.yml to a minimum.

A bit sad to see Docker layer caching missing in this release. Was hoping to be able to speed up pipeline

**Comment 2** (score: 6): Gitlab are so boss. 

We're stuck on v8.x or something and it's pretty horrid compared to where they are at currently.

**Comment 3** (score: 2): looks like some great improvements

I do love how painless admin and upgrading is. although backups do take awhile

**Comment 4** (score: 3): I agree, they need to introduce something like what CircleCI has with Orbs. After the introduction it massively cut down on the length of our project configuration files. Having recently moved from CircleCI this is what I miss the most seconded by the ability to SSH into containers during runs.

**Comment 5** (score: 7): Why so far behind? They make upgrades easy too... Knock on wood!

**Comment 6** (score: 5): Why using such an old version, I update my GitLab with a CI job from within GitLab. I rarely ever have to manually intervene, usually stuff just works.

**Comment 7** (score: 5): >they need to introduce something like what CircleCI has with Orbs

This was what I mentioned would be possible (the implementation isn't as nice as CircleCI Orbs, but it is better than before). See the section on [Using extend and include together](https://docs.gitlab.com/ee/ci/yaml/#using-extends-and-include-together).

You could then create a repo with CI functionality, and include this in your .gitlab-ci.yml:

.gitlab-ci.yml in the main project

    include:
      - project: 'my-group/ci-fun

**Comment 8** (score: 4): > They make upgrades easy too

The execution is easy at least. I'm less than impressed with the actual process itself.

**Comment 9** (score: 1): I don't know. It's a massive enterprise and I'm not on the SRE team.

**Comment 10** (score: 9): Mind if I ask what you've run in to?  We've been doing the latest upgrading our development environment pretty close to when each new release comes out, then production a week later for a a couple years, just using normal yum, and we have never run in to an issue.  Jinxing it now of course though haha, but curious about what others have experienced.

---
### Post 13: How To Implement DevOps Strategy In Your Organization?
- Score: 14, Comments: 4
- Subreddit: r/devops
- URL: https://reddit.com/r/devops/comments/s25v2s/how_to_implement_devops_strategy_in_your/
- Body:  

In the past decade, there has been a huge development in networks, storage, smartphones and the cloud. Custom software development market is continuously growing and showing no signs of slowing down. Optimizing the software development process is easier than done! Challenges for businesses lies in accelerating and automating the write-test-deploy cycle without breaking anything. Here comes the need of DevOps strategy. DevOps strategy means collaborative effort between the development and operations unit.

Those days have gone when a developer would write a code and then wait for a long time to get it deployed. Implementing DevOps without any strategy might result in a disarray of activities. So as to avoid this, here we came with how to implement a clear DevOps strategy in your organization and fast-track your software delivery pipelines. But before digging into it, let’s see the overview of DevOps.

## What Is DevOps?

 

DevOps, IT philosophy and practice combine software development (Dev) and IT operations (Ops), intended to shorten system development life cycle and provide continuous delivery with high high software quality. DevOps development services correspond with Agile software development; some DevOps aspects came from agile methodology. 

Implementing DevOps amalgamates different development, operations, and testing aspects in cross-functional teams across software product or service life cycle. By bringing together collaborative teams across organization, devop

#### Top Comments:

**Comment 1** (score: 3): This is very helpful, clear and pretty extensive for people that don't know how to implement the Devops mentality, or work flow.

Was very nice to read and it answered questions at the same time got them.

**Comment 2** (score: 2): Thank you for posting this!

**Comment 3** (score: 1): I will soon be joining a startup as a product manager specifically to help align DevOps strategy from a business/operations perspective, which I've honestly never seen anywhere else before. Your post was super inspiring and gives me some awesome insight into the challenges ahead. Thanks for sharing!

---
### Post 14: The Complete Overview of DevOps Cloud Native Tools Landscape
- Score: 15, Comments: 2
- Subreddit: r/devops
- URL: https://reddit.com/r/devops/comments/dmwr6j/the_complete_overview_of_devops_cloud_native/
- Body: Cloud native technologies are revolutionizing the way applications are delivered. They serve as an excellent complement to [DevOps](https://blog.cherryservers.com/devops-full-picture-an-intersection-of-culture-processes-and-tools) by providing the tools and platforms to enable automation and scalability. However, even for those in the industry, understanding what cloud native is (and isn’t) and navigating the entirety of the cloud native landscape can be a challenge.

Fortunately, the [Cloud Native Computing Foundation (CNCF)](https://www.cncf.io/) is helping to standardize the cloud native space and making cloud native more accessible. Their [Cloud Native Landscape interactive map](https://landscape.cncf.io/) provides us with a list of tools and services that enable cloud native computing. Here, we’ll take that a step further and break down each section of the current cloud native landscape. By the end of this piece, you should have a firm grasp of the different aspects of cloud native computing, as well as an understanding of many of the most popular tools to implement them.

## What is cloud native and how does its

## landscape look like?

One of the more admirable things the CNCF has done is [give the term “cloud native” an authoritative definition](https://github.com/cncf/toc/blob/master/DEFINITION.md). It should help us avoid much of the ambiguity surrounding other terms commonly used in the industry, such as the confusion around [the differences between DevOps and Agi

#### Top Comments:

**Comment 1** (score: 4): You call out the CNCF as a source of information, but bring up the two least "cloud native" monitoring tools possible. Completely skipping the CNCF's monitoring and observability projects like Prometheus, Fluentd, Jaeger, etc.

**Comment 2** (score: 1): Thank you for your feedback, perhaps we see it from own own point of view. We will try to dig deeper and cover more tools on our next articles.

---
### Post 15: Where do you draw the line of how much developers can manage their own infrastructure?
- Score: 57, Comments: 35
- Subreddit: r/devops
- URL: https://reddit.com/r/devops/comments/1lxl2m3/where_do_you_draw_the_line_of_how_much_developers/
- Body: For context, I'm a developer who's been tasked with helping our very tiny devops team rectify our code to infrastructure pipeline to make soc2 compliance happen. We don't currently have anyone accountable for defining or implementing policy so we're just trying to figure it out as we go. It's not going well and we keep going round-and-round on what "principal of least privilege" means and how IAM binding actually works.

We're in GCP, if that matters.

Today, as configured before I started at this company, a single GCP service account has god priviledges to deploy every project to every environment. Local terraform development happens via impersonation of this god service account. Gitlab impersonates the same SA to deploy to all environments. As you can imagine, we've had several production outages caused by developers doing something unintentionally with local terraform development against what they thought was a dev environment resource and ended up having global ramifications. We of course have CICD and code reviews - we just don't have a great way to create infrastructure. And the nature of what we're building ends up being infrastructure heavy as we're rolling our own PKI infrastructure for an IoT fleet.

The devops lead and I have sat at the negotiation table litigating the solution to this to death. I can't look to a policy maker to arbitrate so I'm looking for outside advice.

Do you air-gap environments so that no single service account can cross environment boundari

#### Top Comments:

**Comment 1** (score: 39): > Do you air-gap environments so that no single service account can cross environment boundaries?

Yes. Teams get their own landing zone (network spoke and cloud project/subscription/account i.e. their own corner of the cloud). Landing zones have baseline settings through policies (e.g. public IPs are not allowed and must be approved. Often a Slack thread is enough).

> Do you allow developers to deploy to dev/sandbox/test environments?

Yes. They own all their environments. They also get access

**Comment 2** (score: 5): Why does anyone need an account that can touch prod ? Let the CI system be the only one with access to prod (under normal conditions).

You used the CI system to deploy to a test/QA/whatever environment first right ?

**Comment 3** (score: 12): DevOps owns IAM Administration. We create roles and users that allow devs to modify their respective resources and nothing else. If your deployment relies on something from another team, you do your part and submit a subsequent request for them to use their own IAM roles that allow them to deploy their part. No single account should be able to deploy everywhere.

  
If you do have a service account that can do everything, only a small handful of power users have access to that, and most likely t

**Comment 4** (score: 4): Your pipeline imo should decide who, how and after what conditions are met that a service be deployed to a given environment.  

I like two folders in GCP - prod and non-prod. Devs have god mode (minus create) in non-prod and very limited read-only in prod. 

DevOps has the same privileges. I use break glass for all privilege escalations with a timebox and enhanced audit trails. 

All builds of infra have to come through IaC, with environments forced via terraform cloud or whatever the fuck it’s

**Comment 5** (score: 6): High level architecture is normally pre decided, so it's just about giving the Devs the ability to rapidly deploy into the existing pattern. 

So DevOps team builds templates and frameworks that gives Devs the ability to build what they want but with some guard rails and alerting for going outside of best practices or existing patterns. 

When Devs want access to new patterns they request them from DevOps. DevOps delivers the pattern, Devs use it to build what they want. 

This allows for things

**Comment 6** (score: 2): [deleted]

**Comment 7** (score: 2): Depends on the dev. Some know just enough to be dangerous, some know nothing, some have been doing infra for years successfully. All devs have a different level of experience when it comes to infrastructure.

I know one who thought he was gods gift to IaC, but failed to notice the prod access keys left in the completely open repository. 

I also know one who just had to much work to do to manage his own infrastructure anymore, and he did a great job of setting it up. 

Talk to the devs, figure o

**Comment 8** (score: 3): Why the need to draw the line? If they have the means to provision the resources, then they are paying for said resources and owning all implications of what they consume.

**Comment 9** (score: 2): This is really governed by your governance, risk, and compliance requirements. Usually id you don't have a specific department for this you should ask infosec.  What do they say?

Generally each team should be able to manage their own infra via IaC. Nobody should be able to touch things in the console directly, except in a few break glass instances and that should set off alarm bells across the company.

**Comment 10** (score: 2): At a .env file.

Developers shouldn't care about where their applications are deployed to or where they live.

Developer Experience is key.

---
### Post 16: How do small SaaS teams handle CI/CD and version control?
- Score: 12, Comments: 29
- Subreddit: r/devops
- URL: https://reddit.com/r/devops/comments/1m6d5ep/how_do_small_saas_teams_handle_cicd_and_version/
- Body: Solo dev here, building a multi-tenant Laravel/Postgres school management system.

I’m at the stage where I need proper CI/CD for staging + prod deploys, and I’m unsure whether to:

* Self-host GitLab + runners (on DigitalOcean or a personal physical server)
* Use GitHub/GitLab’s cloud offering

My biggest concerns:

* **Security/compliance** (especially long-term SOC2)
* **Secrets management** (how to safely deploy to AWS/DigitalOcean)
* **Availability** (what if the runner or repo server goes down?)

Questions:

1. Do you self-host version control and CI/CD? On your cloud provider? Home lab?
2. How do you connect it to your AWS/DO infra securely? (Do you use OIDC? SSH keys? Vault?)
3. For solo devs and small teams — is it better to keep things simple with cloud providers?
4. If I self-host GitLab, can it still be considered secure/compliant enough for audits (assuming hardened infra)?

My plan right now is:

* GitLab on a home server or a separate DO droplet, harden everything with Keycloak and Wireguard
* Runners on the same network
* Deploy apps to DOKS (or ECS later)

Would love to hear how others manage this.

Thanks!

#### Top Comments:

**Comment 1** (score: 11): So far, I've always just used GitHub Cloud.

- This makes security/compliance very easy.
- Secrets for CI can also be managed in a default way
- Availability is higher than for self-hosted variants.

Main drawback is that it costs a bit of money.

**Comment 2** (score: 6): Self hosting gitlab seems like overkill, why not just use Github ci? This is all solved, don't reinvent the wheel

**Comment 3** (score: 4): Major banks use GitHub and Actions, so I don’t think it should be a concern for you.

The only concern with GitHub or another SaaS CI/CD in your situation would be running costs, for example if you want to establish Org on GutHub, you will pay per member per month + there is a cap in free usage of runners for your workflows.

You don’t want to host your CI/CD in a garage, this will be a HUGE no for auditors, it’s not even worth considering.

So the only real choice here is use SaaS CI/CD or host

**Comment 4** (score: 2): For my personal projects dev goes to my development infra runs automated tests and then either auto merges to main or for the projects that require some manual tests, opens a MR and adds a comment for the manual test steps, then I can tag off main and deploy that to preprod and prod as and when I want to deploy new features.

I have got some projects that I auto tag off main and deploy as well.

This all happens on a helm chart repo, the apps have pipelines that run unit tests, build the new ima

**Comment 5** (score: 1): Laravel guy here too! Self-hosting can work, but for small teams it’s usually not worth the extra hassle. But of course depends on the use-case. GitHub Actions or GitLab SaaS + DigitalOcean works great, you get solid CI/CD, OIDC support, and can deploy to DOKS or Droplets easily. As you are solo, I would personally try to focus on shipping, not managing infra unless you have the extra bandwidth of course!

**Comment 6** (score: 1): [deleted]

**Comment 7** (score: 1): Ci/cd hosting is not our business, so we do not do it ourselves. GitHub actions for deployment pipelines, GitHub secrets for whatever keys are needed to make calls to cloud resources for deployments. Version control is of course with GitHub as well.

GitHub and gitlab meet most compliance certifications, so nothing to worry about there. If they don't meet something you need, you probably have a shed load of money for a team to manage an alternative.

For availability, GitHub's availablity is fin

**Comment 8** (score: 1): For a solo dev and laravel it all sounds like overkill.

Look into platforms that do it all for you like heroku etc.

**Comment 9** (score: 1): This kind of stuff is usually not mission critical, especially for solo dev. Like what happens a pipeline doesn't run for a while? Yeah developers are annoyed, but they can mostly go on working. In solo dev scenario, you will likely be able to do the stuff manually in case something breaks and you need emergency build/deploy.

If you like selfhosting, think about Gitea/Forgejo before you jump into GitLab. Gitlab is pretty massive thing to handle (though it is very well documented and automated).

**Comment 10** (score: 1): That makes sense.

Out of curiosity, did you consider self-hosting GitLab on any cloud instance?

Would compliance be an issue? Even if my cloud provider meets some of the compliance required?

Or possibly using gitlab cloud, but self hosting runners only.

Assuming you're okay managing backups and updates, is there a strong reason not to go that route. I'm wondering if the tradeoff in effort is worth the control you gain (e.g., unlimited private runners, tighter integration, cost savings long-t

---
