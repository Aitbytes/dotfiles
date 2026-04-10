# Reddit Data - SoftwareEngineering

## Collected Posts and Comments

### Post 1: How do software engineers with years in the industry do comments?
- Score: 190, Comments: 289
- Subreddit: r/SoftwareEngineering
- URL: https://reddit.com/r/SoftwareEngineering/comments/18bfca1/how_do_software_engineers_with_years_in_the/
- Body: Hello, I'm currently working on a project as part of my computer science  program's capstone or project. I'm interested in understanding how experienced  engineers typically use comments within their code. That would be helpful for senior developers or project managers when  reviewing, critiquing, or understanding the code.

I know my code is terrible would like to know some tips for improvements

https://preview.redd.it/jpbrxlk62i4c1.png?width=864&format=png&auto=webp&s=8ecc19af99fc74eb4a6e0d1ddeab51ccb7bb77c8

#### Top Comments:

**Comment 1** (score: 209): Avoid comments that explain *what* the code is doing. The only people reading those comments will also be able to read the code, so all you're doing is adding noise.

Like, what's the point of comments like "first increment", "second increment", "combine two things into one string" in your code? You're just using more words to say the same thing the code is already saying.

Comments to explain *why* the code is doing something can be useful, but they should be rare and preferably done at the met

**Comment 2** (score: 16): Doc block comments to auto generate documentation is typically all I add these days. Sometimes I use comments to pseudo code functions before I write the actual code, but then its replaced by the code.

**Comment 3** (score: 24): I only comment if I am ashamed of a particular piece. 

“Yeah I know it’s not optimal but I had to because…”

**Comment 4** (score: 10): If you have to leave a comment on some code, try to find a way to make your code more readable, once you’ve exhausted all possible options is it appropriate to leave a comment.

Don’t worry though, you’ll figure it out after your first few code reviews, or in my case your first few hundred code reviews.

**Comment 5** (score: 4):     list.append(thing)  # append the thing to the list

This is totally unhelpful, we know it is appending a thing to a list, there is no benefit in explaining this further as it just makes your code harder to read.

Comment things that need explaining, and make sure you avoid writing code that needs explaining explicitly unless you have exhausted all other options.

Comments should say why or how, not what. If you need to explain what, then you have a problem.

Some of your comments could be re

**Comment 6** (score: 3): I would say like docstrings that explain the why are helpful, and also comments about something that might have been a bit of a headache to figure out and you don’t want to have to figure it out again later when you forget why it’s like this and you don’t want others to have to figure it out too.  Or also a link to the docs or some resource can also be helpful if it’s like some concept or code that’s new to the codebase.

**Comment 7** (score: 3): We log into reddit and shitpost like everyone else.

**Comment 8** (score: 8): [deleted]

**Comment 9** (score: 2): Try to avoid comments in favor of code that is obvious. The only comments I'll write will be on lines that look sttange and would make someone go, "Why is this this way?", or for larger blocks trying to accomplish something, but that is what is trying to be achieved vs what is being done.

**Comment 10** (score: 2): this is a bad comment:

\#get the current time and date

 the comment is a distraction. it's pretty obvious from the code that you're getting the date/time.  i'd prefer to see a comment saying why you need the date and time instead.

it looks like you redeclare that same variable a few lines lower without having used it in the first place.

---
### Post 2: Has anybody had a job they actually liked? If so, what was it?
- Score: 3896, Comments: 6798
- Subreddit: r/AskReddit
- URL: https://reddit.com/r/AskReddit/comments/1afldvi/has_anybody_had_a_job_they_actually_liked_if_so/
#### Top Comments:

**Comment 1** (score: 13637): I was a toy designer for about 45 years and loved it. I designed the first twelve Star Wars figures and a bunch of Hot Wheels.  I’m retired now and painting.

**Comment 2** (score: 4220): When I was in high school I worked at an amusement park called Kings Island. There was a ride called White Water Canyon. They had me sit in this shed back in the woods and I’d get to launch water cannons at people as they floated by on their boats. It was the best job ever! I would sit back there eating snacks and drenching people.

I’m an electrician now, I like it just fine but nothing compares to the water cannon job

**Comment 3** (score: 1436): I once had a job as a freelance proofreader for a publishing company.  I loved every minute of my job.  I love it so much, I probably should have paid them for letting me do the job.  Anyway, I eventually had to quit because I decided I needed a more lucrative job.  So I went to law school, became a lawyer ... made the money, and eventually retired.  Now I proofread for free at a site called Distributed Proofreaders ([https://www.pgdp.net/c/default.php](https://www.pgdp.net/c/default.php)) that 

**Comment 4** (score: 2989): Pizza shop when I was 17. Worked there until I was 22. Met my husband there, my first baby got to run around the place, met some of the friends I still have to this day. The bond we made over that place is incredible. It closed down years ago but every few years we all still get together and hang out. The pizza shop turned into a bar, so we meet there. That place will forever be special to me

**Comment 5** (score: 1657): In high school I worked in a non-chain pizza shop. The owner was NEVER there and it was just me and my 3 best friends running a pizza shop, not sure how we didn't put it out of business. But my goodness it was so fun.

**Comment 6** (score: 4394): It's all about the people and the management. Your job could be scooping shit and digging ditches, but if the people you work with are awesome, you have a boss who supports you and wants to you do well at work and beyond, and you have good benefits; that's a great job.

**Comment 7** (score: 255): My job cleaning tables at the largest cafeteria at NDSU


It was easy, the boss treated us humanely, and got 5 free meals a week and all the drinks I wanted


Even had a performance review so good they let me be one of the caterers for a charity even held by Shaq


People sucked, plenty of people would make messes in front of us and give us crap because it was our job to clean for them


Reminder, these were adults


But the boss was good. Let us sit down during quiet times

**Comment 8** (score: 1810): Software engineer for that Danish company that make plastic bricks… I love very minute.

**Comment 9** (score: 1265): I’m a sign language interpreter, I love my work

**Comment 10** (score: 719): No necessarily the job itself, but the place I work. Smaller office where you are not expected to just grind. You can have a good time while still getting work done. You are not monitored by a clock and treated like an adult to make up time, if need be. You are given flexibility when it comes to family emergencies or child care issues, doctors appointments as well as needing to run a personal errand. There are bi monthly luncheons, random get togethers and everyone is a close group. Everyone kno

---
### Post 3: What are the best books to learn how to think like a software engineer?
- Score: 194, Comments: 67
- Subreddit: r/SoftwareEngineering
- URL: https://reddit.com/r/SoftwareEngineering/comments/1k21d3k/what_are_the_best_books_to_learn_how_to_think/
- Body: i’m trying to level up not just my coding skills, but the way i *think* about problems, like a real software engineer would. i’m looking for book recs that can help me build that mindset. stuff around problem-solving, system design, how to approach real-world challenges etc.

#### Top Comments:

**Comment 1** (score: 36): Vibe code everything, by Sam Altman et al

**Comment 2** (score: 62): Few books from experience:
- Introduction to Algorithms by Thomas H. Cormen: Teaches you the fundamentals of algorithms and data structures.
- Domain Driven Design by Eric Evans: Most of the time the most difficult thing in software engineering is not the technical implementations, but in understanding the problems you want to solve with software and designing the software architectrue to reflect the problem domain. This book helps you with that.
- The Pragmatic Programmer by David Thomas and An

**Comment 3** (score: 36): Great question — thinking like a software engineer is more than just writing code. It’s about problem decomposition, understanding trade-offs, navigating ambiguity, and thinking in systems. Here are some books that helped me (and many others) level up that mindset: 

The Pragmatic Programmer by Andrew Hunt & David Thomas

Clean Architecture by Robert C. Martin

Code Complete by Steve McConnell

Software Requirements by Karl Wiegers, Joy Beatty (The classic from the master)

The Mythical Man-Mont

**Comment 4** (score: 13): There are two pimrary ways of thinking that I think form the foundation of any good engineer.

# System Thinking: 

Everything is a system. You need to see inputs, outputs, feedback loops, dependencies, constraints, and flows—whether it’s in code, an organization, or a business model.

For example, when I look at a car, I don't see a simple thing that goes vroom.  I see a framework for an engine, drive train, torque converters, transmissions, electronic control units, and complex engineering to 

**Comment 5** (score: 7): Here are a few of my top picks, looking across the entire life cycle:

* [McConnell's Rapid Development: Taming Wild Software Schedules](https://www.microsoftpressstore.com/store/rapid-development-9781556159008)
* [Farley's Modern Software Engineering: Doing What Works to Build Better Software Faster](https://www.informit.com/store/modern-software-engineering-doing-what-works-to-build-9780137314911)
* [Shore's The Art of Agile Development](https://www.jamesshore.com/v2/books/aoad2)
* [Wieger's S

**Comment 6** (score: 5): Designing data intensive application, hands down the BEST

**Comment 7** (score: 3): i think this book is good for teaching problem solving technique. 

Think Like a Programmer: An Introduction to Creative Problem   
by V. Anton Spraul

its teach you to split problems into discrete components to make them easier to solve.

**Comment 8** (score: 3): The mythical man-month. Soul of a new machine. Read up on Unix.

**Comment 9** (score: 3): Go with ['The mythical man-month Essays on Software Engineering'](https://web.eecs.umich.edu/~weimerw/2018-481/readings/mythical-man-month.pdf), ['Mathematical Puzzles and diversions'](https://bobson.ludost.net/copycrime/mgardner/gardner02.pdf) &  ['the art of programming, 2nd edition'](https://bobson.ludost.net/copycrime/mgardner/gardner02.pdf).. Good learning…💡

**Comment 10** (score: 2): If you want a light heart approach:
[Aha!](https://www.thriftbooks.com/w/aha-insight_martin-gardner/292557/item/3854266/?utm_source=google&utm_medium=cpc&utm_campaign=high_vol_frontlist_standard_shopping_customer_acquisition_20982170636&utm_adgroup=&utm_term=&utm_content=689361939032&gad_source=1&gclid=CjwKCAjw8IfABhBXEiwAxRHlsGIjR2EJje2aj4fq4xXKluKbNtyJm1oCkmdT4LfpcAQ_cEdtrPIDAxoCjSUQAvD_BwE#idiq=3854266&edition=2416643)

And for a bit more depth - The seminal book [Godel, Escher, Bach](https:/

---
### Post 4: What are some subtle screening questions to separate serious software engineers from code monkeys?
- Score: 85, Comments: 161
- Subreddit: r/SoftwareEngineering
- URL: https://reddit.com/r/SoftwareEngineering/comments/1cxgrgd/what_are_some_subtle_screening_questions_to/
- Body: I need to hire a serious software engineer who applies clean code principles and thinks about software architecture at a high level. I've been fooled before. What are some specific non- or semi-technical screening questions I can use to quickly weed out unsuitable candidates before vetting them more thoroughly?

Here's one example: "What do you think of functional programming?" The answer isn't important per se, but if a candidate doesn't at least know what functional programming \*is\* (and many don't), he or she is too junior for this role. (I'm fine with a small risk of eliminating a good candidate who somehow hasn't heard the term.)

#### Top Comments:

**Comment 1** (score: 169): Hope this "serious software engineer" role comes with serious software engineer pay unlike a lot of these job postings.

**Comment 2** (score: 160): Would you rather enjoy this whiteboard system diagram or a nice banana?

**Comment 3** (score: 88): Can you describe a time when you had to refactor a piece of code? What was the reason for the refactoring, and how did you approach it?

When doing a code review, what kinds of issues or problems do you look for? What kind of feedback do you like to get?

What criteria do you use to determine what kinds of tests to write for a particular feature or bug fix?

**Comment 4** (score: 36): Are you yourself a 'serious' software engineer? Ive never once felt like I've not been able to tell in an interview whether someone is a code monkey or not. If you arent a software engineer and just hiring, i don't think you *can* sus one out if someone is a good interviewer. You simply won't know what answers sounds bs.

**Comment 5** (score: 49): imagine working for a guy asking these questions on reddit...

**Comment 6** (score: 18): i would think an easy one to differentiate is to describe an architectural pattern that you’ve implemented in a past project. if the candidate was involved in arch decisions, they should have no problem diagramming out a complex piece of architecture. Follow up questions would be to discuss trade offs made for certain decisions

**Comment 7** (score: 9): Describe a non trivial problem, preferably one you have experienced at work, and have context for. Ask them what their solution would be. Take stock of the line of questioning they use to flesh out details and gather requirements. That can tell you a lot. Use the discussion as a frame to jump into interesting technical questions and to probe their experience further.

**Comment 8** (score: 5): You can't find this out with "screening" questions, you have to get them talking about a problem, their process, their lessons learned, STAR pattern questions that probe for situations that match the skill set you're looking for, then probe about the tasks, actions, and results.

**Comment 9** (score: 4): "How do you ensure that your code follows best quality practices and is fit for purpose?"

"What is technical debt, how do you minimize it, and how do you manage it?"

**Comment 10** (score: 4): I should have been suspicious when these more "senior" questions did not come up. I failed my probationary period and was told I was too over qualified. They wanted a code monkey not a senior/technical architect type.

So, look for the absence of these questions as well. You live and learn ;)

---
### Post 5: r/SoftwareEngineering will be shutting down indefinitely on June 12th in protest of Reddit's API changes
- Score: 486, Comments: 61
- Subreddit: r/SoftwareEngineering
- URL: https://reddit.com/r/SoftwareEngineering/comments/143j3lv/rsoftwareengineering_will_be_shutting_down/
#### Top Comments:

**Comment 1** (score: 52): I apologize to all the users, I'm the sole moderator of this sub and I can't support the policies that Reddit is implementing, I've tried to foster a SE community, we all know it's difficult to find a place to discuss SE topics (not programming) and that's what I've been trying to do.

If Reddit changes the policy in the future, I'll make the sub public again, I'm not against monetization, but this is just greedy and abusive.

**Edit:**

I just purchased se.social, the idea is to have a Lemmy se

**Comment 2** (score: 12): Agree with your sentiment and as a user I'm pulling out of Reddit entirely.  
Good luck with future endeavours.

**Comment 3** (score: 3): Wait, wait, wait...Apollo is going away?

But the Reddit app sucks!

**Comment 4** (score: 2): Lemmy is good!

**Comment 5** (score: 3): The post makes such thought leaps i can't even take i t seriously, if there is no api, then no bots can be used for the spam, i took a large portion of 2022 r/place using bots, i wont be able to repeat that anynore, which is honestly a good thing, less moderation will be needed because of this, i will miss Boost tho, such a great app, prolly gonna have to start using old.reddit on the web again... with adblocker and all my addons, which is not that terrible
Also child abuse on the surface /dewp 

**Comment 6** (score: 2): God speed

**Comment 7** (score: 1): Glad this didn't happen

**Comment 8** (score: 1): Indefinitely? What about people who still wanna use this without having to use discord? Seems unfair that because of Reddit’s changes, we can’t access a community we love. Even though their changes are dumb

**Comment 9** (score: 1): This makes me sad. I hope with enough pressure from users they will adapt their changes...

**Comment 10** (score: 1): Is ot shut down as in deleted or as in closed for new submissions? hope existing posts can still be accessed.

---
### Post 6: What is seriously overpriced and we all still use?
- Score: 10662, Comments: 11069
- Subreddit: r/AskReddit
- URL: https://reddit.com/r/AskReddit/comments/5b3fw8/what_is_seriously_overpriced_and_we_all_still_use/
#### Top Comments:

**Comment 1** (score: 11634): Mobile data.

**Comment 2** (score: 4735): Airport food.

**Comment 3** (score: 1863): College Text Books

**Comment 4** (score: 1639): In the UK, I'd say landlines. I have to pay line rental @ £16 before I can have broadband and I never use my house phone.

**Comment 5** (score: 1556): [deleted]

**Comment 6** (score: 1202): Matresses.  
I work for a mattress company. The mark-ups are incredible.  
If you are in the market for one, wait until a sale. A customer came in Labor Day and paid $10 for a $90 box

**Comment 7** (score: 8673): Printer Ink. The stuff is like gold in value per ounce.

**Comment 8** (score: 14277): Internet that sucks ass and always gets throttled or slowed down randomly (looking at you Comcast, ATandT, TimeWarner Cable, Verizon, etc.)

**Comment 9** (score: 801): Text message fees might be the purest form of profit ever conceived.

They put effectively zero additional strain on the network, since they are sent in the extra space of data packets that have to be sent anyways during normal operation. Basically your phone needs to regularly update the towers to say 'Hey, I'm in this zone' so the network knows where to find you. But that doesn't take very much data at all, and wireless networks kinda sorta have a minimum packet size, so you can fit the 'Hey, 

**Comment 10** (score: 2149): Bras. And underwear.

---
### Post 7: What do you have a degree in, and what is your actual job?
- Score: 5865, Comments: 6613
- Subreddit: r/AskReddit
- URL: https://reddit.com/r/AskReddit/comments/7tsi3e/what_do_you_have_a_degree_in_and_what_is_your/
#### Top Comments:

**Comment 1** (score: 6322): Degree: Psychology.

Job: I work with people suffering from addictions to gambling and alcohol... as a casino dealer.

**Comment 2** (score: 1445): Degree: Middle eastern History and Arabic. Job: EMT/firefighter

EDIT: Although I didn't pursue a career in my degrees, I found my education, and my current job, to be very fulfilling. Also, everyone who is wondering why I would study what I did should really do some research on how many job opportunities there are in those fields. 

**Comment 3** (score: 1224): I have a finance degree and have been a fly-fishing guide for the past several years.

**Comment 4** (score: 2790): Biochemistry

freelance illustrator

**Comment 5** (score: 2481): I have a BS in chemistry, and I am a forensic DNA scientist.

**Comment 6** (score: 1585): Criminal justice.... fucking bank teller

**Comment 7** (score: 5976): [deleted]

**Comment 8** (score: 8528): Geology. I'm a Geologist. 

**Comment 9** (score: 376): Biological Sciences, BS, concentration in Wildlife Biology.

State biologist, coastal lands.

**Comment 10** (score: 982): Economics - Economist. 

---
