
Branching and Merging
---------------------

The git merge command lets you take the independent lines of development created by git branch and integrate them into a single branch.
Note that all of the commands presented below merge into the current branch. The current branch will be updated to reflect the merge, but the target branch will be completely unaffected. Again, this means that git merge is often used in conjunction with `git checkout` for selecting the current branch and `git branch -d` for deleting the obsolete target branch.

`git merge` will combine multiple sequences of commits into one unified history. `git merge` is usually used to combine two branches, where it takes two commit pointers and will find a common base commit between them and create a new "merge commit" that combines the changes of each queued merge commit sequence.

![](../images/merge-commit.png)

Merge commits are unique against other commits in the fact that they have two parent commits. When creating a merge commit Git will attempt to auto magically merge the separate histories for you. If Git encounters a piece of data that is changed in both histories it will be unable to automatically combine them. This scenario is a version control conflict and Git will need user intervention to continue.

Suppose you are doing some work on a feature development branch and do some commits. Doing so moves the `iss53` branch forward, because you have it checked out (that is, your `HEAD is pointing to it):

![](../images/basic-branching-3.png)

Then  receive a call that another issue is critical and you need a hotfix. You’ll do the following:

1) Switch to your production branch.

2) Create a branch to add the hotfix.

3) After it’s tested, merge the hotfix branch, and push to production.

4) Switch back to your original story and continue working.

    $ git checkout master
    Switched to branch 'master'

At this point, your project working directory is exactly the way it was before you started working on issue #53, and you can concentrate on your hotfix. This is an important point to remember: when you switch branches, Git resets your working directory to look like it did the last time you committed on that branch.
Next, you have a hotfix to make:

    $ git checkout -b hotfix
    Switched to a new branch 'hotfix'
    $ vim index.html
    $ git commit -a -m 'fixed the broken email address'
    [hotfix 1fb7853] fixed the broken email address
     1 file changed, 2 insertions(+)

![](../images/basic-branching-4.png)

You can run your tests, make sure the hotfix is what you want, and finally merge the hotfix branch back into your master branch to deploy to production. You do this with the `git merge` command:

    $ git checkout master
    $ git merge hotfix
    Updating f42c576..3a0874c
    Fast-forward
     index.html | 2 ++
     1 file changed, 2 insertions(+)

You’ll notice the phrase “fast-forward” in that merge. Because the commit C4 pointed to by the branch hotfix you merged in was directly ahead of the commit C2 you’re on

![](../images/basic-branching-5.png)

You can now delete the hotfix branch and switch back to your work-in-progress branch on issue #53 and continue working on it.

    $ git branch -d hotfix
    Deleted branch hotfix (3a0874c).
    $ git checkout iss53
    Switched to branch "iss53"
    $ vim index.html
    $ git commit -a -m 'finished the new footer [issue 53]'
    [iss53 ad82d7a] finished the new footer [issue 53]
    1 file changed, 1 insertion(+)

![](../images/basic-branching-6.png)

It’s worth noting here that the work you did in your hotfix branch is not contained in the files in your iss53 branch. If you need to pull it in, you can merge your master branch into your iss53 branch by running git merge master, or you can wait to integrate those changes

Suppose you’ve decided that your issue #53 work is complete and ready to be merged into your master branch.

    $ git checkout master
    Switched to branch 'master'
    $ git merge iss53
    Merge made by the 'recursive' strategy.
    index.html |    1 +
    1 file changed, 1 insertion(+)

This is a bit different than the hotfix merge you did earlier. In this case, your development history has diverged from some older point. Because the commit on the branch you’re on isn’t a direct ancestor of the branch you’re merging in, Git has to do some work. In this case, Git does a simple three-way merge, using the two snapshots pointed to by the branch tips and the common ancestor of the two:

![](../images/basic-merging-1.png)

Instead of just moving the branch pointer forward, Git creates a new snapshot that results from this three-way merge and automatically creates a new commit that points to it. This is referred to as a merge commit, and is special in that it has more than one parent.

![](../images/basic-merging-2.png)

**Basic Merge Conflicts**

Occasionally, this process doesn’t go smoothly. If you changed the same part of the same file differently in the two branches you’re merging together, Git won’t be able to merge them cleanly. If your fix for issue #53 modified the same part of a file as the hotfix branch, you’ll get a merge conflict that looks something like this:

    $ git merge iss53
    Auto-merging index.html
    CONFLICT (content): Merge conflict in index.html
    Automatic merge failed; fix conflicts and then commit the result.

Git hasn’t automatically created a new merge commit. It has paused the process while you resolve the conflict. If you want to see which files are unmerged at any point after a merge conflict, you can run git status:

    $ git status
    On branch master
    You have unmerged paths.
      (fix conflicts and run "git commit")

    Unmerged paths:
      (use "git add <file>..." to mark resolution)

        both modified:      index.html

    no changes added to commit (use "git add" and/or "git commit -a")

If you want to use a graphical tool to resolve these issues, you can run `git mergetool`, which fires up an appropriate visual merge tool and walks you through the conflicts.

Merging vs Rebasing
-------------------
`git fetch` updates your remote-tracking branches under refs/remotes/<remote>/.

This operation never changes any of your own local branches under refs/heads, and is safe to do without changing your working copy.

`git pull` will bring a local branch up-to-date with its remote version. In simple terms, `git pull` does a `git fetch` followed by a `git merge`.

Suppose originally there were 3 commits, `A`,`B`,`C` and then developer Dan created commit `D`, and developer Ed created commit `E`:

![](../images/commit-d-e.png)

There are two ways to resolve this conflict: merge and rebase.

**Merge:**

![](../images/merge-commit2.png)

Both commits `D` and `E` are still here, but we create merge commit `M` that inherits changes from both `D` and `E`. However, this creates diamond shape, which many people find very confusing.

**Rebase:**

![](../images/rebase-commit.png)

We create commit `R`, which actual file content is identical to that of merge commit `M` above. But, we get rid of commit `E`, like it never existed (denoted by dots - vanishing line). Because of this obliteration, `E` should now be local to developer Ed and have never been pushed to any other repository. Advantage of rebase is that diamond shape is avoided, and history stays nice straight line - most developers love that!

The git rebase command can actually make life much easier for a development team when used with care.

Both `git rebase` and `git merge` are designed to integrate changes from one branch into another branch—they just do it in very different ways

Consider what happens when you start working on a new feature in a dedicated branch, then another team member updates the master branch with new commits. This results in a forked history, which should be familiar to anyone who has used Git as a collaboration tool.

![](../images/forked-history.png)

Now, let’s say that the new commits in master are relevant to the feature that you’re working on. To incorporate the new commits into your feature branch, you have two options: merging or rebasing.

**The Merge Option**

The easiest option is to merge the master branch into the feature branch using something like the following:

    git checkout feature
    git merge master

Or, you can condense this to a one-liner:

    git merge master feature

This creates a new “merge commit” in the feature branch that ties together the histories of both branches.

![](../images/merge-commit3.png)

Merging is nice because it’s a non-destructive operation. The existing branches are not changed in any way. This avoids all of the potential pitfalls of rebasing (discussed below).
On the other hand, this also means that the feature branch will have an extraneous merge commit every time you need to incorporate upstream changes. If master is very active, this can pollute your feature branch’s history quite a bit. While it’s possible to mitigate this issue with advanced git log options, it can make it hard for other developers to understand the history of the project.

**The Rebase Option**

As an alternative to merging, you can rebase the feature branch onto master branch using the following commands:

    git checkout feature
    git rebase master

This moves the entire feature branch to begin on the tip of the master branch, effectively incorporating all of the new commits in master. But, instead of using a merge commit, rebasing re-writes the project history by creating brand new commits for each commit in the original branch.

![](../images/rebase-commit2.png)

The major benefit of rebasing is that you get a much cleaner project history. First, it eliminates the unnecessary merge commits required by git merge. Second, as you can see in the above diagram, rebasing also results in a perfectly linear project history—you can follow the tip of feature all the way to the beginning of the project without any forks. This makes it easier to navigate your project with commands like git log, git bisect, and gitk.

But, there are two trade-offs for this pristine commit history: safety and traceability. If you don’t follow the Golden Rule of Rebasing, re-writing project history can be potentially catastrophic for your collaboration workflow.

**Perils of Rebasing**

Ahh, but the bliss of rebasing isn’t without its drawbacks, which can be summed up in a single line:

Do not rebase commits that exist outside your repository.

The golden rule of git rebase is to never use it on public branches.
For example, think about what would happen if you rebased master onto your feature branch:

![](../images/rebasing-master.png)

The rebase moves all of the commits in master onto the tip of feature. The problem is that this only happened in your repository. All of the other developers are still working with the original master. Since rebasing results in brand new commits, Git will think that your master branch’s history has diverged from everybody else’s.

