
**Branches in a Nutshell**

When you make a commit, Git stores a commit object that contains a pointer to the snapshot of the content you staged. This object also contains metadata and pointers to the commit or commits that directly came before this commit

Aassume that you have a directory containing three files, and you stage them all and commit.
Your Git repository now contains five objects: one blob for the contents of each of your three files, one tree that lists the contents of the directory and specifies which file names are stored as which blobs, and one commit with the pointer to that root tree and all the commit metadata:

![](./images/commit-and-tree.png)

If you make some changes and commit again, the next commit stores a pointer to the commit that came immediately before it:

![](./images/commits-and-parents.png)

A branch in Git is simply a lightweight movable pointer to one of these commits. The default branch name in Git is master. As you start making commits, you’re given a master branch that points to the last commit you made. Every time you commit, it moves forward automatically.

If you create a new branch it creates a new pointer for you to move around. Let’s say you create a new branch called testing with the `git branch` command:

    $ git branch testing

This creates a new pointer to the same commit you’re currently on.

How does Git know what branch you’re currently on? It keeps a special pointer called `HEAD`.
Switch to the new branch:

    $ git checkout testing

This moves `HEAD` to point to the testing branch:

![](./images/head-to-testing.png)

You can easily see this by running a simple `git log` command that shows you where the branch pointers are pointing. This option is called `--decorate`.

    $ git log --oneline --decorate

Let’s do another commit:

    $ vim test.rb
    $ git commit -a -m 'made a change'

The HEAD branch moves forward when a commit is made

This is interesting, because now your testing branch has moved forward, but your master branch still points to the commit you were on when switched branches

![](./images/advance-testing.png)

Switching back to the master branches moves the HEAD pointer back to point to the master branch, and it reverted the files in your working directory back to the snapshot that master points to. This also means the changes you make from this point forward will diverge from an older version of the project. It essentially rewinds the work you’ve done in your testing branch so you can go in a different direction.

On the master branch, let’s make a few changes and commit again:

    $ vim test.rb
    $ git commit -a -m 'made other changes'

Now your project has diverged. Both of those changes are isolated in separate branches: you can switch back and forth between the branches and merge them together when you’re ready

![](./images/advance-master.png)

**Basic Branching and Merging**

Suppose you are doing some work on a feature development branch, then  receive a call that another issue is critical and you need a hotfix. You’ll do the following:

1) Switch to your production branch.

2) Create a branch to add the hotfix.

3) After it’s tested, merge the hotfix branch, and push to production.

4) Switch back to your original story and continue working.


`git reset`, `git checkout`, `git revert`
-----------------------------------------

It helps to think about each command in terms of their effect on the three state management mechanisms of a Git repository: the working directory,
the staged snapshot, and the commit history.


