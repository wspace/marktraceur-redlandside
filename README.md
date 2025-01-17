# RedlandsIDE

RedlandsIDE, or rIDE, is a very simple IDE meant for students who have little
or no interest in extra compiler options, extra features, or really anything.
It's also ideal for people who simply want to jump into a project quickly
without doing anything complicated. Of course, this means that the project
must be properly configured for simple compilation, but we leave that up to the
project authors!

In any case, let's get right into how to use RedlandsIDE.

## Dependencies

Dependencies are a tricky thing in Python, since there are so many ways to get
what you need. Here are a few common ways:

### Debian package manager (apt-get)

This way ensures that you get a good, stable version of the packages, and also
makes them easy to manage. The command is this (run it as root):

```sh
$ apt-get install python-qt4
```

### Fedora package manager (yum)

Similar to the Debian method above, but for Fedora!

```sh
$ yum install pyqt-devel
```

### Python package manager (pip or easy_install)

This next way has its advantages, too! For example, rather than installing the
dependencies as root, if you have a python virtualenv set up, you can install
it locally! In any case, you can run this command to achieve your goals:

```sh
$ pip install python-qt
```

### Other package managers?

If you have a suggestion for a way we can install pyqt4 on other distributions,
please submit a pull request or issue to this project!

## Installation

Installation is as simple as downloading the files! Since there's not yet any
package management work done, we don't have to do anything else.

## Language Support

This project currently supports these languages:

* Python
* C++
* Prolog
* Lisp
* LOLCODE
* Whitespace

## Running

In order to run the project, you'll need to use the `cd` command to get into
the project's directory. For me, that looks like this:

```sh
$ cd ~/projects/redlandside
```

But you may have a different directory structure. Now that you're there, you
can run the application with

```sh
$ ./main.py
```

Thanks for using rIDE, and I hope it works really well for you!
