# Reddit Data - GDPR data export

## Collected Posts and Comments

### Post 1: Client-side passport photo maker - ONNX/WASM background removal, WebGPU, and zero server processing
- Score: 1284, Comments: 74
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1rh5qfm/clientside_passport_photo_maker_onnxwasm/
- Body: Hi!

I built [www.passportphotosnap.com](https://www.passportphotosnap.com), a purely client-side utility for generating passport and visa photos for 140+ countries.

The goal was to handle the entire pipeline - from face detection to background removal - without a single image ever leaving the user's browser.

# The Technical Implementation

* **Background Removal:** I'm using `@imgly/background-removal`. It leverages WASM and WebGPU (with CPU fallback). The models are \~84MB and are lazy-loaded only when the user starts the removal process.
* **Face Detection:** I used `@vladmandic/face-api` (TinyFaceDetector) to handle the auto-centering and alignment based on specific country requirements (head size %, eye position, etc.).
* **Architecture:** The site is a static Next.js 15 export. There is no backend, no temporary storage, and no database. Privacy is enforced by the architecture itself.
* **300 DPI Rendering:** I'm using the Canvas API + Jimp to generate the final high-res crops and the multi-photo print layouts (4x6, 5x7, A4).

# Key Challenges

* **COOP/COEP Headers:** Getting the `SharedArrayBuffer` to work for the background removal WASM on a static Vercel export required some strict header configuration (`Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Embedder-Policy: require-corp`).
* **Self-Hosted Models:** I wrote a custom postinstall script to copy the ONNX/WASM models from `node_modules` into the `public/` directory so they are served from my own do

#### Top Comments:

**Comment 1** (score: 49): Background removable may invalidate your application in a lot of territories

**Comment 2** (score: 16): Oooo I kinda love it! Does it work for UK and EU formats? … asking for a friend of course

**Comment 3** (score: 7): I work on a project that uses  u/imglybackground-removal too. Heads up - their v2 update changed how the WASM workers initialize. Broke our build for a day. Might want to pin your version

**Comment 4** (score: 7): 1. Background application might make it invalid
2. Photos need to be signed/witnessed

**Comment 5** (score: 4): GitHub?

---
### Post 2: RIP Postman free tier. Here's an open-source local-first alternative we've been building for over a year
- Score: 1138, Comments: 198
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1qyi3wz/rip_postman_free_tier_heres_an_opensource/
- Body: Hello r/rwebdev,

A bit over a year ago, u/moosebay1, u/electwix, and me set out to build DevTools Studio - an open-source local-first alternative to Postman, and with them announcing pricing changes on March 1st, we figured this is a good time to share our progress so far.

If you know Postman, you'll feel at home. The UI is familiar with request builder, collections, environments. But instead of just running requests, you can connect them into visual flows like n8n.

## Here is how our app stands out

In addition to Postman and n8n, the UX is also inspired by common IDEs, with filesystem hierarchy and tabs. You can think of in-app resources as files, and use any preferred strategy for organizing and working with them.

It's an Electron app, but powered by Go on the backend for uncompromising performance. Using TanStack DB for sync, all resources are updated in real-time despite the separated architecture.

We provide a smart HAR import mechanism, which lets you record real API traffic from a browser and generate requests and flows automatically within seconds, without any manual setup.

Simple and user friendly n8n-like flows for automation, instead of convoluted scripts to chain requests together. With our flows, you can see and debug the running process in real time - data moving between steps, sequence of calls, dependencies, etc. It is easier to understand than scrolling through test files, and better to maintain over time.

All resources can be exported to clean, human

#### Top Comments:

**Comment 1** (score: 494): We switched to Bruno a while ago. Postman is no bueno anymore. Will have a look at yours next week!

**Comment 2** (score: 75): Switched to Apidog recently after the Postman shift. Covers what we need without the enterprise push.

**Comment 3** (score: 52): What’s happening to postman free tier ?

**Comment 4** (score: 101): Competition is always good! If Postman charges for what I use it for, I'll use your product.

**Comment 5** (score: 61): Pretty sure there's nothing better than Yaak.

---
### Post 3: An ode to GDPR
- Score: 673, Comments: 305
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/8li2ot/an_ode_to_gdpr/
- Body: Twas the night before GDPR, and throughout the UK

Employers were panicked, hoping their compliance was OK.

Security and Procedures have been checked with care

But it was still pretty daunting knowing by morning the law would be there!

Directors were restless, tossing and turning in their beds,

whilst visions of million pound fines danced in their heads.

The DPO’s are ready to embrace their new role

whilst marketing teams look aged as the stress takes its toll.

No one denies that the change in legislation is better \- for sure,

but let’s admit now that the process has been a chore.

Updating policy documents is not our idea of fun

But the ICO has told us that it needs to be done.

So alas, we are here, the night before D\-Day.

Gone are the days where personal data goes astray.

Hopefully your efforts will not have been in vain...

Because GDPR has been a right f\*\*\*king pain!

#### Top Comments:

**Comment 1** (score: 164): Saw a good tweet similar to this doing the rounds today:

He's making a list

He's checking it twice

He's gonna find out who's naughty or nice 

Santa Claus is in contravention of article 4 of the General Data Protection Regulation (EU) 2016/679

(Credit @mutablejoe)

**Comment 2** (score: 1): # Just in case you are trying to make sense of GDPR, here are some great resources to help you out:

### Good Guide
https://techblog.bozho.net/gdpr-practical-guide-developers/

### Checklist
https://gdprchecklist.io/ 

### For developers
https://www.smashingmagazine.com/2018/02/gdpr-for-web-developers/

### For designers
https://www.smashingmagazine.com/2017/07/privacy-by-design-framework/

-- 
^(stolen from : Smashing Magazine's twitter https://twitter.com/smashingmag/status/999189181162250241)

**Comment 3** (score: 23): I’ve been wondering. How does the law affect people building hobby websites or learning by building? Does the law only affect corporations. If not, is there any income or profit cutoffs in place to keep it easy to make a hobby website without having a lawyer? I assume in practice they’d enforce it sensibly, but as the law is written is there legal liability?

**Comment 4** (score: 158): Best legislation ever. 

__**EDIT**__ __**1**__: I work for a company  that deals with data and I stand by what I said.

**Comment 5** (score: 20): I've been getting a lot of emails from companies about this. It sure is a getting a bit spammy 

---
### Post 4: We spent 33 months building a data grid, here's how we solved slow UIs.
- Score: 635, Comments: 67
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1ng8rb9/we_spent_33_months_building_a_data_grid_heres_how/
- Body: A few months ago, we launched the beta of [LyteNyte Grid](https://www.1771technologies.com/), our high-performance React data grid. Today, we're taking the next leap forward with LyteNyte Grid v1, a major release that reflects months of feedback, iteration, and performance tuning.

# Headless By Design

LyteNyte Grid is now fully headless. We’ve broken the grid down into composable React components, giving you total control over structure, behavior, and styling. There’s no black-box component logic. You decide what the grid looks like, how it behaves, and how it integrates with your stack.

* Works with any styling system. Tailwind, CSS Modules, Emotion, you name it.
* Attach event listeners and refs without the gymnastics.
* Fully declarative views and state. No magic, just React.

If you don’t feel like going through all the styling work, we also have pre-made themes that are a single class name to apply.

# Halved the Bundle Size

We’ve slashed our bundle size by about 50% across both Core and PRO editions.

* **Core** can be as small as 36kb (including sorting, filtering, virtualization, column/row actions, and much more).
* **PRO** can be as small as 49kb and adds advanced features like column pivoting, tree data, and server-side data.

# Even Faster Performance

LyteNyte Grid has always been fast. It’s now faster. We’ve optimized core rendering, refined internal caching, and improved interaction latency even under load. LyteNyte can handle 10,000 updates a second even f

#### Top Comments:

**Comment 1** (score: 66): Looks like AG Grid? How does it compare?

**Comment 2** (score: 16): I love virtualization for performance reasons, but we've had problems with it in unit tests (Jest) when using Ag Grid. How does this data grid work in a JSDom environment like Jest uses for their rendering tests?

**Comment 3** (score: 53): Wish it was framework agnostic

**Comment 4** (score: 18): "Here's how we solved slow UIs"

"It's now faster"

:(  As someone else who's built a lot of these sorts of components, I was hoping for a bit more detail here.  Could you expand on what sort of optimisations you've done here?  That would be really interesting, and, for me at least, would inspire a lot more confidence in the product than just hearing that it's fast.

**Comment 5** (score: 31): Very pretty.  
Vanilla Javascript version ?

---
### Post 5: I'm a front-end engineer who loves building side-projects. My latest is an AI Art Generator app. Here's how I built and launched a fairly complex app in under a month thanks to some good choices of technology.
- Score: 630, Comments: 54
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

**Comment 1** (score: 25): Art style looks very cool! Nice work

**Comment 2** (score: 12): Nice post, but you're not talking about the AI bit at all, which in my opinion is the most interesting part... :-(  
How do you actually make those generated pictures?  
Did you make the algorithm / AI yourself?

**Comment 3** (score: 18): There's show off Saturday in this subreddit, and as far as I'm aware, it's still Saturday here. So technically you could put your app name? I'm no mod though.  


Anyway, nice work and nice post!

**Comment 4** (score: 17): I'm a front end dev who never builds side projects. You guys play your cards right and maybe I'll show off that button I made that launches a modal but never did anything else with.

**Comment 5** (score: 7): What kinda costs are you looking at for Firebase and Algorithmia?  They sound like nice products... almost too nice?

---
### Post 6: HTML to PDF is such a pain in the ass
- Score: 425, Comments: 208
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1m67e80/html_to_pdf_is_such_a_pain_in_the_ass/
- Body: Admin dashboard needs a “export as PDF” button.

Been hacking html2pdf lib to get proper results but it’s all so hacky.

Something that a browser extension like GoFullPage can do so easily, and to do it with JS is practically impossible.

Headless is the only way to do it properly — but you have to pay an API for that, and expose sensitive data to third parties.

Rant over.

#### Top Comments:

**Comment 1** (score: 422): If I were in your shoes, I'd push back and offer an alternative. I'd suggest using CSS media queries for print like so

```
@media print {
  body {
    background: white;
    color: black;
  }
  .no-print {
    display: none;
  }
}
```

Put `.no-print` on things you don't want to print, and otherwise specify CSS to make the dashboard styled appropriately for a printed page. Anything inside of the `@media print` section will only be applied when printing via the browser.

Then ask your customer t

**Comment 2** (score: 100): Just use puppeteer or gotenberg, no need to pay for it.

**Comment 3** (score: 98): > Headless is the only way to do it properly — but you have to pay an API for that, and expose sensitive data to third parties. 

Just install a chromium based browser like Google Chrome

    chromium --headless --print-to-pdf=file1.pdf --no-pdf-header-footer https://example.com/internal-page

**Comment 4** (score: 60): There is also Gotenberg which is easy to self host in a Docker container.

**Comment 5** (score: 12): It is not javascript, but have a look at [WeasyPrint](https://weasyprint.org/) or [PrinceXML](https://www.princexml.com/). Both headless.

---
### Post 7: Safari silently deleted our users' saved data after 7 days.
- Score: 405, Comments: 201
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1rpp4oh/safari_silently_deleted_our_users_saved_data/
- Body: We built a web based project management tool, not a full SaaS with accounts at first, just a local first tool where everything saves to browser via IndexedDB. Think of it like Notion but everything stays in your browser, no server, no account needed. We marketed it as "your data never leaves your device" and people loved it, about 25K weekly active users mostly on desktop Chrome and Firefox where everything worked perfectly.

Then we started getting emails from users saying their entire project boards were gone. Not corrupted, not partially missing, completely wiped like they'd never existed. The weird thing was it was only iPhone and iPad users and pattern was always same, they'd use app heavily for a few days, then not open it for about a week, and when they came back everything was gone.

It took us way too long to figure this out because we kept looking for bugs in our code. We audited our IndexedDB write logic, checked for storage quota issues, added error boundaries around every database operation, added telemetry to track when data was being written and read. Our code was fine. The data was being saved correctly every single time. It was just disappearing on its own a week later.

Turns out Safari on iOS has a 7 day cap on "script writable storage" for websites that aren't added to home screen as a PWA. If user doesn't visit your site for 7 consecutive days, Safari automatically purges all their IndexedDB, localStorage, Cache API data, everything. This isn't a bug, it'

#### Top Comments:

**Comment 1** (score: 326): That's the fun part of web development! So many new things and different standards to discover!

**Comment 2** (score: 390): You can never backup data if it's only stored on the clients, it is inherently unreliable from the start.

**Comment 3** (score: 235): A browser-only app without any other support in server or client seems architecturally very fragile to me. You just illustrated an example why. Browsers are meant for transient computing.

**Comment 4** (score: 49): Are you also requesting *persistent storage* permission? If not any browser can yeet it if it wants. 

https://web.dev/articles/persistent-storage

**Comment 5** (score: 84): > not a full SaaS with accounts at first, just a local first tool where everything saves to browser via IndexedDB. Think of it like Notion but everything stays in your browser, no server, no account needed. We marketed it as "your data never leaves your device"

So, your users loose all data when they …

* clear local data
* switch browser
* buy a new computer 
* …

This wasn’t exactly a smart design choice. All bowser storage is temporary.


---
### Post 8: Made a neural net from scratch using JS & WebGL. Source code in comments.
- Score: 330, Comments: 23
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1pfe3fr/made_a_neural_net_from_scratch_using_js_webgl/
#### Top Comments:

**Comment 1** (score: 119): Sometimes I'm shocked I get paid to make dumb crud apps when people can build stuff like this.

Insane

**Comment 2** (score: 19): This kind of thing runs smoothly in a web environment. It's like I'm looking into another world.

**Comment 3** (score: 28): Github: [https://github.com/ChuWon/nn](https://github.com/ChuWon/nn)  
Demo: [https://chuwon.github.io/nn/](https://chuwon.github.io/nn/)

**Comment 4** (score: 14): I do know some web development. But, dude this is insanely nuts site. Best visualization I have seen Ofcourse, Beside 3Blue 1Brown.

**Comment 5** (score: 8): I have no idea what it does but it looks amazing

---
### Post 9: I built a free tool to create custom map posters of anywhere on Earth and would love some feedback!
- Score: 323, Comments: 107
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1q31bio/i_built_a_free_tool_to_create_custom_map_posters/
- Body: I've been working on a side project called [Carto-Art](https://cartoart.net) \- a web app that turns real map data into print-ready poster art.

The idea came from seeing vendors selling simple city map prints and thinking "I could make something way more customizable." So I built it.

**What it does:**

* Search any location or pan/zoom/tilt the camera to frame your composition
* Toggle layers individually (streets, buildings, water, parks, terrain, labels)
* Choose from styles like minimal line art, dark/noir, blueprint, vintage, etc.
* Full color customization - swap background, water, roads, green space colors in real-time
* Export at true print resolution up to 24×36" at 300 DPI

**The terrain feature is my favorite part.** It uses GPU-accelerated hillshading with Terrain-RGB tiles that encode elevation at 0.1m precision. The shading automatically adapts to whatever color palette you've selected - navy shadows for dark themes, warm browns for vintage, etc.

Everything runs client-side with OpenStreetMap data, so there's no account needed and it's free to use.

Would love feedback from this community on what features would make this more useful. 

[Link: cartoart.net](https://cartoart.net)

#### Top Comments:

**Comment 1** (score: 38): It is awesome! However: if I choose a higher export level, the map in the resulting image is very zoomed out. In the preview I only see my city and in print-ready download I see the whole country.  

It seems like the revolution correlates with the zoom level 

**Comment 2** (score: 23): Nobody calling out Caracas 💀

**Comment 3** (score: 14): This deployment is temporarily paused

**Comment 4** (score: 10): Nice project... It doesn't seem to know where New Zealand is.. .this is not uncommon with map tools.

See:  
[https://www.reddit.com/r/mapswithoutnewzealand/](https://www.reddit.com/r/mapswithoutnewzealand/)

**Comment 5** (score: 14): 10/10 no notes. That is really cool

---
### Post 10: A reminder that there are more react hooks than useState and useEffect!
- Score: 278, Comments: 57
- Subreddit: r/webdev
- URL: https://reddit.com/r/webdev/comments/1ojni2o/a_reminder_that_there_are_more_react_hooks_than/
- Body: Please don't roast me for wanting to share this, but I've been learning more about newer react hooks and remembered when I knew no other hooks than `useState` and `useEffect` lol. I am not here to judge, I am here to help spread the knowledge with a few hooks I have became way more familiar and comfortable with! Here is a reminder for all the hooks you don't use but probably should!

# useMemo: The "I already did it" hook

`useMemo` helps prevent unnecessary re-computation of values between renders.  
It’s perfect for expensive functions or large array operations that depend on stable inputs.

```
const filteredData = useMemo(() => {
      return thousandsOfDataPoints.filter((item) => item.isImportant && item.isMassive);
}, [thousandsOfDataPoints]);
```

Without `useMemo`, React would re-run this filtering logic **every render**, even when `thousandsOfDataPoints` hasn’t changed.  
With it, React only recalculates when `thousandsOfDataPoints` changes — saving you cycles and keeping components snappy. The takes away, use useMemo for large datasets that don't really change often. Think retrieving a list of data for processing.

# useCallback: The "Don't do it unless I tell you" to hook

`useCallback` prevents unnecessary re-renders caused by unstable function references.  
This becomes essential when passing callbacks down to memorized child components.

```
    import React, { useState, useCallback, memo } from "react";
    
    const TodoItem = memo(({ todo, onToggle }) => {
 

#### Top Comments:

**Comment 1** (score: 51): As far as `useMemo` and `useCallback`, those hooks aren't needed as much anymore with the introduction of React Compiler.

**Comment 2** (score: 35): You can also do some fancy stuff with `useReducer()` and `useContext()`.

**Comment 3** (score: 58): Just one more hook bro. Don't worry bro, the next hook will fix everything.

**Comment 4** (score: 38): as a react beginner, this is a game changer! thank you so much for taking the time out of your day to write this up :))

**Comment 5** (score: 11): Ai

---
