========
Commands
========


cache:clear
-----------
Clear the cache.


gen:secretkey
-------------
Generate a new Secretkey for Django.


patch
-----
Command "patch" will help you to increase the version number of your project in a easy way.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| -M, --major               | Set major number                              |
+---------------------------+-----------------------------------------------+
| -m, --minor               | Set minor number                              |
+---------------------------+-----------------------------------------------+
| -p, --patch               | Set patch number                              |
+---------------------------+-----------------------------------------------+
| -d, --dev                 | Set dev release (e.g. 1.2.1dev1)              |
+---------------------------+-----------------------------------------------+
| -a, --alpha               | Set alpha release (e.g. 1.2.1a1)              |
+---------------------------+-----------------------------------------------+
| -b, --beta                | Set beta release (e.g. 1.2.1b1)               |
+---------------------------+-----------------------------------------------+
| -r, --release-candidate   | Set release candidate release (e.g. 1.2.1rc1) |
+---------------------------+-----------------------------------------------+
| -f, --force               | Force patching                                |
+---------------------------+-----------------------------------------------+


git:add
-------
Add files to Git repository. Supports all standard "git add" options.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| -n, --dry-run             | Dry run                                       |
+---------------------------+-----------------------------------------------+
| --verbose                 | Be verbose.                                   |
+---------------------------+-----------------------------------------------+
| -i, --interactive         | Interactive picking.                          |
+---------------------------+-----------------------------------------------+
| -p, --patch               | Select hunks interactively.                   |
+---------------------------+-----------------------------------------------+
| -e, --edit                | Edit current diff and apply.                  |
+---------------------------+-----------------------------------------------+
| -f, --force               | Allow adding otherwise ignored files.         |
+---------------------------+-----------------------------------------------+
| -u, --update              | Update tracked files.                         |
+---------------------------+-----------------------------------------------+
| -N, --intent-to-add       | Record only the fact that the path will be    |
|                           | added later.                                  |
+---------------------------+-----------------------------------------------+
| -A, --all                 | Add changes from all tracked and untracked    |
|                           | files.                                        |
+---------------------------+-----------------------------------------------+
| --ignore-removal          | Ignore paths removed in the working tree      |
|                           | (same as --no-all).                           |
+---------------------------+-----------------------------------------------+
| --refresh                 | Do not add, only refresh the index.           |
+---------------------------+-----------------------------------------------+
| --ignore-errors           | Just skip files which cannot be added because |
|                           | of errors.                                    |
+---------------------------+-----------------------------------------------+
| --ignore-missing          | Check if - even missing - files are ignored   |
|                           | in dry run.                                   |
+---------------------------+-----------------------------------------------+


git:tag
-------
Tag your project.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| --default                 | (is default)                                  |
+---------------------------+-----------------------------------------------+
| --staging                 | Create a staging tag (e.g. staging-v1.2.3).   |
+---------------------------+-----------------------------------------------+
| --activate                | Create a activate tag (e.g. activate-v1.2.3). |
+---------------------------+-----------------------------------------------+
| --push                    | Push tags.                                    |
+---------------------------+-----------------------------------------------+


git:tag:push
------------
Push your tagged project.


git:tag:delete
--------------
Remove the latest or given tag from local repository.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| <tag>                     | Remove the latest or given tag (optional).    |
+---------------------------+-----------------------------------------------+


pypi:export
-----------
Export your project.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| --no-wheel                | Export project without wheel.                 |
|                           | (not recommended)                             |
+---------------------------+-----------------------------------------------+
| -u, --upload              | Upload Project.                               |
+---------------------------+-----------------------------------------------+


pypi:upload
-----------
Upload project to pypi via twine.

+---------------------------+-----------------------------------------------+
| Option                    | Description                                   |
+===========================+===============================================+
| --default                 | Upload project to PyPI via twine.             |
+---------------------------+-----------------------------------------------+
