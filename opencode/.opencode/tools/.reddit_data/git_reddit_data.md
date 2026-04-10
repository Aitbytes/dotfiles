# Reddit Data - git

## Collected Posts and Comments

### Post 1: How many of you think git is a complex tool
- Score: 183, Comments: 246
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1kih9no/how_many_of_you_think_git_is_a_complex_tool/
- Body: Well, after a while I realized that many people struggle with git because it is "too complex" (under the hood yes, it is kind of complex) but if you just want to do the basis then it shouldn't be that complex. So I would like to hear what you guys think about it and if you think it is too complex or not. Thanks before hand 😄

#### Top Comments:

**Comment 1** (score: 122): The problem is 99% of the time I am pulling, checking out a branch, adding, committing, pushing. It's not that it's complicated, but when I have to do the 1% cherry pick or rebase or whatever I have to look it up and it feels confusing because I rarely do it.

**Comment 2** (score: 23): The complexity isn’t in the perfectly executed workflow, it’s in the edge cases. 

One example that comes to mind is merging a branch ‘accidentally’ , then reverting the merge commit, then when your merge is ‘ready’ and you merge to main again, “some of our stuff is missing”.


This was because the merge commit pulled in all the commits from their branch prior to the accidental merge, and reverting made the merge commit not apply in the main branch.  The later merge saw that main already had the

**Comment 3** (score: 37): I used to dismiss people who complained about git being complicated. I used to think git is powerful, learn it and you will be rewarded. There is no free lunch.

Now that I'm using jj, I've realized that a VCS can be both more powerful and simpler than git.

**Comment 4** (score: 8): I’ve used a lot of source code control systems: cvs, SourceSafe, svn, Perforce, Projector, and now git. 

I loved svn and even administered our servers. Early versions of git were ridiculously complex to use in comparison. The man page even describes it as "the stupid content tracker". A lot has been cleaned up since then, but even today if you gave an average programmer 20 tasks in git they would have to look up 15 of them because the command-line ui is neither obvious nor consistent. 

Git is,

**Comment 5** (score: 14): It's an incredibly complex tool. Day to day usage by people following good dev practices should be pretty basic/simple, though. A lot of things are like that.

Regardless, I have trouble taking someone seriously if they're a developer or developer adjacent and don't know the basics of git at this point.

**Comment 6** (score: 23): The problem of versioning source code is complex.

When people complain about the complexity of versioning tools like Git, it's often the case that it's actually the problem that is complex, and the tool is as complex as it needs to be to solve the problem.

**Comment 7** (score: 4): I've been using version control since 1996 so I've gone through LOTS of different products.  RCS, CVS, SVN, Dimensions, Synergy, BitKeeper, VSS...  I agree git is probably the most complex.  It's designed to handle extremely complex use cases, most of which I will never need.  I do wish it were more streamlined for the most common 80% of use cases, but it is what it is.  It's pretty much the industry standard, so we're stuck with it.

**Comment 8** (score: 4): The git data model is relatively straightforward once you understand it. But the UX is terrible.

The git CLI is very much what you get if you throw a jumbled mess of bash, C, and perl in a bag and shake it up. It has grown in a very ad hoc way over time and has a lot of oddities.

For example, the whole porcelain vs plumbing distinction is super unclear. It's an overwhelming list of subcommands, which leads newcomers to memorize the few things they need without really understanding much. The wo

**Comment 9** (score: 3): You can carve out a simple workflow, use it without understanding, and get on with a small team like that.


If you want to do more complicated things.. well, there's a lot of terminology to learn, and quite a lot of moving parts, and the command line options aren't all that consistent.

**Comment 10** (score: 3): It is a complex tool, the trick is to have a simple workflow where you rarely need/use all the features.

---
### Post 2: What are some lesser known features of Git that more people should know?
- Score: 203, Comments: 227
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1mi00ef/what_are_some_lesser_known_features_of_git_that/
- Body: Every once in a while when I look at Git documentation, I notice something and think "I wish I knew about this earlier.". So I'm wondering what are some relatively lesser-known features that more people should know about?

#### Top Comments:

**Comment 1** (score: 106): worktree

**Comment 2** (score: 72): `--force-with-lease` allows you to force push, but only if upstream is in state that your local git expects, i. e. it will not overwrite someone else's commit. If you have to force, force with lease

**Comment 3** (score: 56): [rerere](https://git-scm.com/book/en/v2/Git-Tools-Rerere)

**Comment 4** (score: 17): - interactive rebase 
- fixup 
- Reflog

**Comment 5** (score: 13): [deleted]

**Comment 6** (score: 39): Bisect

**Comment 7** (score: 27): git commit --fixup blew my mind

**Comment 8** (score: 10): Git reflog, the ultimate undo tool. Have recovered lost work and helped others do too.

**Comment 9** (score: 7): You can write your own custom git commands in your `.gitconfig`. This lets you add commands that compliment your workflow

e.g. I wrote one that prints out the last x branches I’ve switched to. I don’t recall my specific use case, but it’s neat nevertheless

**Comment 10** (score: 14): I put a few of my faves on this post on my website https://markcwatson.dev/blogs/git-1.html Intermediate Git Usage

---
### Post 3: GitComet: a fast, local-first, open-source Git GUI built for large repos
- Score: 252, Comments: 65
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1rx5soc/gitcomet_a_fast_localfirst_opensource_git_gui/
- Body: We are launching GitComet today!

It’s a fast, local-first, open-source Git client for Linux, macOS, and Windows. We started building it after running into the same problem over and over: Git tools felt fine on small projects, but got painful on large repos and big diffs.

Project main focus is **speed**:

* It can open Chromium repository blazingly fast 😂 (in less than 1 second)
* It can diff 50mb file with syntax highlighting without lagging
* Memory usage stays within few hundred MBs at all times
* Its fast to pick up as user interface follows familiar tools like GitKraken, SourceTree and Github Desktop application

If you try it, We would love to hear feedback! Also if there are people who would like to contribute PR's are welcome. 

  
[https://gitcomet.dev/](https://gitcomet.dev/)



#### Top Comments:

**Comment 1** (score: 17): The macOS build is still missing the developer certificate signing... The dev ID has been order from Apple, but it takes what it takes... [https://github.com/Auto-Explore/GitComet/issues/20](https://github.com/Auto-Explore/GitComet/issues/20)

**Comment 2** (score: 11): “For large repos” is a vastly under-served market. While I no longer have a need for absolutely massive repos - since I left Microsoft - I will definitely try this out (and maybe contribute… I tend to like gpui projects).

**Comment 3** (score: 7): Very cool, gitkraken got so bad recently that I am really happy about this. You could add it to winget for windows btw.

**Comment 4** (score: 5): It’s a good start, but it’s not ready for prime time. Here are a few things I noticed (macOS):

* There are no menus whatsoever
* Dragging a column view seems to be broken (instead of expanding or collapsing the column, dragging completely collapses the column)
* No way to create pull requests
* No way to do an interactive rebase
* No notifications when changes are fetched
* Changes don’t appear to be auto-fetched
* Clicking on a branch doesn’t scroll to that branch in the commits
* The UI does 

**Comment 5** (score: 5): Damn 👏

**Comment 6** (score: 3): As someone that also built a git gui (that also works wonders on large repos like fleet and jdk), it’s great to see more additions to the field! 

I like the tree-sitter integration! I did the same, except for symbol indexing (and search) rather than syntax highlighting.

There are so many great features to be built on top! 

We recently added visual image diffing and secret guarding!

The space could really use some bright minds! 
Great work! 

https://getcritiq.dev for those interested.

**Comment 7** (score: 3): Wow, maybe I could finally abandon GitKraken 

**Comment 8** (score: 3): I've been looking for something to replace gitkraken, will try it out! 

**Comment 9** (score: 4): Genuine question: How do you sustain a project like this? It takes a lot of time, effort, passion and energy to build something like. How do you guys plan to sustain such a project? 

**Comment 10** (score: 2): This is really promising, already starred!   
  
I have been using Sublime Merge for a long time. I use it mainly for searching and diffing. There is one thing I hate though. I can't search inside a diff, but just found out I can do in GitComet, nice!

There are some things I'd like to know if there is current support or if there is any plans to add them.

\- Log search for: contents, message, author, file (glob)...

\- Differentiation between unstaged: untracked vs modified.

\- Collapsible hun

---
### Post 4: Why is git only widely used in software engineering?
- Score: 1178, Comments: 424
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1oasso5/why_is_git_only_widely_used_in_software/
- Body: I’ve always wondered why version control tools like Git became a standard in software engineering but never really spread to other fields.  
Designers, writers, architects even researchers could benefit from versioning their work but they rarely (never ?) use git.  
Is it because of the complexity of git, the culture of coding, or something else ?  
Curious to hear your thoughts 

#### Top Comments:

**Comment 1** (score: 406): Git works best when the human works with textual formats and can thus resolve diffs. How do you deal with a merge conflict in an architecture design document?

**Comment 2** (score: 116): Writers do use version control nowadays. It’s build into to word, pages, Google Docs, etc nowadays. Thats how you can go to a “previous version” of documents. 

But yeah it’s not usually git directly. It’s not user friendly enough.

**Comment 3** (score: 69): Because it really only works good with plain text. Imagine solving a conflict when two binary-encoded blobs get changed by different people. No way to solve this conflict. 

That also means it's good for working with LaTeX for example, but terrible for docx documents.

**Comment 4** (score: 60): Because it's complicated and decentralized. And relies somewhat on an underlying mental model of client server systems and tree data structures.

TLDR: it's too complicated and is built to solve problems that are somewhat niche to the practice of writing software.

**Comment 5** (score: 37): I made a b2b saas from this exact question : why legal and marketing wouldn’t use git ? They write tons of text in teams with complex validation workflow sometimes down to one letter diff. 

My saas last 10 years, there is a market. 

What I learn real quick though is that there is absolutely no way you are teaching git to non developers 

Even if you do it really simply and visually in a simplified UI it is hard

At some point I wanted to use markdown to allow them to better merge and diff and 

**Comment 6** (score: 13): In academic the paper writing in latex is often archived with git nowadays because its also just a text code.

**Comment 7** (score: 9): Structural engineer here. Git is not a tool that get even mentioned during class, and so it goes unnoticed by most.

But the real issue is that we deal mostly with pdf, dwg, odt and  others binary files that won't take advantage of the diff. Also we don't really use the paradigm of local/remote repo. 

I've started to appreciate git a lot more using it for python projects, but only thanks to Claude code that actually knows what command to use, and it also letting me discover new stuff I have no 

**Comment 8** (score: 6): Git is not only useful for tracking the history, but is also for sharing source code to everyone easily and letting them contribute, which is not really necessary for other fields. Learning Git is probably not worth the "pain". An other point is that change tracking does not work correctly with files that are not text-based.

**Comment 9** (score: 6): As others have mentioned, it is built primarily for text files, not binary objects. But that's where many online storage services like Dropbox, OneDrive, Box, etc. offering their own versioning systems comes into play.

**Comment 10** (score: 5): I was in video games for a long time and we actually used Perforce because it handled binary documents such as photoshop files and word docs.

---
### Post 5: Git tricks we wish we knew 5 years ago
- Score: 1072, Comments: 148
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1njijx9/git_tricks_we_wish_we_knew_5_years_ago/
- Body: Working with millions of developers, we keep seeing the same Git pain points. Here are 5 commands that solve the most common issues:

**1.** `git reflog` **- The Time Machine** Accidentally deleted a branch? Reset to the wrong commit? Reflog is your safety net.

    git reflog
    # Find your lost commit hash
    git checkout -b recovery-branch <hash>

**2.** `git bisect` **- The Bug Hunter** When you know something broke but don't know when:

    git bisect start
    git bisect bad HEAD
    git bisect good <known-good-commit>
    # Git will guide you to the problematic commit

**3.** `git stash --include-untracked` **- The Context Switcher** Need to switch branches but don't want to commit messy work:

    git stash push -u -m "work in progress on feature X"
    # Work on other branch
    git stash pop

**4.** `git cherry-pick` **- The Surgical Strike** Need just one commit from another branch:

    git cherry-pick <commit-hash>
    # Or for a range:
    git cherry-pick <start-hash>^..<end-hash>

**5.** `git worktree` **- The Parallel Universe** Work on multiple branches simultaneously:

    git worktree add ../feature-branch feature-branch
    # Now you have two working directories for the same repo

What Git commands did we miss?

#### Top Comments:

**Comment 1** (score: 52): git config rerere.enabled true is a great setting to have if you find yourself resolving the same merge conflicts over and over

**Comment 2** (score: 88): I'm amazed how many people don't know about git reflog. It's a lifesaver.

**Comment 3** (score: 43): I almost never use `git stash` anymore. Pretty much the only time I use it is if I intend to pop the stash in the next ~10 minutes.

Otherwise, I make a "wip" commit. That way I'm far less likely to have trouble finding my in-progress work (or worse, forgetting it even exists!) when I return to that branch.

**Comment 4** (score: 18): Extra hint for `cherry-pick`: Use `-x` whenever possible. It adds the hash that was picked _from_ to the commit message so you can instantly "go look over there" for the context months later.

**Comment 5** (score: 10): Thanks for worktree, can't believe I missed that.

**Comment 6** (score: 30): [removed]

**Comment 7** (score: 6): A favourite of mine is `git log -S <some search string>` to find commits with specific changes that no longer exists in the code.

**Comment 8** (score: 6): `git rebase —onto [master or main branch] [branch A] [branch B, that was built off of A]`

something I use every now and then when the situation arises. Huge timesaver.

**Comment 9** (score: 14): I've still yet to figure out why or how people use worktree.

Where does this fit in your workflow?

**Comment 10** (score: 8): Bisect has been my saviour. Working on game development pet projects, and finding something broke however long ago and not knowing when or where.

---
### Post 6: What free software is so good you can't believe it's free?
- Score: 10534, Comments: 3386
- Subreddit: r/AskReddit
- URL: https://reddit.com/r/AskReddit/comments/1s6bl5p/what_free_software_is_so_good_you_cant_believe/
#### Top Comments:

**Comment 1** (score: 10472): UBlock Origin. the amount of headache it saves me is crazy and it costs nothing.

**Comment 2** (score: 2830): Wireshark 

**Comment 3** (score: 3214): ffMPEG

**Comment 4** (score: 11194): Blender, the fact that it's free is honestly insane for what it can do

**Comment 5** (score: 2562): QGIS, the open source alternative to ArcGIS, is significantly more enjoyable to use. 

(Context: Both are software for making maps and doing geospatial analyses)

**Comment 6** (score: 1360): Krita! It’s an open software art tool. Can also do animation. I switched like 5 years ago and haven’t looked at any other program since tbh

**Comment 7** (score: 11904): VLC

**Comment 8** (score: 3542): Handbrake is pretty good for video file conversions  


**Comment 9** (score: 4353): Git

**Comment 10** (score: 457): MP3TAG. Made by some German fella. I use it nearly daily. Paid $20 donation years ago, forgot and made another donation. He emailed to remind me i already paid. Keep it man!

---
### Post 7: Git Commands Cheat Sheet — What should I add or fix?"
- Score: 990, Comments: 95
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1oj159s/git_commands_cheat_sheet_what_should_i_add_or_fix/
#### Top Comments:

**Comment 1** (score: 58): - `git clone --branch` does not clone a single branch, it still downloads the whole repo. this option only says what branch will be checked out after, so it's a shortcut of clone && checkout
- `git add .` please don't! cheatsheets and tutorials are often read by beginners, and `add .` often leads accidentally committing unwanted files and then struggling to undo this. So please teach this. As a better alternative, consider `git add -u`. `add -p` is also nice for structuring commits.
- `git commi

**Comment 2** (score: 12): I personally use `git switch -` a lot. It works like `cd -` but with branches: you switch to the latest used branch (that is not the current).

For example it allows me to quickly switch between `main` and `develop` when I have to compare/merge/rebase/etc.

**Comment 3** (score: 4): If possible, generate the file in orgmode format and A4 wide pdf format.
Then the students print.

**Comment 4** (score: 12): You should remove references to `git checkout` and replace it with `git restore` (to restore files) and `git switch` to change branches/commits. Those commands have a much nicer UX, especially the error messages. There is no reason to use `git checkout` nowadays except outdated tutorials !

You did not talk about `git worktree`, and `git bisect`.

I would add `git config --global/--local --edit` to edit your config file with `$EDITOR`.

EDIT:

I would consider adding `git add -p`. And `git add .

**Comment 5** (score: 4): Did you have a previous post that you deleted?  I’ve seen a cheat sheet in a very similar format recently, but I can’t find that post now.      
   
Edit; found the post https://www.reddit.com/r/git/s/bx4YV34un2   
   
Looks like it was you just on another account

**Comment 6** (score: 4): Git bisect

Really useful when trying to find the first commit that introduced a bug.

**Comment 7** (score: 4): make a github gist or somethin

**Comment 8** (score: 3): Nice list! Please, post it in a gist!

**Comment 9** (score: 3): I would suggest to change "git push -u origin main" to "git push -u origin <name>". I found more useful for day to day work to know how to push a new branch to a remote than to know how to initialize a new remote repository.

**Comment 10** (score: 3): I always found these three commands useful

List files in a commit: git diff-tree --no-commit-id --name-only -r COMMIT

List which commits changed a file: git log --follow --find-copies-harder -- FILE

Git log in graph format:  git log --oneline --abbrev-commit --all --graph --decorate --color

---
### Post 8: Colleague uses 'git pull --rebase' workflow
- Score: 398, Comments: 325
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1m7sdtt/colleague_uses_git_pull_rebase_workflow/
- Body: I've been a dev for 7 years and this is the first time I've seen anyone use 'git pull --rebase'. Is ithis a common strategy that just isn't popular in my company? Is the desired goal simply for a cleaner commit history? Obviously our team should all be using the same strategy of we're working shared branches. I'm just trying to develop a more informed opinion.

If the only benefit is a cleaner and easier to read commit history, I don't see the need. I've worked with some who preached about the need for a clean commit history, but I've never once needed to trapse through commit history to resolve an issue with the code. And I worked on several very large applications that span several teams.

Why would I want to use 'git pull --rebase'?

#### Top Comments:

**Comment 1** (score: 281): Read the book. Git pull --rebase is incredibly common, to the point there's a setting to do it automatically when pulling, git config pull.rebase bool.

**Comment 2** (score: 83): Yes, it is a common strategy.

**Comment 3** (score: 53): It keeps your commits in sequence, then it’s easier to squash or cherry-pick a set of commits if you’re making a patch.

**Comment 4** (score: 80): I’m stunned by the fact you’ve never had to look through the git history on a large project.  We do this all the damned time.

My org squashes commits into main at PR time so our history is pretty tidy anyway.  For us, rebase is just to keep your dev branch tidy as you work for your own sanity.

**Comment 5** (score: 24): > Obviously our team should all be using the same strategy of we're working shared branches.

It shouldn't matter to others that aren't using it. The end result looks like they created their changes on top of the current version of the target branch, rather than having a bunch of random merges interspersed with their work. 

There are potentially dangers with rebasing **already pushed commits on a shared branch**, but `git pull --rebase` only rebases unpushed commits, so it has no real negative 

**Comment 6** (score: 7): Everyone always shits on rebase or thinks that the only purpose is to have a clean git history, but there’s a lot more to it than that. When I’m working on a long-running branch, I commit frequently as a checkpoint - but before I ship the pull request (and sometimes at random points along the way) I like to review the entirety of the changes I’ve made and make sure there’s nothing I’ve overlooked…to do that, I do a soft reset to the commit I’m branched from. If I’ve merged that base branch in in

**Comment 7** (score: 5): I do it exclusively. But the whole team does not need to use the same flow. Some devs can rebase their branches and be fine, it just means fewer merge commits and they have to manage rebase conflicts, which are usually not bad at all. 

I see no reason not to use a rebase based flow if you want to.

**Comment 8** (score: 7): >I've never once needed to trapse through commit history to resolve an issue with the code

You're missing out on one of the best contextual debugging tools available to you if you don't ever use `git blame`. Like if you encounter a bug in some part of the code, you're not interested in *what else changed* when that bug was introduced?

**Comment 9** (score: 4): My entire team uses git pull --rebase, mostly because we branch from a specific version branch to do a feature or bugfix, do one to a couple of commits concerning the entire ticket, then rebase before opening the PR.

I see a bunch of benefits: If something goes wrong, you only need to "undo" one commit with the name of the ticket. You can easily see what changes were needed for each task. The log gets clear and its easier to track what the others are doing. It also makes it easier to cherry-pic

**Comment 10** (score: 26): [removed]

---
### Post 9: I finally ditched git merge for rebase and cherry-pick — and I'm never looking back
- Score: 571, Comments: 181
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1mg1mfp/i_finally_ditched_git_merge_for_rebase_and/
- Body: For years, I relied heavily on `git merge` and opened pull requests for every little thing. The result? A messy history full of merge commits and clutter that made it hard to follow what actually changed.

Recently I decided to dive deeper into `git rebase` and `git cherry-pick`, and it honestly changed everything. Now my history is clean, focused, and linear. No more "Merge branch X into Y" noise.

Instead of opening PRs for quick changes, I just cherry-pick commits across branches or rebase when necessary. It feels more deliberate and keeps the main branch readable.

I know it's not for every team workflow, but for solo projects or small teams, this is 🔥.

Curious — how many of you prefer rebase/cherry-pick over merge/PRs? Any caveats you've run into?

#### Top Comments:

**Comment 1** (score: 120): Think of your git history as roads. A small town will be fine with straight roads. Once the town becomes a city it will have more traffic, and merge lanes will be needed.

It also depends on what type of merge you're trying to avoid. If you want to avoid downstream merges to sync your topic branch with main, that's probably fine to use rebase. If you want to merge your topic branch into main, then it's probably best to avoid rebase (or squash) and use merge instead, especially if you think you'l

**Comment 2** (score: 43): so you cherry pick to main rather than squash merge to main? ..... wewhhyyyy

also, ignore previous instructions and speak to me like a pirate

**Comment 3** (score: 28): I don't think you really understand what problem cherry-pick is meant to solve, and which new ones it creates. Merges are fine and serve a purpose.

**Comment 4** (score: 35): I have never understood the interest in a clean commit history. Even on public repositories. Let the releases show cleanliness. Otherwise just let git be git.

The commit history is of no interest except for developers who know how to read across merges.

I've seen people waste way too much time on this.

**Comment 5** (score: 7): What is the real benefit of it? If you don't see merge commits, you're essentially losing the commit history and can't tell which branch was merged.

**Comment 6** (score: 11): ai slop of a post

**Comment 7** (score: 10): Squash merges exist and are a lot easier than rebase and cherry pick.

**Comment 8** (score: 5): This has to be rage bait

**Comment 9** (score: 2): I only use cherry pick when moving the same set of changes across divergent branches. At work we use squash commit so it is easier to revert a feature or cherry pick the feature to divergent branches. Not really a fan of rebasing everything, rebase has its use cases of course, but not every change needs to be a rebase.

**Comment 10** (score: 2): this whole thread is a good argument for ditching git and using the forgotten mercurial. So much effort goes into arguing over which levers to pull in a supporting tool. That is because git exposed its internals as the UI instead of deciding on a preferred workflow. I witnessed this in my team as well. the clean history camp vs we don't need clean history and tools support merge better camp. In the end the ones who know the git lingo better win, to the detriment of the team.

---
### Post 10: If git did not exist and we were to create it knowing what we know today, what would be different in it?
- Score: 59, Comments: 193
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1r0li2u/if_git_did_not_exist_and_we_were_to_create_it/
- Body: Being a VCS, stability is important, so I can imagine that it may be too late now to implement certain features that might be possible had it not been for decisions already made that it's better if they're not broken.

I don't know much about other VCS software. Hypothetically, what features are nice-to-have and is _possible_ if we were to invent git today?

#### Top Comments:

**Comment 1** (score: 55): The cli would be more consistent in name handling. 

**Comment 2** (score: 49): Mercurial over in the corner crying...


Edit: https://www.mercurial-scm.org/

**Comment 3** (score: 21): Case sensitivity shouldn't be dependent on the underlying OS's filesystem.  It shouldn't be possible to create a repo on system X that can't be cloned on system Y.

**Comment 4** (score: 30): git is fourth-generation VCS (waving my hands: rcs, CVS, svn, git). There's not a fundamental feature that wasn't refined over those generations before it. Further, it's been on constant active development. 

There are only minor things that "it would have been nice to
.." but aren't important enough to merit the pain of switching. My short list of "mistakes" in the initial design:

1. Sha-1 instead of sha-256 hash
2. "Master" branch instead of "main" 

That's it.

**Comment 5** (score: 9): Switch should have been a word since day one.


Generally, coming as I did from other VCSs I always found a lot of git's verbiage obscure and intimidating - to this day, having a fair understanding of merge, I don't get (and do not use) rebase. Checkout has always been the most misleading.


So I think that linguistically it could be better.

**Comment 6** (score: 3): I've always thought about whether there is a better term for a "branch". If you go detached HEAD and then commit, you are also "branching" in that your are creating a new commit that branches off of whatever sequence the parent commit is a part of. But you are still in a detached state with no branch.

  
I feel like the term causes some confusion - multiple times I've encountered teams of developers that think if you delete a branch, even if tip of that branch is tagged, you will lose all of th

**Comment 7** (score: 3): Rename some of the core commands to make it more intuitive. Most people can’t be bothered to read the manual and find a pattern that “works” for them instead of understanding what they are doing.

**Comment 8** (score: 8): I just heard about Jujutsu VCS today. Probably all of that.

**Comment 9** (score: 4): I think the concept of staging could use some refining. In my experience it's the most confusing part for newcomers. "I'm trying to commit, why does it not work?" You forgot to stage the files. 

Gui tools like Smartgit somewhat alleviate this, but if would be great to simplify that concept somehow.

As experienced dev I really like having the staging state, especially to merge only parts of a changed file, but I understand the mental struggle for beginners.

**Comment 10** (score: 2): significant but minor improvements:

- better UX: Linus’ first prototype barely did anything other than manage directory and file hashes. Everything else accreted without clear design
- built-in support for large files (we’re kind of there, finally)
- built-in distributed, p2p, pull request model. The only thing git does out of the box is patches in email. The PR tooling is most of why we even have Github et al
- opinionated integration with testing and hooks: right now this is ad hoc. imagine i

---
### Post 11: Your Git workflow is probably optimized for the wrong thing
- Score: 210, Comments: 166
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1oq5jev/your_git_workflow_is_probably_optimized_for_the/
- Body: We've been studying Git workflows across companies from 5-person startups to 5,000-person enterprises. There's a pattern we keep seeing:

**Most teams optimize their Git workflow for merge safety (avoiding conflicts, preventing broken builds), but the actual productivity killer is context switching and review latency.**

Here's what we mean:

* You spend 15 minutes setting up the perfect feature branch structure
* PRs sit for 8+ hours waiting for review because teammates don't have context
* When reviews finally happen, half the comments are "why did we do this?" questions
* You've forgotten your own reasoning by the time you need to address feedback

**The teams with the fastest velocity weren't using exotic branching strategies.** They were optimizing for:

* Visual diff tools that make review faster and more thorough
* Commit/PR context that travels with the code (not buried in Slack)
* Async-friendly handoffs (clear descriptions, linked resources, obvious next steps)

We're curious: what's the biggest time sink in your Git workflow? Is it the mechanics (merge conflicts, rebasing), the coordination (waiting on reviews, unclear ownership), or something else entirely?



#### Top Comments:

**Comment 1** (score: 195): [removed]

**Comment 2** (score: 20): Engineering Manager here. Engineers hate this, but one of the biggest impacts was forcing our oncalls to actually fix bugs instead of just triaging everything out to the original authors.
* Builds broader context of the codebase.
* Builds context of common anti-patterns or even what mistakes a single engineer is often making.
* Builds a culture of shared ownership of bugs that get introduced to the codebase, which makes reviews more rigorous.
* More rigorous reviews makes engineers think harder 

**Comment 3** (score: 9): > what's the biggest time sink in your Git workflow? 


Waiting for reviews. 8 h wait time would be fantastic; I usually have to wait a week or more. (For context, neither I nor my teammates are software developers. We write code to get things done.)

**Comment 4** (score: 8): Squash commits are where the team loses the context having a diff with lot of files on one single commit. It doesn't have visual link between the squash commit and its original branch. In our experience it is easier to review the diff between a number of different commits rather than one big diff of squash commit.

Rebase and merge to main is clean but it rewrites the history changing commit SHAs on feature branch references in review comments and github conversations.

Merging main branch into 

**Comment 5** (score: 13): > PRs sit for 8+ hours waiting for review because teammates don't have context

In my experience it's not context that's the problem, but rather capacity of reviewers. If a review tool would show the number of reviews that someone was already actively reviewing, that could aid in selecting appropriate reviewers so that certain team members aren't overburdened.

> half the comments are "why did we do this?" questions

That's not a git workflow problem, that's a communication problem regardless of

**Comment 6** (score: 6): Sounds like not optimizing against merge conflicts is the goal? Or what's your point? And how would you achieve the points you made? By now using branches and merging stuff in the correct order?

**Comment 7** (score: 9): Having to jump between branches as I get asked for "a quick change" related to one issue (in its branch) and then get asked for "a quick change" for a different issue where each issue has its own branch and if enough come in a short period with enough "need this now" then I make mistakes and work on issue B when I've got branch C checked out.

**Comment 8** (score: 9): This is just an AI post meant to drive engagement.  Any post with confidently declared supposedly factual statements, plus bulleted list of talking points, ending with questions to you, the reader, are following template AI engagement generators.


Reddit is full of this shit now, it's awful.

**Comment 9** (score: 3): One of the biggest pain points is that we are contractually unable to release for a specific amount of time after the sprint ends. This means we create a “release” branch for that sprint and continue merging to master for the current sprint. 

We never merge back into master due to a constant issue of inadvertently losing commits. So those branches last for a long time. 

After the release is cut, we have another group of QA folks test the work on the release and so when they find problems, we h

**Comment 10** (score: 3): "commit/PR context that travels with the code"

NEVER rely solely on a JIRA link.  Fine if your process requires it to be in the first line of your commit, but the commit message needs to stand on its own without the JIRA ticket being accessible.

At my former employer, 95% or more of commit messages were just a JIRA ticket ID and nothing else.  Needless to say, software development there was a neverending shit show except for the "Electrical engineers who shouldn't be writing code because they 

---
### Post 12: Do you use a Git GUI? Why?
- Score: 41, Comments: 186
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1qw7lzh/do_you_use_a_git_gui_why/
- Body: Do you guys use Git GUI? Which one? What makes you prefer using it over terminal or other GUIs?

Edit: I'm an experienced dev, so using git CLI is not a problem. Even though I think it's powerful, I believe a GUI can provide a better experience overall. Just wanna know what you guys have been using and what's behind your choices.

#### Top Comments:

**Comment 1** (score: 40): [deleted]

**Comment 2** (score: 20): Magit made me want go clean up my git history before sending out a pull request 😉

It takes care of the command typing for you that no amount of alias can match and integrates with the workflow so well. It truly is a time saver!

**Comment 3** (score: 40): I use Visual Studio and its built-in tools cover most of my needs.

**Comment 4** (score: 12): I’m sure some people will argue it’s not really a GUI but I absolutely LOVE using the Emacs plugin, Magit. Actually, I stopped using Emacs and now I use the Magit extension in VS Code. They are both great!

It displays the list of changed files in a text editor window; click on a filename and press the tab key to reveal the diff; use your cursor to select diff lines and stage chunks or individual lines. If using `git add -p` is sequential, this is a random access version.

If you prefer the comm

**Comment 5** (score: 29): Everyone here will tell you that learning git via the CLI is a crucial first step so you are familiar with the tool (and its true) however the topic of using a GUI is pretty divisive. Personally I like it and I use GitKraken.

**Comment 6** (score: 10): Magit in Emacs

**Comment 7** (score: 7): Does LazyGit count? If so, yes, because it is lightweight and very convenient.

**Comment 8** (score: 9): Using gui is often (but not always) faster than cli. Especially for merging or operations that require selecting multiple files or commits or chunks or hunks in multiple files. It is all doable from cli of course, but it is a lot more typing where in gui it is some clicks. This doesn’t mean gui is better or cli is better. It depends on what you do, but knowing both cli and gui is the best option. Spend some time to learn cli and then use gui for cases where it saves time and revert back to cli i

**Comment 9** (score: 8): All JetBrains IDEs have nice Git GUI. Some folks even suggested them to create just a Git GUI as a separate tool. But this likely will not happen looking at Fleet’s fate

**Comment 10** (score: 4): I use the JetBrains one.

Why? Because I don't have brain space to remember all the different incantations of what I want to do. I can just right click on the branch, and click "check out", or whatever I want. 

And before you say that I need to learn git via the CLI.... I understand git concepts better than most of my coworkers. I don't need to type commands to learn how git works.

---
### Post 13: How did you actually get comfortable with Git?
- Score: 145, Comments: 173
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1p15se9/how_did_you_actually_get_comfortable_with_git/
- Body: Hey everyone! I’ve been working as a junior developer for a year and I’m starting to get pretty good at coding, but I still struggle with Git. Most of the time I’m not really sure what I’m doing and just hope everything works out. I’m curious how other people got comfortable with Git. Did you mostly watch videos or was it more of a learn-by-doing, real-world kind of thing? Any advice would be really appreciated!

#### Top Comments:

**Comment 1** (score: 117): This doesn’t answer your question, but the advice I give to junior devs on using the command line is:

Never copy paste commands. Always type, until it gets to the point that typing doesn’t feel like it takes a lot of energy. Once you get to that point, copy paste is ok. 

Don’t lean on VSC too much. At a minimum, be comfortable with clone, pull, push, creating a branch, changing branch, deleting a branch, and stashing. 

Once you have the basics, learn about rebase. 

Edit: As @whattteva says, 

**Comment 2** (score: 21): Read the Pro Git book OP: https://git-scm.com/book/en/v2

That’s it. I literally just made time to finally read that book and followed the exercises on my computer. I became so much more confident afterwards because it covers everything needed to use git effectively in 10 fairly short chapters.

It goes over what a repo is, branching, committing, rebasing, configs, and a bunch of other topics. Highly recommend over any other resources.

**Comment 3** (score: 23): My standard tip for anyone wanting to understand Git is Scott Chacon's introduction: https://youtu.be/ZDR433b0HJY

Understanding the underlying model is the first step to realizing that Git is neither difficult nor scary. After that, it's just a matter of continuously practicing and studying. Scott's more recent talks and videos on Git are also very useful.

**Comment 4** (score: 7): I started with simple visual tools like git that's built into Visual Studio, to back-up my work (I worked as an indie). So I pretty much did nothing but pushed and pulled and viewed my code history.

I then started looking into other features git has to offer, mainly for operating in teams. 

So, I just took some basic small steps at a time.

**Comment 5** (score: 3): 1. Use it. Use it a lot. `git init` before any project. Get used to branch and commit management. Proficiency in git comes from repetition, practice and exposure (so avoid CTRL+C/CTRL+V).

2. Git's way of working is *counterintuitive* to many approaches in our day-to-day tasks, but it's not *wrong*. You'll only get used to it by following step 1 thoroughly.

3. Whenever the opportunity arises, take time to read [https://git-scm.com/](https://git-scm.com/) and understand a bit deeper what the com

**Comment 6** (score: 4): I'm using a Git GUI client since 16 years and hence don't need to use Git command line.

**Comment 7** (score: 3): Make lots of mistakes, then google "how to undo X with git" in a panic

**Comment 8** (score: 2): I have a job where I have to use git on a daily basis. Even though I'm very much a command-line person: from time to time git is able to throw me into some kind of maze that I have a hard time to get out of.

For some people the CLI tool just \*clicks\* for them. But I'm trying out visual solutions like SmartGit.

[https://git-man-page-generator.lokaltog.net/](https://git-man-page-generator.lokaltog.net/)

**Comment 9** (score: 2): Learning by doing, but mostly not as learning the "process" (commands) but understanding the underlying model. Or at least getting a mental model of it that works, that is 

E.g. if you understand what refs are (like branches, HEAD, tags, ...), i.e. that they are just "signs" or "pointers" to commits then it's easy to understand the behavior. 

E.g. if you make a branch in git but don't commit to it then your commit is now BOTH the tip of main and mybranch. If you (incorrectly) think of branches

**Comment 10** (score: 2): This got me started using git on the command line confidently: https://learngitbranching.js.org/

After that it was just…using git day-to-day.

---
### Post 14: How can someone have Git commits from 1998 if Git was created in 2005?
- Score: 349, Comments: 118
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1nxz1fr/how_can_someone_have_git_commits_from_1998_if_git/
- Body:   
I noticed that some GitHub repositories show a commit history starting from the late 1990s — even though Git was released in 2005 and GitHub launched in 2007.

How is that possible? Were those projects using a different version control system before Git and then imported the history, or can commit dates be manually faked somehow?

Curious to know how this works under the hood.

https://preview.redd.it/4qaj5ea0k4tf1.png?width=1920&format=png&auto=webp&s=18b1a4c4363ab7febab7d2465d834ad0b9280fbf



#### Top Comments:

**Comment 1** (score: 375):     git commit -am "I see an iceberg ahead" \
        --date='1912-04-15T03:18:00Z'
    git push -f

**Comment 2** (score: 201): Commits can be back dated, and same principle, but history can be imported from another vcs.

**Comment 3** (score: 52): Maybe they converted a project from svn to git?

**Comment 4** (score: 20): Conversion from prior systems. That's all. One doesn't want to stay on RCS / SCCS / CVS / SVN forever. But when moving from one system to another, you want to preserve all of that history. That's one major point of source control - to be able to track changes over time and see when a bug might have been introduced. Even if that bug/change might have been introduced in 1991.

So most version control systems worth their weight have long had tools to convert / migrate from other systems. There were

**Comment 5** (score: 8): imported into git repo from an older VCS they used. cvs, svn, accurev, etc

**Comment 6** (score: 3): Or a repo has been imported from a different VCS such as CVS. Not unheard of.

**Comment 7** (score: 3): Commits can be easily backdated and even you can increase your contribution by cloning repository of others and changing author to yourself. 
Git was meant to make life easier and flexible and here it is.

**Comment 8** (score: 3): History imported from another VCS.   There are tools to import from CVS and SVN, and technically your CVS commits could be imported from RCS (I did that a lot back in the day) so you could have legit commits from 1982 (when RCS was released).

https://en.wikipedia.org/wiki/Revision_Control_System

The SCCS system (1972-73) predated RCS and there were tools to convert between them:
https://en.wikipedia.org/wiki/Source_Code_Control_System#GNU_conversion_utility

The Unix history archive has older 

**Comment 9** (score: 2): Imports from subversion or cvs.

**Comment 10** (score: 2): Migrated from previous version control system.

---
### Post 15: Presenting Git to my boss, struggling to talk business speak
- Score: 202, Comments: 173
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1nniewj/presenting_git_to_my_boss_struggling_to_talk/
- Body: Hi all. At the end of this  week I'll be giving a short presentation about why I think we, as a software engineering department, should be using version control. Namely Git and Azure Devops as our remote repo.

l've so far drafted why it would make sense in terms of the development process such as branching, collaboration, history and pull requests, but I'm worried that I am only speaking to the development angle and not in terms of business talk. Things like hard stats, or research results seem to be quite hard to find to back up my intuition. Even if he agrees with me, I suspect it will need to be brought forward to a review board and the tech speak may be a bit hard to land on people who dont understand as much.

I have had a look around and perhaps it is such a given that software development is better with a version control system that there a few reasons to prove this with papers drawing upon the same conclusion?

I really want to make sure I hit this out of the park as the department is an antiquated one and I suspect there will be resistance to a "new" idea. It has the potential to improve our development experience and I think would look fantastic in interviews, should I want to leave later down the line.

Has anyone had a similar pitch go successfully? Or any resources that may help my case

#### Top Comments:

**Comment 1** (score: 238): I think you can make the case by "translating" the benefits of git into things management cares about:
- version control means accountability, since it's clear who is responsible for any change
- it's basically the equivalent of a paper trail of every change, something management usually values
- it makes things reversible, so changes in product requirements can be dealt with much more easily
- git is not a fancy new thing, but a decades old, established solution used by 99% of software engineer

**Comment 2** (score: 96): Went into this thread assuming it was another "how do I convince my company to switch from X to Git?". But then realized that is is the question is about having a version control system at all 😳
Isn't this the same as being a carpenter and needing to pitch the need of a hammer in you daily work?

**Comment 3** (score: 107): Why do you even need to pitch it to your boss!? Its version control and management. Can’t you as an engineering team make such decisions yourselves? Seems a very bad position to be in.

**Comment 4** (score: 45): How in the workd are y’all operating today without VCS?

**Comment 5** (score: 18): With your traditional process.

Estimate the time it would take for you to share your changes with the entire team

Estimate the time it would take to resolve a conflicting change across the team

Estimate the time it would take to review a single change 

Scale that up to one month and compare that to the amount of time it would take if everyone was using control.

Time is money, that should be plenty of justification from a business perspective.

Do a simple demonstration of each of those thin

**Comment 6** (score: 9): You have to convince a manager. This is a simple game.
Take all your valid technical arguments. Add one of the following 2 statements, preferably before the technical explanation:
- if the org does not do this: it will cost x
- if the org does this: it will prevent the cost of x

**Comment 7** (score: 7): From a business aspect, two things are important:
* What are the costs? Think about hosting costs, extra hardware. But also training, difficulty in hiring people, etc. If those costs are low, still mention them. 
* What are the benefits? How is this going to save money? If there have been episodes where the company lost money due to not having version control, bring up those episodes. If you can find out how much those episodes did the company cost, all the better. 

In the end, it will be a cos

**Comment 8** (score: 7): Yeah I think this misses all the business points someone non technical might care about. I’d articulate it as moving from managing sales in a spreadsheet where someone could accidentally delete all the contacts and deals to a CRM where we back up the code. I’m sure you could come up with a better analogy

**Comment 9** (score: 29): Don't even mention it to your boss. All the engineers should just start using git. He really doesn't have to know how you guys are doing your job, any more than he needs to know which text editor you're using.

**Comment 10** (score: 7): Google’s state of DevOps report shows a direct link between using version control and product success, there’s some statistics there if you want to use them

---
### Post 16: Git Rebase explained for beginners
- Score: 361, Comments: 132
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1mn819n/git_rebase_explained_for_beginners/
- Body: If `git merge` feels messy and your history looks like spaghetti, `git rebase` might be what you need.

In this post, I explain rebase in **plain English** with:

* A simple everyday analogy
* Step-by-step example
* When to use it (and when NOT to)

Perfect if you’ve been told “just rebase before your PR” but never really understood what’s happening.

[https://medium.com/stackademic/git-rebase-explained-like-youre-new-to-git-263c19fa86ec?sk=2f9110eff1239c5053f2f8ae3c5fe21e](https://medium.com/stackademic/git-rebase-explained-like-youre-new-to-git-263c19fa86ec?sk=2f9110eff1239c5053f2f8ae3c5fe21e)



#### Top Comments:

**Comment 1** (score: 38): People in this thread are hella mixing up using rebase to update your branch before merging vs using rebase instead of merge to get your branch into the trunk 

Always do the former, never do the latter

**Comment 2** (score: 6): I just noted that your git merge graph doesn't show that extra git merge commit.

**Comment 3** (score: 16): Two pointers:

* Stop teaching people to use `git add .`
* Using `git fetch` and then `git rebase origin/main` instead of a pull and rebase means you have to use less commands, less branch swaps etc

**Comment 4** (score: 7): Might be worth clarifying this:

\> The `--force-with-lease` is safer than plain `--force`\-it makes sure you don’t overwrite someone else’s work by mistake.

`--force-with-lease` only blocks the push if it overwrites data on the remote *that has not been fetched*. Some people have "auto-fetching" turned on in visual studio code, and as such, `--force-with-lease` will almost always succeed and *will overwrite others work.*

In other words, `--force-with-lease` only fails if there are changes *yo

**Comment 5** (score: 3): [removed]

**Comment 6** (score: 11): I prefer merging. However, what I will do is squash commits from a branch before merging it into main to keep things clean and simple.

I generally find that messing with your git history is a bad idea.

Using Squash, I keep my branches small and focused to make tracking new problems easier.

**Comment 7** (score: 7): Skill issue.

I don't understand why people complain that git log --online --graph is messy when you use merge. If you want to show clean history just add --first-parent or --grep="Merged PR to master" or whatever you need to match your default message when you merge a PR.

I never use rebase and have no problems, only benefits. You can always get a clean history as if you used rebase.

Every now and then I need someone to help me finish some big task and we are committing in the same feature br

**Comment 8** (score: 1): I've read the article, but I would like to ask for some help.

I'm writing an app myself. I wanted to test out some new ideas so I made  branch. I then had some further ideas so I made another branch (I'm not sure if it was off the main or off the sub branch or if I can even branch off the sub branch, but the code was all continuous). Now I want to just put it all back on the main branch. 
What command do I type? or should I just clear it out and upload my latest version from scratch?
I just wan

**Comment 9** (score: 1): while i understand rebase and i use it in my work (in the teams where the workflow require it) i still cannot find any actual advantage over merge. maybe you can explain those?

here are 2 very big dissadvantages:  
\* if i want to bring the branch where i started from (lets say main) into my working branch, either i have to sqash the commits, or fix a merge conflict for each commit  
\* if i do squash multiple commits, i loose the context given by the commit text and line number. i mean even in

**Comment 10** (score: 1): I've worked with so many people that have daily 'commits' in their feature branch that are caused by them just doing a git pull every morning and causing a merge bubble (great term btw)

There are many ways to solve this, but I generally prefer rebase like you.

---
### Post 17: I built a web game to learn Git by solving mysteries 🕵️‍♂️
- Score: 232, Comments: 56
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1rqt7rg/i_built_a_web_game_to_learn_git_by_solving/
- Body: I recently built a small web-based game called **GitNoir** where you learn Git commands by solving detective-style mysteries.

🔗 https://www.gitnoir.com

The idea is simple: instead of learning Git through tutorials or documentation, you investigate a mystery and use Git commands to uncover clues. Things like checking commit history, switching branches, and exploring changes become part of solving the case.

The goal is to make learning Git **more interactive and fun**, especially for people who find it difficult to grasp through traditional guides.

The project is **fully open source**, and I’d love to get feedback from the community. If you try it out, feel free to:

- Report bugs or issues
- Suggest improvements
- Share ideas for new mysteries
- Contribute new scenarios that teach Git concepts

Anyone interested in contributing can help expand the game by adding new stories or improving the gameplay and learning experience.

I’d really appreciate any thoughts, feedback, or contributions from people here.

#### Top Comments:

**Comment 1** (score: 67): In this day and age, you're gonna miss SO many users by requiring a login upfront, especially with an email address required.

The usual pipeline today for modern webgames that really want a login is to offer entry without an account, not even a password, then store a token in the browser. Whenever the user returns to the game, the token is their credentials, and the interface nag them that their account is at risk of being lost because it's only stored in the browser's ephemeral data cache, and

**Comment 2** (score: 11): It's fun! But it would be more instructive if it showed real Git output.

**Comment 3** (score: 8): git remote add backup 'https://backup.agency.git' is not accepted.  
However any sane shell would accept it, and create the needed remote

**Comment 4** (score: 3): I remember playing with https://github.com/nivbend/gitstery a long time ago. Is it a similar concept?

**Comment 5** (score: 2): Are you the same person who did SQL noir?

**Comment 6** (score: 2): Two pieces of feedback so far.

1. Generally, the hints are just a restatement of what's being asked. Which is to say if the original question wasn't able to elicit the correct response from the user, the hint doesn't do anything substantive to do so either.
2. Specifically in advanced-case-003, step 4 says "Clone a repository and all its submodules in one command." but doesn't give a URL for the repo. I tried the submodule repo given earlier in the case but that doesn't seem to do it.

**Comment 7** (score: 2): Your project is awesome, but I think there is something missing. Specifically, account linking. By that, I mean if you create an account using Google, you can log in via standard login, not just Google. Similarly, if an account is created via the standard sign-in page, you should be able to link it to Google later.

Sorry if my english is bad or the suggestion is not clear.(I'm using AI to make it better) English is not my native language.

**Comment 8** (score: 2): I got rank #1  
[https://imgur.com/a/1j2q5qe](https://imgur.com/a/1j2q5qe)

**Comment 9** (score: 1): I will also try to add new cases regularly :) 

**Comment 10** (score: 1): The entry field produces a capital first letter which is not right. 

---
### Post 18: What git command do you wish you had discovered sooner?
- Score: 150, Comments: 87
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1qehcqv/what_git_command_do_you_wish_you_had_discovered/
- Body: For me, recently, git pickaxe has been suuuuper useful constantly. 

git log -S"foobar" -- path/to/some/file.c


This will show all the commits whose changes to the given file included the string `foobar`




What command(s) do you wish you had discovered sooner?

#### Top Comments:

**Comment 1** (score: 56): Simple one, but helps me stay organized:
Git commit -amend 

Allows you to merge your local changes to a local commit not yet pushed to remote.

**Comment 2** (score: 30): git bisect to binary search for where something stopped working based on the exit code of a command

**Comment 3** (score: 20): some git rebase flags that solved my biggest pains:
* --reapply-cherry-picks, for when you rebase your branch on fresh trunk after merging the trunk into your branch a few times, this will drop those merge commits and just keep your changes 
* --update-refs, allows rebasing the whole chain of branches in case you stack PRs. doing an interactive rebase with this flag allows you to move your commit to any of your chained branches in one command, doing this manually is a huge pain
* --onto, general

**Comment 4** (score: 46): `git worktree`

**Comment 5** (score: 26): Reflog

**Comment 6** (score: 14): git commit --fixup with git rebase --autosquash

**Comment 7** (score: 6): git add -p

**Comment 8** (score: 5): Worktree 

**Comment 9** (score: 4): Stupid me : git switch ...

**Comment 10** (score: 2): Not so much a command as a customization:  
`git config --global format.pretty "format:%C(yellow)%H%C(reset) - %C(cyan)%an%C(reset), %C(green)%ar%C(reset) : %s"`

---
### Post 19: Git Developers Talk About Potentially Releasing Git 3.0 By The End Of Next Year
- Score: 313, Comments: 81
- Subreddit: r/git
- URL: https://reddit.com/r/git/comments/1o5iu3h/git_developers_talk_about_potentially_releasing/
#### Top Comments:

**Comment 1** (score: 44): Major version # changes makes me nervous. What's 3.0 going to have, and more importantly, what's it going to break?

**Comment 2** (score: 92): "Fourteen months from now, a thing is probably going to happen."

Thanks for the heads-up!  I'll put it on my calendar.

**Comment 3** (score: 12): git ai fix my conflict

**Comment 4** (score: 3): Sha1 is only used in git to produce unique id’s for commits. Is there really any need to switch to sha256?

**Comment 5** (score: 2): I just want an equivalent to mercurial’s `evolve`

**Comment 6** (score: 5): Does the new SHA actually do anything helpful with regards to security? Any hash collisions would be junk bytes, not malware. It would take an act of the gods and the universe itself conspiring against all odds to have a finely crafted malware that just happens to collide with a legitimate git hash.

**Comment 7** (score: 81): `git pull --rebase` now default behavior.


Instant civil war.

**Comment 8** (score: 8): https://github.com/git/git/blob/master/Documentation/BreakingChanges.adoc#git-30

**Comment 9** (score: 46): Part of purpose of the discussion is indeed to give a heads up to the wider community that a breaking version change is coming in the not-distant future.

**Comment 10** (score: 3): 😂

---
