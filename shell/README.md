# Unix Shell

A simple shell that:

* prints a command prompt `$` (or environment variable PS1, if set) and waits for a command
* ignores empty commands
* terminates with `exit`
* finds arguments in PATH if absolute path is not specified
* handles one pipe
* handles one IO redirect
* prints `command not found` if a command is not found
