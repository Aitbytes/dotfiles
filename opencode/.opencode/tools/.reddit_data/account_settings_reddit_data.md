# Reddit Data - account settings

## Collected Posts and Comments

### Post 1: I planted fake API keys in online code editors and monitored where they went. CodePen sends your code to servers as you type.
- Score: 1441, Comments: 171
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1rj1oac/i_planted_fake_api_keys_in_online_code_editors/
- Body: I've been auditing the privacy practices of developer tools. This time I tested what happens to your code in online editors.

Test data: const API\_KEY = "sk-secret-test-12345"; const DB\_PASSWORD = "hunter2";

CodePen The moment you type, your code is sent to CodePen's servers via POST requests to codepen.io/cpe/process (Babel transpilation) and codepen.io/cpe/boomboom/store (preview rendering). You don't need to click Save it happens in real-time. My fake API key was transmitted verbatim in the request payload. All pens are public by default and auto-licensed as MIT. Private pens require PRO.

JSFiddle Code is sent to [fiddle.jshell.net/\_display](http://fiddle.jshell.net/_display) every time you click Run. For logged-in users, auto-save runs every 60 seconds, and auto-run fires after a 900ms debounce on every code change. Fiddles are public by default and indexed by Google. Three ad networks loaded (Carbon Ads, BuySellAds, EthicalAds). Their iframe sandbox configuration has an escape vulnerability logged in the console.

CodeSandbox Runs 6 separate analytics services: PostHog, Amplitude, Plausible, Cloudflare Web Analytics, Google Analytics, and Google Tag Manager. All code stored server-side. Public by default on free  tier. Their Terms prohibit using code for LLM training, but their Privacy Policy lists "LLM providers" as third-party data recipients. Those two statements directly contradict each other.

Replit This one floored me. A single page load generated 316 network

#### Top Comments:

**Comment 1** (score: 1042): Only an idiot would be putting their private API keys in a public code editor though, right?

Right?

**Comment 2** (score: 146): >developers use these tools to write code that handles user data responsibly

In theory, some do, but my experience says it's a really small percentage...

**Comment 3** (score: 60): The more interesting thing to do would be to plant low-privilieged tokens to high impact services (like AWS), and monitor how fast it was til you planted those tokens- > usage 

**Comment 4** (score: 82): I fail to see what your fake API keys in this story have to do with anything? Can you elaborate? It seems like the same outcome regardless if you put fake API keys in or not

**Comment 5** (score: 35): That's been standard practice for these editors since forever, they need your code server-side for features like autocomplete and previews to work at all.

---
### Post 2: I wanted to share some Front End practice interview questions, after interviewing and finding it nothing like Leetcode
- Score: 961, Comments: 168
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/hyuznw/i_wanted_to_share_some_front_end_practice/
- Body: I recently spent some time preparing for Front End interviews and found the suggested 'Software Engineer' interview prep pretty lacking: **the common advice is to spend most of your time grinding Leetcode and, for Front End interviews, get ready for countless** [trivia-style questions](https://github.com/h5bp/Front-end-Developer-Interview-Questions)**.**

After half a dozen interviews with Bay Area companies, I personally experienced just one Leetcode-style algorithmic question (a pretty basic graph question) and zero FE trivia questions.

**My interview experience was roughly: 25% culture fit, 25% system design/experience (e.g. discussing a project I worked on and choices I made), and 50% practical Front End coding.**

This also matches my experience as an interviewer at my previous company, where we phased out both algorithmic and trivia questions (in favor of practical FE coding) after finding they were poor indicators of future success.

IMPORTANT NOTE: your experience may vary, especially with companies based in other states or countries!

I feel like there's a huge lack of practice questions suited for practical Front End interviews, so **I wanted to share a handful of my favorite Front End coding practice questions** (with slight variations) that came up for me. But first, a few tips for getting the most out of these practice questions:

* Use [codepen.io](http://codepen.io) \- I was asked to use this in nearly every interview. Get familiar with the environment: shortc

#### Top Comments:

**Comment 1** (score: 230): Wow, 60 minutes to implement snake and 60 minutes to implement a carousel? Something doesn't seem to add up there. Seems like enough time for a simple carousel.

**Comment 2** (score: 41): Was this a 12 hour interview?

**Comment 3** (score: 109): Building a snake game in 60 minutes is an absolute nonsense.

To be honest, doing any of these tasks in 60 or less minutes in absolute nonsense.

I'm not saying it's impossible, but if you want me to write good code (which should be the main goal of you as a programmer or them as a company looking for programmers) I am not doing anything like that in 60 minutes.

I don't know which companies you have applied for, but I either had questions that took 10 seconds to answer or I had a week or even a

**Comment 4** (score: 19): I couldn’t do any of this, I’d just steal some office supplies and leave.  When somebody wants me to paint their house they don’t have me paint a wall for free while they stand over my shoulder, I paint their damned house and if they’re happy I get paid. 

What’s wrong with grabbing the best resume,  taking a look at their portfolio, hiring the person to do something small, when they complete it pay them (radical concept, I know) and if they’re good hire them full time.  

Performing circus tric

**Comment 5** (score: 39): ...This is not for entry level positions right? Because Im self taught and youre freaking me out Lol

---
### Post 3: I stumbled on the sun's article and saw this cookie consent popup, is this legal?
- Score: 956, Comments: 276
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1noi8mx/i_stumbled_on_the_suns_article_and_saw_this/
#### Top Comments:

**Comment 1** (score: 715): Yup - either way you give consent

Lots of news outlets have discovered this unfortunately

edit: ICO Comment https://cy.ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/online-tracking/consent-or-pay/about-this-guidance/#what

**Comment 2** (score: 281): Shit rag with a shit policy.
Income across that shit I just nope out.

**Comment 3** (score: 190): This is a GDPR "loophole" that a lot of news sites use here in the EU.

It's legal because they're not required to provide you a service. If you don't want to consent you can theorically just not use their website.

The EU doesn't prioritize/want to fix this loophole because this trick is used by a lot of news organizations that already struggle financially, and removing this option from them would hurt them even more financially as less people would subscribe or pay. Which in the end would resu

**Comment 4** (score: 17): You can read on it here: [https://www.cookieyes.com/blog/cookie-wall/](https://www.cookieyes.com/blog/cookie-wall/)

**Comment 5** (score: 34): The _Saddam Hussein_ of parasitic shitrags.  

Don't give them the time of day. Move on.

---
### Post 4: GoDaddy sent us a bogus malware report, threatens us with suspending our domain and tries to up-sell us their "security" package.
- Score: 880, Comments: 193
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/caymdf/godaddy_sent_us_a_bogus_malware_report_threatens/
- Body: GoDaddy sent us a malware report, that our subdomain allegedly hosts malware, and might be suspended if we don't remove it in 24 hours, which in effect could sink our company, as this is a domain that our company SaaS platform is available at.

All our subdomains host the same SaaS app with different configurations, so the fact that malware was detected on only one of them is interesting by itself, and all  they provided us is the subdomain address, and generic advice of "update your wordpress, and change your FTP password" kind, which is not very helpful, as we don't have any of those. We are running in Azure Kubernetes Services, so we don't have hosting with GoDaddy, only domain registration.

There is no alert available in the GoDaddy web portal, or there is but its not loading for me, as I'm using delegated access to another account, and domain list does not load for me. Nice IAM.

[Google](https://transparencyreport.google.com/safe-browsing/search) and some other less known "security checkers" raise no concerns for our website. I've also checked the sources served to browser, our sources are fine, and no external resources are loaded.

Here is the fun part:

* alert email was written in Polish (we are a Polish company)
* tech support phone number is in Warsaw local area code
* tech support does not speak Polish
* tech support cannot read and comprehend the alert email, as it was written in Polish
* tech support cannot tell me what made the malware alert go off, but I can

#### Top Comments:

**Comment 1** (score: 395): GoDaddy have a *long* history of being an ass with its customers.

Glad (or sad) to see that it haven't changed.

**Comment 2** (score: 204): Why are people still buying stuff from GoDaddy?

**Comment 3** (score: 77): Get a transfer code and gtfo with your domain there... today!

**Comment 4** (score: 68): Godaddy sucks. I wouldn't work for them or use their services. They don't care about their customers, only their money. They push sales on every person who calls, whether it's for a service they would benefit from or not. In fact, most of the crap they sell people, the buyers don't even know what it is they've bought, or how to set it up. 

&#x200B;

I've had instances where I've called them, they have no idea what they're talking about, and quickly try to sell me their most expensive products w

**Comment 5** (score: 25): \>  GoDaddy spotted we have a subdomain with our clients name, and their logo on our LP, PHISHING was suspected, they send us MALWARE email alert

I wonder if the intention was to resolve the security issue and sincerely push the security package on you or if it's an exploitative tactic to push more of their services.

&#x200B;

I work in Cyber Security and I can honestly attest that there is a great number of legitimate websites that are exploited for pushing scams and malware and unfortunately

---
### Post 5: I'm a front-end engineer who loves building side-projects. My latest is an AI Art Generator app. Here's how I built and launched a fairly complex app in under a month thanks to some good choices of technology.
- Score: 633, Comments: 54
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/f14dqf/im_a_frontend_engineer_who_loves_building/
- Body: Hi r/webdev, I'm a front-end engineer who loves building side-projects. My latest is an AI Art Generator. In this article I talk about the technology choices I made while building it, why I made them, and how they helped me launch the app a lot faster than I otherwise would have been able to. Note: I originally posted this on [Medium](https://medium.com/@angus.russell89/anatomy-of-an-ai-art-generator-app-13259e438ce5). I've stripped all mentions of the actual app to comply with this sub's self-promotion rules.

https://preview.redd.it/z9kzq8l24uf41.jpg?width=1600&format=pjpg&auto=webp&s=ff0a8b5573676997b62f9317d64f957fa94f4945

# First, a brief timeline

**October 14, 2019** — Looking back at my commit history, this is the day I switched focus from validating the idea of selling AI-generated artworks, to actually building the app.

**October 28** — 2 weeks later I sent a Slack message to some friends showing them my progress, a completely un-styled, zero polish “app” (web page) that allowed them to upload an image, upload a style, queue a style-transfer job and view the result.

**October 30** — I sent another Slack message saying “It looks a lot better now” (I’d added styles and a bit of polish).

**November 13** — I posted it to Reddit for the first time on r/SideProject and r/deepdream. Launched.

# Requirements

A lot of functionality is required for an app like this:

* GPUs in the cloud to queue and run jobs on
* An API to create jobs on the GPUs
* A way for the client 

#### Top Comments:

**Comment 1** (score: 26): Art style looks very cool! Nice work

**Comment 2** (score: 12): Nice post, but you're not talking about the AI bit at all, which in my opinion is the most interesting part... :-(  
How do you actually make those generated pictures?  
Did you make the algorithm / AI yourself?

**Comment 3** (score: 19): There's show off Saturday in this subreddit, and as far as I'm aware, it's still Saturday here. So technically you could put your app name? I'm no mod though.  


Anyway, nice work and nice post!

**Comment 4** (score: 16): I'm a front end dev who never builds side projects. You guys play your cards right and maybe I'll show off that button I made that launches a modal but never did anything else with.

**Comment 5** (score: 7): What kinda costs are you looking at for Firebase and Algorithmia?  They sound like nice products... almost too nice?

---
### Post 6: I built an open source Heroku that costs 1/10th as much to use
- Score: 594, Comments: 59
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1jca7oa/i_built_an_open_source_heroku_that_costs_110th_as/
- Body: I've been working on [https://canine.sh](https://canine.sh/) for the past year. Tldr: its your run of the mill Heroku, Flyio, Render, etc, except that its fully open source, and free to use (including just using the cloud hosted option) 

Built it based on some learnings I've had in the past building startups where we quickly outgrew the single VPS type deployments, moved onto managed platforms like Heroku and Render, and watched our costs explode, with an annoying amount of vendor lockin. Our peak year, we hit over $400k in hosting costs.

[Made with shots.so](https://preview.redd.it/iz76slvhcyoe1.png?width=1920&format=png&auto=webp&s=bb271c7d861b0b9748490559b719da67833cfe88)

Goal for this project was to build something that indie hackers can start with and get up and running fast, but has no problem being flexible enough to scale to future needs.

Managed Kubernetes is now widely available and dirt cheap ($10 / month), so you don't have to worry about, and supported by pretty much every single cloud vendor.

This lets you take advantage of a ton of things that Kubernetes does really well, like automatic healthchecks, zero downtime deployments, auto scaling, etc, while also making it easy to use for solo developers or small teams.

The additional benefit of Kubernetes is that it's also possible to host a bunch of other stuff in your cluster via Helm charts, that you’d normally have to pay for like:

* Sentry
* Wordpress
* Metabase
* Dagster
* Airflow
* MongoDB
* Redis
* Pos

#### Top Comments:

**Comment 1** (score: 80): Sounds interesting. What would you say is the biggest difference / benefit to Coolify?

**Comment 2** (score: 32): Great project and really nice landing page, looking forward to use it. I was looking for a solution like this, currently using  coolify

**Comment 3** (score: 16): This is fricking amazing OP. I was searching for something like this too. Let me spend some time experimenting with this. When you mention cloud hosted. How does it work out. I don't see a pricing page in there

**Comment 4** (score: 13): This looks really great and I'd love to try it, but I'm not seeing a way to sign up that doesn't grant a crazy level of GitHub permissions, both to personal and organization level repositories, so that's a no go for me unless I create a burner GitHub account. Would love to try it with a personal project but can't grant the organization level permissions. Can they be made optional?

**Comment 5** (score: 7): That's awesome! How does it compare performance-wise to [Fly.io](http://Fly.io) and Render?

---
### Post 7: Regularly Scheduled 'GoDaddy Fucking Sucks' Post
- Score: 572, Comments: 154
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/h0t8iu/regularly_scheduled_godaddy_fucking_sucks_post/
- Body: Trying to get a client's site live last minute because stupid reasons. Whatever, standard WP site. They have GoDaddy, cheapest Managed WordPress plan. I usually use AIO WP Migration to move simple sites around. Exported and the zip is 384MB and then realize GoDaddy has a 100MB upload limit set for the shared server. Tried creating a php.ini, no dice. Tried setting ini vars in the wp-config, no dice still. Finally, tried throwing the lines into the htaccess and still no dice. All of a sudden, 500 error! So I go back to edit the htaccess file and some automated system has locked the file and then the GoDaddy File Browser in the account dashboard isn't loading. Great! Tried SFTP but, surprise!, the server is timing out so I can't even FTP in to tickle the htaccess.

&#x200B;

I'm now on a live chat with some dude who takes literally two to three minutes to respond. I told him the issue and his suggestion is to wait for DNS to propagate. I am so upset and tired and I just want to go to bed.

&#x200B;

Don't use GoDaddy and don't let your clients use GoDaddy.

&#x200B;

What's your latest shitty hosting horror story?

#### Top Comments:

**Comment 1** (score: 109): Their tech support is really hit or miss. I've had techs who really knew what they were doing, and some who were as useful as argumentative eggplants. If you get a dud, hang up and try again. I'm convinced I've saved hours of time by doing so.

**Comment 2** (score: 113): They removed old PHP version(Dont remember which exactly, but not that old) from their linux hosting without warning and instead of switching to the next oldest version they just switched to latest and a forum website my client was hosting dropped. 

like wtf

**Comment 3** (score: 46): My shitty hosting horror story starts with a freelance project that I was being heavily underpaid for. The client was going to arrange their own hosting and I tried advising them to pick some easy solution but instead they chose to handle it via some guy who had his own company making and hosting simple websites. He himself wasn't hosting anything, he was using a different small-time shared hosting service.

This basically meant that he didn't have any access to the server beyond the standard ph

**Comment 4** (score: 24): For future reference, you can selectively export from AIO WPM if you don't want or can't deal with large single-file uploads. What I used to do to get around limits like this was just export everything but the media library with AIO, and then use FTP to upload the rest. The big selling point of AIO is not having to micromanage the database migration, URLs, permalinks, precariously configured plugin ecosystem, etc. FTPing the uploads folder is time-consuming but really straightforward.

I feel yo

**Comment 5** (score: 23): [removed]

---
### Post 8: That time we had to change someone’s name because of a coding decision.
- Score: 558, Comments: 110
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/188vrbo/that_time_we_had_to_change_someones_name_because/
- Body: No, not their username.  Their name. 

The place I work uses Google Workspace for some things and we discovered a giant problem In their coding.  They admit to it but have yet to fix it.

The error is innocent enough.  The user tries to log in and sees "This account cannot be accessed because the login credentials could not be verified."

[https://support.google.com/a/answer/2463723?hl=en&ref\_topic=7579248&sjid=17207273433788812640-NC#zippy=](https://support.google.com/a/answer/2463723?hl=en&ref_topic=7579248&sjid=17207273433788812640-NC#zippy=)

But why?  We do your basic troubleshooting, it’s not their username or password.  It’s not MFA.  We contact support.

It’s their name.  It’s their non-American name more correctly. 

This issue relies on two things being true

1. You implement third party SSO.  We did of course.
2. people must have accent marks in their names.

That Google article links to a Wikipedia article.   The issue is their SAML assertation fails if your first, last or full name has any characters not on that list.  Thst’s right, an International company implemented a character set that doesn’t include accent marks.

[https://en.wikipedia.org/wiki/ASCII#Printable\_characters](https://en.wikipedia.org/wiki/ASCII#Printable_characters)

Among that page is the 1977/1986 ASCII tables. That’s what characters people can have in their first or last name.  If your name is André you must change the spelling of your name. You must become Andre.  Pronounced differently i

#### Top Comments:

**Comment 1** (score: 505): [deleted]

**Comment 2** (score: 151): Some motivation:

https://gdprhub.eu/index.php?title=Court_of_Appeal_of_Brussels_-_2019/AR/1006

>The Court of Appeal of Brussels held that data subjects have the right under Article 16 GDPR for their name to be spelled correctly when processed by a bank's computer systems.
>
>[...] The Court of Appeal of Brussels held that, in accordance with Article 16 GDPR, the data subject has the right for their name to be correctly spelled when processed by the computer systems of the Bank. To claim in 201

**Comment 3** (score: 85): I have accents in all 3 of my names, but I rarely use them when signing up. I live in an English speaking country and it's just easier not to confuse people with them.

To answer your question, my bank didn't support accents when I signed up 6 years ago.

**Comment 4** (score: 24): I can't even use the hyphen in my name in a lot of places.

**Comment 5** (score: 22): Mandatory relevant xkcd https://xkcd.com/327/

---
### Post 9: A lot of websites use javascript "buttons" instead of hyperlinks, which prevents you from opening things in a new tab. Does this serve any kind of real purpose or is it just the company needlessly forcing you to use the site a certain way?
- Score: 490, Comments: 217
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1av6a50/a_lot_of_websites_use_javascript_buttons_instead/
- Body: I say "buttons"  because often times they aren't really buttons, they just look like what would normally be a hyperlink, but it still behaves like a button, in that you can't hover over it and see a URL or open it in a new tab.

I'm currently on OfferUp on a search page, and I tried to open my account settings in a new tab and I noticed that my browser didn't  detect it as a link, which I've seen thousands of times before, and it made me wanna ask.

https://i.imgur.com/m7q2gLx.jpeg

Just curious if there is any actual good reason to do this?

#### Top Comments:

**Comment 1** (score: 154): This is horrible for accessibility, btw

**Comment 2** (score: 919): In my experience, it's devs not knowing semantic HTML and designers not giving 2 shits.

**Comment 3** (score: 67): If the result of clicking something will be a navigation event, it should be an anchor, never a button. Doing otherwise is being a baddie.

**Comment 4** (score: 317): Buttons do things, links take you places. If you don't follow this principle, you make your site less accessible to visitors.

**Comment 5** (score: 74): There is no good reason. If it takes you to a different page it should be a link I.E. an anchor tag.

Similarly if it triggers an action without navigation it should be a button or at least have `role=button` and the accompanying accessibility features.

---
### Post 10: A Couple of Things I Noticed When Remaking the Google Homepage
- Score: 476, Comments: 111
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/e9n6xq/a_couple_of_things_i_noticed_when_remaking_the/
- Body: Hey all, again!

I decided to further my learning by starting The Odin Project. As always, I decided to start from the beginning regardless of my prior knowledge -- I like to do things from the start as I find I always notice something which I can improve on, regardless of the level of developer the module is intended.

When completing the remake Google's homepage project I noticed a few things which I found pretty strange/I hadn't seen in practice/mentioned elsewhere so thought I would ask on here.

Namely those things are as follows:

1. They seem to place their meta tags within the document's body -- Is there a reason for this? I always thought that meta tags had to live in the head.
2. The entire Google homepage seems to be wrapped in a div with `id="viewport"`. The CSS which goes along with it, from what I can see, simply sets the position to be `absolute` and then makes it fill the page:

&#8203;

        position: absolute;
        top: 0;
        width: 100%;

3. Making an element for positioning text -- Google's homepage seems to implement a HTML tag call `<center></center>` which has the purpose of aligning all text within the element centrally. Does anyone know if this is a good idea to translate to other projects or if there is any reason for doing this beyond ye olde DRY methodology? This is the CSS which goes with it:

        display: block;
        text-align: -webkit-center;

Anyway, as always, thank you in advance!

EDIT:

Wow, so many replies! Thank you all

#### Top Comments:

**Comment 1** (score: 111): The Google homepage is probably *the* most trafficked page on the internet. As such, they have many concerns that most sites will never have.

My guess is that a lot of those oddities you’ve noticed boil down to two things:

1.	Code golf - making the payload smaller by using a variety of hacks and tricks that aren’t really “best practice,” but make the footprint smaller
2.	browser support

**Comment 2** (score: 195): "Do as google says, not as google does."

**Comment 3** (score: 137): You may be interested to learn that at Google, there is not an HTML file (or files) for the homepage. In fact, it's a program written in C which is used to generate it.


Source: I worked there and was on the team responsible for manually changing the "homepage" to launch Google Doodles. I also designed and built a system to automate the process.

**Comment 4** (score: 80): No idea what the answer is to this, but I’m chucking an upvote to hopefully get this post some recognition. Some quality questions!

**Comment 5** (score: 24): 1. I haven't kept up closely with Page Rank but I vaguely remember reading many years ago that they were starting to ignore the head META tags when it came to determining Page Rank. Maybe they still use them when placed in the body? It's just guessing though since none of us know what their bots are doing.

---
