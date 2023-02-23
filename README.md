#!/usr/bin/python
# Pomodoro

Pomodoro is a simple command-line application that helps you stay focused and productive by using
the Pomodoro technique. With Pomodoro, you can easily set work and break times, and the application
will notify you when it's time to take a break.
Installation

To install Pomodoro on a Mac using Homebrew, run the following command in your terminal:

```bash
brew install pomodoro-timer
```

For Linux users, you can install the application by cloning the repository and running the following
commands in your terminal:

```bash
git clone https://github.com/username/pomodoro.git
cd pomodoro
pip install -r requirements.txt
```

Usage

To use Pomodoro, open your terminal and type the following command:

```bash
pomodoro
```

This will start the Pomodoro timer with default settings of 25 minutes of work time and 5 minutes of
break time. If you want to set custom times, you can use the --work and --rest options, like this:

```bash
pomodoro --work 30 --rest 10
```

This will set the work time to 30 minutes and the break time to 10 minutes.

You can also enable desktop notifications by using the --notify option:

```bash
pomodoro --notify
```

This will enable desktop notifications for the Pomodoro timer. Note that this option is only
available on Mac and Linux systems that support notifications.

Once you start the timer, Pomodoro will display a progress bar in the terminal, and notify you when
it's time to take a break. When the break is over, Pomodoro will automatically start another work
session.