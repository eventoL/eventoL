## Contributing

First, thank you for considering contributing to EventtoL. For people
like you, is that EventoL is a great tool.

### 1. Where do I go from here?

If you've noticed an error or have a question, first look in
[support group](https://t.me/eventol_soporte), [Stack Overflow](https://stackoverflow.com/) or [issues](https://github.com/eventoL/eventoL/ issues) to see if someone else in the community has already created an issue.
If not, go ahead and [create an issue](https://github.com/eventoL/eventoL/issues/new/choose)!

### 2. Fork and create a branch

If this is something you think you can fix, then create a [fork Eventol](https://github.com/eventoL/eventoL) and
create a branch with a descriptive name.

A good branch name would be (the number of the issue you are working on and some text):

```sh
# Example issue: 325 Add japanese trasnlations
git checkout -b 325-add-japanese-translations
```

### 3. Set up the development and testing environment

Make sure you're using a recent python (3.5 or greater) and have npm installed.
Also exists another way to have the environment only with docker for that look in the [installation documentation](http://eventol.github.io/eventoL/#/en/installation).

### 4. Did you find an error?

* **Make sure the error has not been reported** in the [issues](https://github.com/eventoL/eventoL/issues).

* If you can't find an open issue that addresses the problem,
  [opened a new one](https://github.com/eventoL/eventoL/issues/new/choose).
  In order to have a correctly informed issue, follow the instructions indicated in the selected template.

### 5. Implement your fix or functionality

At this point, you are ready to make your changes! Feel free to ask for help;
they are all beginners at the beginning.

### 6. View your changes in an application

It is important that before sending your code you try it locally.
To achieve that you can follow the steps of [installation guide](http://eventol.github.io/eventoL/#/en/installation)

### 7. Get the code style

Your patch must follow the same conventions and pass the same code quality
than the rest of the project. *Pylint* and *Eslint* will give you
feedback on this.
You can verify and correct the comments by running it
locally using the [test script](http://eventol.github.io/eventoL/#/en/test_script).

### 8. Make a Pull request

At this point, you must go back to the main branch and make sure it is compatible with the main branch at this time:

```sh
git remote add upstream git@github.com:eventoL/eventoL.git
git checkout master
git pull upstream master
```

Then update your branch from your local master copy, and push!

```sh
git checkout 325-add-japanese-translations
git rebase master
git push - origin set-upstream 325-add-japanese-translations
```

Finally, go to GitHub and [create a pull request](https://github.com/eventoL/eventoL/compare):

Travis CI will execute our test suite.
Your PR will not be merged until all the tests pass.
Gitlab will also run the linters (both python and reactive) and the python and react tests.

### 8. Make your pull request updated

Whenever the master has a change, it is recommended that you update the pull request.

```sh
git checkout 325-add-japanese-translations
git pull --rebase upstream master
git push --force-with-lease 325-add-japanese-translations
```

### 10. Merging a PR (maintainers only)

An RP can only be merged into a master by an administrator if:

* CI is happening.
* Each linter is passing.
* No changes requested.
* It is updated with the current master.

Any administrator can merge a PR if all these conditions are met.

### 11. Shipping a release (maintainers only)

Administrators must do the following to launch a version:

* Make sure that all pull requests are in and that the change log is updated
* Update the changelog file with the new version number
* Create a tag for that version (this tag has to be signed)

### 12. Links

* **Official documentation**: http://eventol.github.io/eventoL/#/
* **Support telegram group**: https://t.me/eventol_soporte
* **Official Repository**: https://github.com/eventoL/eventoL
* **Issues**: https://github.com/eventoL/eventoL/issues
* **Pull requests**: https://github.com/eventoL/eventoL/pulls
* **Gitlab Repository (mirror for pipelines)**: https://gitlab.com/eventol/eventoL
* **Gitlab pipelines**: https://gitlab.com/eventol/eventoL/pipelines
* **Coveralls Report**: https://coveralls.io/github/eventoL/eventoL?branch=master
* **Requires.io**: https://requires.io/github/eventoL/eventoL/requirements/?branch=master
* **Weblate translations**: https://hosted.weblate.org/projects/eventol/
* **Travis builds**: https://travis-ci.org/eventoL/eventoL