# Reddit Data - programming

## Collected Posts and Comments

### Post 1: Study Finds That 52 Percent of ChatGPT Answers to Programming Questions Are Wrong
- Score: 6399, Comments: 812
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/1czk8nv/study_finds_that_52_percent_of_chatgpt_answers_to/
#### Top Comments:

**Comment 1** (score: 2876): I don't mind that it gets things wrong, English can be ambiguous sometimes.

But I do hate getting stuck in the loop of

"You are correct. I've made those changes for you"
 *has changed absolutely nothing*

**Comment 2** (score: 671): it generates code calling APIs that don't exist.

**Comment 3** (score: 284): Personally feel like the stack overflow answer that has been scrutinized by human beings who love to prove people wrong is still unbeatable for me. If someone makes shit up it'll get downvoted and people will get off on telling them they're wrong and why. As opposed to ChatGPT making shit up and I spend as much time implementing it myself as reviewing the code to make sure it's actually doing what I want.

For really simple tasks like making a skeleton and stuff like that sure but my first insti

**Comment 4** (score: 271): My favorite thing to do with ChatGPT is have it explain a line of code or a complex command with a bunch of arguments. I've got some openssl command with 15 arguments, or a line of bash I don't understand at all. 

It's usually very accurate and much faster than pulling up the actual documentation. 

What I absolutely won't do anymore, is ask it how to accomplish what I want using a command because it will just imagine things that don't exist. 

> Just use -ExactlyWhatIWant

Only it doesn't exis

**Comment 5** (score: 29): These models don't tell you the correct answer. (They don't know anything like that) 
They will tell you an answer that has a high probability of "this is what the correct answer LOOKS LIKE." Which is similar but not the same.

**Comment 6** (score: 22): If you're using ChatGPT to give you the answer, you're deing it wrong. 

I use it to sanity check ideas, stress test my reasonings, and explore ideas that might not have occured to me.

If you're asking it with the hope of it being a solution generator, I thank you for my job security.

**Comment 7** (score: 38): I've had ChatGPT just make up functions that aren't in the API lol.

> Hey ChatGPT. How do I do something in this programming language?

> Very easy just use the DoSomething() function

> That function doesn't exist...

> I'm sorry. You're right. Try this..

>    public DoTheThing() 

>    {

>        DoSomething();

>    }

**Comment 8** (score: 205): Have been using GPT-4 pretty heavily to generate code for rapid prototyping the last couple of weeks and I believe it.  The first answer is easily off if the question wasn't asked precisely enough.  It takes some iteration to arrive at what looks like an acceptable solution.  And then it may not compile because GPT had a hallucination or I'm using a slightly different runtime or library.

Its the same old 'garbage in, garbage out' as always. It is still a really powerful tool, but even more dang

**Comment 9** (score: 48): 48% of the time, it works every time.

**Comment 10** (score: 65): [deleted]

---
### Post 2: Google's Shift to Rust Programming Cuts Android Memory Vulnerabilities by 68%
- Score: 3388, Comments: 477
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/1iub0rk/googles_shift_to_rust_programming_cuts_android/
#### Top Comments:

**Comment 1** (score: 864): That's nice

**Comment 2** (score: 318): Nice, albeit pretty expected, result. But what about the other categories of vulnerabilities? How have they looked pre- and post-Rust?

**Comment 3** (score: 188): Using a language with high memory safety reduces memory vulnerabilities 😱

In seriousness, it’s interesting to hear how they consider their approach of just doing new code in Rust and leaving well enough alone for the old code has worked for them.

I have to wonder if Linux kernel development/maintainers could learn from this.

**Comment 4** (score: 84): [deleted]

**Comment 5** (score: 9): How am I going to root my future phones?

**Comment 6** (score: 21): The article says that it is not only the move to Rust but a more general move to a different paradigm with regards to safety.

**Comment 7** (score: 69): Transitioning to Rust, from what?

It's popular to bash C++, but straight C is where simple string concatenation introduces vulnerabilities if not done right. I'd be curious to see the analysis of those vulnerabilities in the first place.

**Comment 8** (score: 17): I agree with the idea, but holy cow.  Can these guys please speak like a human?

> Adopting Safe Coding in new code offers a paradigm shift, allowing us to leverage the inherent decay of vulnerabilities to our advantage, even in large existing systems

Would it have been so hard to say "Vulnerabilities in old code tend to get fixed over time, so preventing them from happening in new code gets us more value than you'd expect."?

**Comment 9** (score: 50): Hypothetically if all existing C++ code was replaced with modern C++, only smart pointers and "strict memory safe practices" for all new code would it yield the same results?

Edit : read Google's blog about this topic. It's not simply the case of switching out C++ with Rust. It was also making sure that all NEW code adhered to strict memory safety guidelines. The language is just a tool. What you accomplish with it depends on how you use it.

**Comment 10** (score: 22): I just searched a popular job site nearly 5K C++ jobs, around 800 Rust.

---
### Post 3: Why Electronic Voting is a BAD Idea - Why you can't program your way to election integrity
- Score: 864, Comments: 1009
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/1p5m5n2/why_electronic_voting_is_a_bad_idea_why_you_cant/
#### Top Comments:

**Comment 1** (score: 132): Damn it i thought tom scott came back for a second

**Comment 2** (score: 664): This video is 10 years old. Anything happened recently that makes it relevant?

**Comment 3** (score: 89): The main argument _for_ non electronic voting is the one he says at the start of the follow-up video: attacks don't scale very well. And I think it's a very good argument. 

Still, I've watched this video and the follow up some times, and I've always felt they are kinda... low effort, research wise? 

Tom brings up good thought exercises and things to question, but he shows few actual data and sometimes the argument is ["no one does that"](https://youtu.be/LkH2r-sNjQs?si=otMfsb2BR4CASvh4&t=342),

**Comment 4** (score: 192): As someone who actually works in the industry, the machines and software of today that allow people to vote and to count those votes are indeed audited and tested not only by security companies, but also the Department of Homeland Security.

Any time there is a new version of these machines and softwares developed, all of them are audited, tested and authorized on a state by state basis before they are put into use in any election in those states.

Voting where it is right now, is the most secur

**Comment 5** (score: 7): People don't trust digital votes, yet they do trust that their lives savings are just bits in some database somewhere. Newsflash that one is also behind several layers of interleaving ledgers that are all checked regularly against each other to spot fraud, or mistakes, early on.

**Comment 6** (score: 6): Interestingly enough India and Brazil are the largest democracies in the world and they use e-voting.

A bit strange that the video neglects to discuss the election system of those countries much at all.

**Comment 7** (score: 71): It’s strange that Estonia doesn’t have a problem with that

**Comment 8** (score: 8): Electronic voting isn’t a perfect solution I agree.

However…

Last time I went to vote, the officiating staff crossed the wrong name off, and then subsequently asked me to go back into the booth to vote a second time as I was still on the list.

I fail to see how a collection of bumbling humans is any safe to be honest…

**Comment 9** (score: 17): There was a discussion on this very topic on r/rust, a week or so ago.

To summarize, there are multiple potential issues to be wary about with regard to elections. Off the top of my head, something like:

 1. Identity Theft: ie, I vote in your stead.
 2. Coercion (vote): ie, you vote, but I look over your shoulder to make sure you vote the right way.
 3. Coercion (post-facto): ie, you voted on your own, but I double check that you voted the right way.
 4. Corruption (transit): ie, you vote A, b

**Comment 10** (score: 18): Brazil disagrees. Eletronic voting has been going on since the 90's and it's a huge success. 100M+ people vote every 2 years and no fraud has ever been proved. It's extremely efficient, we know the results country wide in a few hours.

---
### Post 4: r/programming should shut down from 12th to 14th June
- Score: 13397, Comments: 534
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/141oyj9/rprogramming_should_shut_down_from_12th_to_14th/
#### Top Comments:

**Comment 1** (score: 194): What are good Reddit alternatives?

**Comment 2** (score: 1037): lol. The mods of this subreddit are reddit employees, including the CEO as 2nd mod. They aren't shutting it down.

**Comment 3** (score: 842): I’ve been supporting reddit since 2010. Reddit gold. 

How much is the data worth?

How much is everyone’s support worth? That’s a better question. 

Don’t trade your future for a quick payday, Reddit. 

Premium was supposed to be the alternative to selling the users out like Facebook.

Hmmm, that reminds me. Did you ask redditors what they wanted for Reddit?

**Comment 4** (score: 1336): APIs are our lifeline.

**Comment 5** (score: 207): Just for 2 days? C'mon. A PROGRAMMING sub of all things should know the implications of what reddit is doing. Shut down until better terms are offered.

**Comment 6** (score: 66): Two days will not matter. Shut down until Reddit reverses course.

**Comment 7** (score: 317): [deleted]

**Comment 8** (score: 85): No, it should shut down until we get what we want.

**Comment 9** (score: 42): These temporary shutdowns are pointless. Just shut down the entire sub indefinitely until they reverse decisions. It's not like anybody's losing anything. Mods don't exactly get paid to run this place, and any discussions or information to be had can always be found elsewhere. It's not like Reddit is ground zero for humanity's knowledge.

Maybe it's time for Reddit to meet its demise considering it's pandering to ridiculous bullshit lately.

**Comment 10** (score: 32): Shameful Reddit bots abound: https://i.imgur.com/omrm3Yw.jpg

[Comment 1 ](https://www.reddit.com/r/programming/comments/141oyj9/rprogramming_should_shut_down_from_12th_to_14th/jn3op6b/)

[Comment 2](https://www.reddit.com/r/programming/comments/141oyj9/rprogramming_should_shut_down_from_12th_to_14th/jn3tuq0/)

Edit - [mofos just don't stop ](https://i.imgur.com/gph8iU8.jpg)

---
### Post 5: [Serious]Former teens who went to wilderness camps, therapeutic boarding schools and other "troubled teen" programs, what were your experiences?
- Score: 34720, Comments: 3979
- Subreddit: r/AskReddit
- URL: https://reddit.com/r/AskReddit/comments/c7ldpc/seriousformer_teens_who_went_to_wilderness_camps/
#### Top Comments:

**Comment 1** (score: 6578): My father lost custody of me for domestic violence and I got scooped up by CPS and put into the group home system. He got custody back a couple of months later and I ended up running away. They sent me to a place called "Vision Quest," which was a place with troublemakers, but not that bad. The thing that was bad was that there wasn't any food. I was eating little single serving cups of cream cheese. Ended up running from there with another dude, and when we got picked up I ended up in a residen

**Comment 2** (score: 1124): I was sent to the infamous PCS (Provo Canyon School) from 1994 - 1996, at the crescendo of the 'standing ips' era. I witnessed a lot of beatings, and rapes. But thankfully I was never party to either one of those things. I kept to myself enough and got along with everyone. 

The worst thing was during a stint in investment, I noticed a few other kids working on loosening a pipe from a drain trap on a sink. I thought that shit was funny at the time, because "hey, petty vandalism, right?".

Well, 

**Comment 3** (score: 2606): [removed]

**Comment 4** (score: 213): I wrote this in another thread a few weeks ago about 'cults', so, I'll just copy and paste. 

I've talked about this before on Reddit, and was surprised because so many people also went to these schools but had no idea.

The CEDU boarding schools were founded by a high ranking Synanon member named Mel Wasserman. If you guys don't know what Synanon is, here you go. There's about a dozen of these schools and they are STILL OPEN. Edit: Here's the school's wiki I went to Boulder Creek Academy, 2001-

**Comment 5** (score: 7506): I was definitely a troubled teen. A lot of running away, drugs, alcohol etc.

My parents sent me to Elan School, in Maine. When i arrived i was strip searched and showered by a girl, not staff. 

It was pretty hellish, abuse was the norm. It was a couple hundred kids and a very small handful of staff. Essentially if you won privileges you got to run things. Until you messed up and had to beging the status climb all over again. We weren't allowed to make friends, that was called a contract and ot

**Comment 6** (score: 9859): I did Outward Bound when I was 18. The group consisted of about 14 of us, all between the ages of 16 and 20.

One girl was "sent" by her parents, I assume to straighten her up. On the first night we camped, she fled. She took a map, a compass, and I think some matches and was gone when we woke up.

We were told later she had made it to a road and hitchhiked to somewhere. I think she eventually made it home.

If there are camps specifically for kids in trouble, her parents should have sent her to

**Comment 7** (score: 13024): [deleted]

**Comment 8** (score: 12320): [removed]

**Comment 9** (score: 4279): [removed]

**Comment 10** (score: 3586): I did the Northwest Youth Conservation Corp. It is not exactly a troubled teens program, but I was put in an interesting situation. I joined because it seemed like a fun way to spend a summer outdoors, doing some hard but worthwhile work in the wilderness, and make some money to buy a homebuilt pc gaming rig. I knew another person joining for the 6 weeks and it just seemed like a normal teenager summer thing. For the most part it was. See, usually the crews are 5 guys, and 5 girls. They did not 

---
### Post 6: App developers and programmers of Reddit, what was the dumbest app/program idea someone ever proposed to you?
- Score: 9233, Comments: 2729
- Subreddit: r/AskReddit
- URL: https://reddit.com/r/AskReddit/comments/dq3xd3/app_developers_and_programmers_of_reddit_what_was/
#### Top Comments:

**Comment 1** (score: 716): Someone tried to sell a friend a membership to the "New Internet". She asked me to sit in and listen to the sales guys pitch. At the time I was running a web hosting business along with managing a smaller dial up isp's networking infrastructure.

The new internet was going to be built new from the ground up. All new infrastructure but without all the stuff that makes the internet "bad". The sales guy couldn't explain how that was going to work.

For only $50 my friend would get a lifetime member

**Comment 2** (score: 4541): My uncle suggested I create a type of digital map that could direct you places and help you get from point A to point B.

He suggested this three weeks ago.

**Comment 3** (score: 6593): My favorite but dumbest was "Chipotledate" which would match you with people with similar or compatible Chipotle orders.

**Comment 4** (score: 15636): My family has a technology business, and when my mom started to learn to make apps to support the product she made a test app first. 

The whole app was just one search bar that you could type any word and it would do nothing, unless you searched "loser" and then it would pop up with a picture of me from middle school with a bad sunburn and braces. 

Thanks Mom.

**Comment 5** (score: 1767): A friend of mine wanted me to make an app that turned your phone screen into a mirror. Not front facing camera, not just blacking the screen, but a literal mirror. He couldn't grasp why this wasn't possible. 

Also ANY kind of new social media app that they think can be made by one person in an hour.

**Comment 6** (score: 7237): * Any attempt to create another social media app
* Knockoffs of popular games (like the plethora of Temple Run games)
* An app for a smart watch that will run in the background and periodically meow

**Comment 7** (score: 1064): Not mine, but for our capstone project, various faculty around campus get to put in project proposals for us to choose from.

The worst fucking proposal was a magic 8 ball type of app but instead of a magic 8 ball, it was a psychic dog. It was supposed to "scan" your dog's paw and give some kind of 8ball-esque answer to your question.

The group that got stuck with that project...I felt so bad for them. Repeatedly asking for changes the night before each deadline and getting upset when it didn't

**Comment 8** (score: 4980): I have a buddy who is a programmer and a while back wanted to just get used to making an iphone app and uploading to the itunes store so that he was familiar with the process for when he wanted to do a real app. As practice he made an app that would randomly generate a name based on census data (more common names were more common). 

It made it on some websites list of top 10 lazy apps and a bunch of authors started buying it. Last I heard he had made about $20,000 on his stupid app he uploaded 

**Comment 9** (score: 1410): * An app that does your taxes for you after talking about a site that does it.
* An app to make XYZ noise
* A web site to take custom butcher orders. The reason this is dumb is that nobody in the shop would know how to run it except for me, and I was one of the butchers.

**Comment 10** (score: 2983): I had a friend who had an idea for "youtube, but better".

He didn't know *how* it would be better. Also he had no idea about domain names, hosting, VPS, maintaining a website, designing a website, or literally anything.

After he explained it, I let him down as gently as I could. "That is the stupidest fucking idea I've ever heard".

---
### Post 7: There’s a reason that programmers always want to throw away old code and start over: they think the old code is a mess. They are probably wrong. The reason that they think the old code is a mess is because of a cardinal, fundamental law of programming: It’s harder to read code than to write it.
- Score: 26933, Comments: 1073
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/8f2lzu/theres_a_reason_that_programmers_always_want_to/
#### Top Comments:

**Comment 1** (score: 2719): I think most programmers work in a similar way: imagine a problem, then decompose the problem into its constituent parts and attack those simpler, isolated problems.

The problem with a large codebase is that no one, not even the person that wrote all of it can fit the solution in their working memory. The tendency of programmers (who generally underestimate complexity) is to say: wait a minute, this problem doesn't require 10 million LOC, I could easily solve this problem in 250 lines of elegan

**Comment 2** (score: 657): I think most code, no matter how well designed before hand, is designed mostly on the fly. You always run into things you didn't think of and adapt. This leads to cludges and breaking the design. Once everything is done and it works, I love nothing better than tearing it all down and re-writing it with all lessons learned. 


**Comment 3** (score: 1670): [deleted]

**Comment 4** (score: 111): It depends.  I've been on many projects where the initial project requirements were "Oh, it's easy, you just need to do A->B->C->D".  

Then you hit testing, or worse production, and then all kinds of wackadoo requirements materialize.  "Well yeah, Most of the time you do A->B, but in these 3 situations you go to C, then back to B, then to D for 2 of them and C for the 3rd one."  "Oh yeah, this other situation requires you to go to E, then spin a D20 and decide to go to B or C or end it in F".  

**Comment 5** (score: 157): As a programmer, I have about a 0% urge to “throw away” old code. However, I have a 100% urge to rewrite old code one function at a time.

**Comment 6** (score: 533): While he makes some valid points, sometimes the codebase is just bad.  
A tangled mess of rushed spaghetti code full of "TODO" and "FIXME",
and lots of temporary hacks.  
At that point starting from scratch can be the right decision, sometimes.  

**Comment 7** (score: 143): I feel like Netscape and Borland are very different from the software most of us are working today. Netscape is a desktop application with a massive code base. I'm currently working on web services and front end apps on the order of 10k LOC. I feel like rewriting Netscape is a much bigger effort (and more likely to go wrong) than rewriting these front end apps and web services.

Also, FYI this article is almost 20 years old

**Comment 8** (score: 32): Any mature codebase will be full of non\-obvious code that is there to support what I like to refer to as *invisible requirements*. 

Invisible requirements are requirements that do not appear in any design doc or user documentation, but the existing codebase has been written to support them. They are often the result of architectural or design decisions made during the original development; modifications made to workaround bugs or performance issues; well\-known application features being used 

**Comment 9** (score: 53): As Perlis put it all the way back [in 1982](https://www.gwern.net/docs/cs/1982-perlis.pdf "Epigrams on Programming"):

> 7\. It is easier to write an incorrect program than understand a correct one.

**Comment 10** (score: 80): While he may have a point, he picked the absolute **worst possible example in history** to illustrate it. Netscape 4 was garbage. You couldn't even resize the window without a complete reload. Hundreds of glitches in rendering. Getting absolutely destroyed by IE in every way. They made the best decision of their lives ditching that buggy codebase and beginning what would become Firefox, a revolutionary browser at the time. I'm almost certain trying to build Firefox off Navigator 4 would've been 

---
### Post 8: I scraped 7M programming job offers for 8 months and here are the most demanded programming languages
- Score: 4095, Comments: 888
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/vnfl62/i_scraped_7m_programming_job_offers_for_8_months/
#### Top Comments:

**Comment 1** (score: 5915): 1. JavaScript/TypeScript
2. Python
3. Java
4. C#
5. PHP
6. C/C++
7. Ruby
8. Go

Saved you a click.

**Comment 2** (score: 400): This seems a little unbalanced. Are those Javascript jobs strictly Javascript or are they from adverts that require language X + some Javascript on the side?

**Comment 3** (score: 70): Now if someone can calculate supply as well.

**Comment 4** (score: 115): Love the entry for Fortran.

**Comment 5** (score: 51): [deleted]

**Comment 6** (score: 435): >C# is a general purpose, multi-paradigm programming language, based mainly on its predecessor C++

Who wrote this? With that logic the predecessor of Python is C

**Comment 7** (score: 102): Good God, Perl. What happened to you?

**Comment 8** (score: 237): Spend free time scraping useful data

Summarize data in helpful article with graphics

Post to Reddit

Receive 200 critiques on how you should’ve done better

**Comment 9** (score: 48): It's not easy finding good developers, but must be a special kind of hell to look for anyone with COBOL skills.

**Comment 10** (score: 64): TIL *irruption* is a word.

---
### Post 9: Linus Torvalds rails against 80-character-lines as a de facto programming standard
- Score: 5841, Comments: 1143
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/kpq460/linus_torvalds_rails_against_80characterlines_as/
#### Top Comments:

**Comment 1** (score: 1716): I like 100 or 120, as long as it's consistent. I did 80 for a while but it really is excessively short. At the same time, you do need some hard limit to avoid hiding code off to the right.

**Comment 2** (score: 193): [deleted]

**Comment 3** (score: 858): [deleted]

**Comment 4** (score: 79): The correct length is whatever fits *my* monitor.  The rest of you be damned.

**Comment 5** (score: 134): Can we also agree that 72 characters for git commit headers is also masochistic?

**Comment 6** (score: 141): This isn't the first time Linus rants about line length limits - see [this email](https://lkml.org/lkml/2012/2/3/394).

I haven't seen 80-character limits in a long time, except in some default linter configurations. 120 characters seem to be popular now, but there are still some cases where line breaking does not make the code any better. You have the occasional long formula or hard-coded string or (n+3)-character line.

It's okay if the character limit encourages writing simpler code, but most

**Comment 7** (score: 225): Yeah well the kernel uses a 8 character long tabstop, which feels to me as a brief trip to the Moon and back. Given that limitation it's no wonder 80 is too short.

For 2-space indentation, 80 works very well.

4-spaces, I'd be down with 88 (after seeing the arguments and results from Black, the Python formatter) with an absolute maximum of 100 before I can't compromise in good conscience.

8-space is right out, at that point if you can't easily see the indentation you should adjust your font si

**Comment 8** (score: 124): ironically send in a <80 character wide formatted mailing list.

**Comment 9** (score: 107): As someone that uses a tiling window manager, I kinda like this relic.

**Comment 10** (score: 9): Nowadays it’s not about people on vt100s, it’s more about side-by-side views, e.g. when using a diff/merge tool.

---
### Post 10: Google engineer breaks down the problems he uses when doing technical interviews. Lots of advice on algorithms and programming.
- Score: 6411, Comments: 1086
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/ixo3px/google_engineer_breaks_down_the_problems_he_uses/
#### Top Comments:

**Comment 1** (score: 2505): Doing all that so you can get hired and implement REST APIs

**Comment 2** (score: 514): When I was in undergrad there was a presentation by some Google engineers (setup by an alum I think) and they fielded questions from the group.

When asked about interviews all 5 of them gave often conflicting and contradictory answers to questions about how they interview people what they look for and what was important.

I am reminded of this every time I see one of these Blog posts.

**Comment 3** (score: 248): I can't wait to see this question get asked by a mom and pop shop running visual basic

**Comment 4** (score: 749): What a load of non-predictive crap.  But at least it makes the interviewer feel smart, which must be the point.

**Comment 5** (score: 285): I firmly believe algorithmic programming interviews are being used as a proxy for an IQ test. Bottom line is companies dont care about getting the best candidate, they just want to make sure the candidate they do hire is good enough. By giving them questions that have to be studied on leetcode for a few months, you are essentially locking in a certain baseline intelligence and logical ability. For companies like Google this approach may be practical, but when a whole industry does this it just e

**Comment 6** (score: 21): For anyone interested, this site lists companies that whiteboard, and companies that don't, along with their city location (worldwide)

http://they.whiteboarded.me/companies-that-dont-whiteboard.html

**Comment 7** (score: 22): Seems like a long way to say "naive recursive solution << memoized recursive solution << dynamic programming solution".

I've run into a real-world instance of a problem worthy of dynamic programming all of one time in my five years of full time experience. Interestingly, using a poor algorithm was half of the problem, but the other half of the problem was the fact that we had a web UI waiting behind a spinner for the algo solution, recomputing on every page load with no caching or precalculatin

**Comment 8** (score: 33): well, you know it's fucked up, when there are tons of companies specialized in algorithm puzzle training. A ten billion dollar market exists just to make you suffer.

**Comment 9** (score: 231): "Here are some behind-the-scenes look at our process that hasn't worked for at least a decade, possibly never. Now startups can copy our deeply flawed system! Enjoy cramming for months next time you interview." -Google

**Comment 10** (score: 13): A few months ago I was asked to be part of the interview process for new programmers at my company. I noticed after the first few interviews that we ask them questions which aren't representative of their day-to-day job if we employ them, so I...... refactored those questions and testsamples.

Now we actually test for the things we actually hire for, which is a much better experience for everyone involved. I don't give a damn if someone can write complex algorithms by hand on a whiteboard. We're

---
### Post 11: I scraped 12M programming job offers for 21 months and here are the most demanded programming languages!
- Score: 1487, Comments: 471
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/1gac15b/i_scraped_12m_programming_job_offers_for_21/
#### Top Comments:

**Comment 1** (score: 1392): Please be aware that C and C++, while related, are not one language. C/C++ does not exist. A job writing C will be very different from a job writing C++.

**Comment 2** (score: 556): Hey, 8000 rust jobs. That's double last year, and double the year before that. 
We're getting there lads

**Comment 3** (score: 123): Surprised by comparatively low numbers for Kotlin and Swift especially. I thought native mobile development was bigger than that?

**Comment 4** (score: 204): Interesting and not really unexpected. What would also be interesting to see is the average pay offer for those different positions (I know they don't post those). Some languages might have smaller number of openings, but higher demand in highly skilled developers.

It also confirms that some language proponents are way louder than the actual demand for that language. I won't mention any names :P

**Comment 5** (score: 102): I plan on retiring when Java is the new COBOL so I can take a contracting gig once a month to fix some random disaster created 40 years ago.

**Comment 6** (score: 51): Ace use of scraping, data, analysis and visualisation! 

Interested to know what causes the blips in Aug24 - perhaps a real world explanation, or perhaps a data issue such as problems scraping from a specific site? The combo of some staying at their typical percentages, three spiking up and one spiking down seems like the latter could be the case.

Great work and super useful, thanks for sharing!

**Comment 7** (score: 22): Just FYI every graph on the page is titled as JavaScript / Typescript jobs instead of the relevant language

**Comment 8** (score: 16): Isn't JS just added to every listing that has anything to do with the web?  I'd be more interested in JS as the job itself.

**Comment 9** (score: 50): Now weight it by salary

**Comment 10** (score: 24): Pretty much stays the same over the years

---
### Post 12: Spacetraders is an online multiplayer game based entirely on APIs. You have to build your own management and UI on your own with any programming language.
- Score: 4943, Comments: 307
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/13bg9zi/spacetraders_is_an_online_multiplayer_game_based/
#### Top Comments:

**Comment 1** (score: 934): This is an awesome idea, for experienced programmers can be a good way to learn a new language or stretch muscles, for beginners could be what gets them into coding for the first time properly. Wish this had existed when I was learning, will give it a look

**Comment 2** (score: 313): [deleted]

**Comment 3** (score: 1815): this just sounds like work with extra steps

**Comment 4** (score: 153): Reminds me of [Screeps](https://screeps.com/). Does anyone know of other games in this genre?

**Comment 5** (score: 203): The problem with these programming games is always that there will be a few highly optimized libraries that play for you and most people use those. Clone a repo and you're "playing"... kind of takes the fun out of it when you're up against that kind of players.

The clients that people made seem neat at least. That's unique compared to something like Screeps which already has a client.

**Comment 6** (score: 99): Brilliant idea!

Of course there's already an Emacs client 🤣

**Comment 7** (score: 23): Then there's always the pure postgres version!
https://schemaverse.com/

**Comment 8** (score: 23): > with any programming language.

In the grim darkness of the far future, there is only COBOL.

**Comment 9** (score: 54): I love the concept! My only concern jumping in is the game could be ‘solved.’ E.g: There’s an open source project that is superior to all other bots in every way, and it’s futile to come up with your own solution.

**Comment 10** (score: 27): I'm curious if you have any idea if and how you plan to monetize the game once you're out of alpha. I have no problem paying for a game I enjoy—I would just like to know what that will look like before I invest time in it.

E.g., monthly subscription for hosted with an option for self-hosted play? Hell yeah, I'm there. Something with crypto and/or micro-transactions for game actions? That would be a no from me, dog.

---
### Post 13: 80's kids started programming at an earlier age than today's millennials
- Score: 5282, Comments: 1336
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/7sec31/80s_kids_started_programming_at_an_earlier_age/
#### Top Comments:

**Comment 1** (score: 711): Back then if you wanted a game, you sometimes had to type in the program from a magazine. Nowadays, if you want a computer to do something, chances are someone's already written the program to do it.

**Comment 2** (score: 1271): God damn millennials, now they've gone and killed programming with their avacado toast nonsense 

**Comment 3** (score: 938): >a comparatively larger proportion started programming between the ages of five and ten. 12.2 percent of those aged between 35 and 44 started programming then.

Speaking about 18 - 24 year olds (a subset of millennials)

> 68.2 percent started coding between the ages of 16 to 20.

I'm not exactly sure how one can make that claim based on these statistics. It would be better to state how many millennials started at 5-10 instead of this shit. 

**Comment 4** (score: 51): There *are* no millenials left in school - they’re all adults now.

Also - from the POV of a software engineer who came up in the 80s/90s  - the barriers to entry are so much greater now. Although the amount of information/tutorials/languages/tools are much greater now - we’re well past the point where getting the word “poop” to scroll down a screen forever is going to capture the imagination of the average child.

We really need to work on that - we live in a digital-age rapidly evading the und

**Comment 5** (score: 49): I so remember studiously copying code from magazines into my commodore. That was the beginning of the end of my sanity.

edit: over 50 here, Timex Sinclair 1000. Just had a flashback, I think that was my first one. It was long ago when dinosaurs still roamed the earth.

**Comment 6** (score: 211): I owe my career to the [Commodore VIC-20 Progammer's Reference Guide](http://www.classiccmp.org/cini/pdf/Commodore/VIC-20%20Programmer's%20Reference%20Guide.pdf).   This is how 11 year-olds got into 6502 machine language coding in 1985.

**Comment 7** (score: 215): This is why they invented the raspberry pi and microbit for schools.

**Comment 8** (score: 70): I owe my career to a fellow latch key kid name Joel.  He showed me how to edit the snake game on a PET computer.  Got it to put out random letters after read some of the books on basic from the library.  Finally made my dreams come true when the snakes body was the letters it had eaten and I could challenge myself to eat the lettrr in the proper order to spell out bad words.

**Comment 9** (score: 105): [deleted]

**Comment 10** (score: 314): It's all bullshit.  There were a lot fewer programmers back then.  If you look at it as a percentage of the population, there are a lot more people starting to program at age 10 now then there were in the early 80's.  

And it's a LOT easier to start now.  Python is no harder than BASIC, but more important you've got things like Roblox, Minecraft, and scripting level editors, etc.

---
### Post 14: Engineering manager breaks down problems he used to use to screen candidates. Lots of good programming tips and advice.
- Score: 3361, Comments: 789
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/p5gfl6/engineering_manager_breaks_down_problems_he_used/
#### Top Comments:

**Comment 1** (score: 1593): "Great inventive solution to this algorithm problem, you're hired! Now go fix the CSS on this page and write some simple CRUD code."

**Comment 2** (score: 175): As an Engineering Manager my opinion is this - know what you say you know and be at comfort with things you don't know that you don't know.

I have asked programming questions, behavioral questions and may be "explain how you did what you said in resume". 

You will be surprised to know that most people cannot explain what they claim they did on their Resume. Yeah, we all like to have shiny Resumes but sometimes it not the quantity that matters but quality.

Mugging leetcode problems but failing

**Comment 3** (score: 327): [deleted]

**Comment 4** (score: 81): My group recently started doing code reviews as our technical skill challenge. We wrote a small application (two classes, some model classes and an API definition) and ask the candidate to review and provide feedback and point out problems. It's a real world task that we expect engineers to do and it helps give us insight into how they think and prioritize when it comes to coding. It's also a free form.rxcercise so we don't have a set of expected problems for them to find (though, I get disappoi

**Comment 5** (score: 223): Engineering manager here checking in to say I’d probably get to step two and just say fuck it. I could talk you through how to optimise it but I ain’t got time to write that. What, will we sit around writing fast puzzles all day at Reddit? Or are we gonna be figuring out how to cache a homepage that is different for literally every fucking user and is constantly in a state of flux?

There’s load of interesting problems Reddit has that you could ask about. For example:

-	here we have a mobile br

**Comment 6** (score: 19): I interviewed at Reddit earlier this year and received an offer for a front-end role although I ended up going with a different offer. Without getting too specific, my interview looked like this:

* Generic leetcode style screening question
* Really basic UI question that involved a ton of boilerplate code
* A couple of behavioral interviews
* Another basic UI question that built off my previous UI interview, again with tons of boilerplate code
* A system design session (my favorite one)

Pretty

**Comment 7** (score: 328): [deleted]

**Comment 8** (score: 55): There are a lot of really bad takes on this.  I was reading through some of them before I went and read the article, and so I figured it would be talking about graph traversal and Big-O notation or some esoteric shit.

Everyone out there that thinks this is a bad coding problem is dead wrong.  

* The algorithm for determining the next state of each cell is clearly laid out in the question.  There's no searching, sorting or graph traversal at all here.  Just simple for loops and counting.  
* It

**Comment 9** (score: 132): My first go-to programming interview question is a lot easier and it goes like this:

Given a long list of lower-case letters, write a function that return a list of unique letters in the original list.

Surprisingly lots of "programmers" couldn't get it right.  For those who could, you can really see the different ways of thinking.  Some simply use a hash-table/dictionary (ok, this guy knows at least a bit of data structure), some use list and do a lot of looping (a warning flag right here). So

**Comment 10** (score: 38): Accessibility tip: [never put a link where the only display text says "here"](https://usability.yale.edu/web-accessibility/articles/links#link-text) (relevant because the first paragraph of that post does this)

---
### Post 15: This video shows the most popular programming languages on Stack Overflow since September 2008
- Score: 6047, Comments: 554
- Subreddit: r/programming
- URL: https://reddit.com/r/programming/comments/d2qrx6/this_video_shows_the_most_popular_programming/
#### Top Comments:

**Comment 1** (score: 1591): I like how Java questions go up towards the middle and ends of semesters and then drastically drop at the ends of them.

**Comment 2** (score: 140): Obviously VB programmers are the best - they don't need to ask questions on Stack Overflow.

**Comment 3** (score: 828): Most popular, or the languages people need the most help with?

**Comment 4** (score: 108): I think a far better metric would be for stack overflow to publish how many *page views* questions for each language receive.

**Comment 5** (score: 108): Well of course C# is a lot lower now, Jon Skeet has already answered literally every question about C# that could be thought of.

**Comment 6** (score: 81): Python slithering it’s way to the top

**Comment 7** (score: 502): Animated bar charts are an anti-pattern. Use a line chart!!

**Comment 8** (score: 30): someone should do this for Github

**Comment 9** (score: 40): If anything this chart demonstrates the truth of Atwood's Law (Jeff Atwood co-founded Stack Overflow).

″Any application that can be written in JavaScript will eventually be written in JavaScript″

**Comment 10** (score: 191): Posts like this are rough.  I always feel like this ignores frameworks, like jquery, rails django.  Lots of searches / posts just use those framework names without referring to python, ruby, etc.

Id  like to know if this data is taking in account those framework names or not.

---
