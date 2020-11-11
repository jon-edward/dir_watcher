# dir_watcher
dir_watcher is a simple utility for watching a specified directory for changes to any of its files (including nested directories or just the top level), printing a notification of a change to a file or directory, and optionally running a main python script upon encountered change.

# How to use
dir_watcher can be used as a module or be run directly as a python script. 

# Using dir_watcher as a module
**Simplest case:**
```
from dir_watcher.watcher import watch
watch("path/to/directory")
```
_Where the desired outcome is to print changes made to directory path/to/directory._

**Slightly more complex case:**
```
from dir_watcher.watcher import watch
watch("path/to/directory",
      run_file="path/to/file.py",
      inc_ext=[".py", ".txt"],
      nested=True,
      dur=2.0,
      sys_argv="-a 1",
      pref="python3")
```
_Where the desired outcome is to only check .py or .txt files in the directory path/to/directory or nested directories inside path/to/directory every 2.0 seconds. When changes are encountered, it runs the following command:_
```
python3 path/to/file.py -a 1
```

# Using dir_watcher as a python script
Using the -h help flag prints:
```
usage: watcher.py [-h] [--run_file RUN_F] [--watch_directory W_DIR]
                  [--nested_check]
                  [--included_extensions INC_EXT [INC_EXT ...]]
                  [--excluded_extensions EXC_EXT [EXC_EXT ...]]
                  [--duration DUR] [--suppress_change_notification]
                  [--sys_argv SYS_ARGV] [--python_prefix PYTHON_PREFIX]

Watch a directory for changes and optionally run a specified file when a
change is detected.

optional arguments:
  -h, --help            show this help message and exit
  --run_file RUN_F, -rf RUN_F
                        Defines a .py file to run when a change is detected in
                        watched directory. Defaults to not running any files
                        upon change detected.
  --watch_directory W_DIR, -wd W_DIR
                        Specifies which directory to watch for changes.
                        Defaults to the current working directory.
  --nested_check, -nc   The existence of this flag checks directories within
                        watched directory. Defaults to only checking files at
                        the top level of the watched directory.
  --included_extensions INC_EXT [INC_EXT ...], -ie INC_EXT [INC_EXT ...]
                        Specifies which extensions should exclusively be
                        checked in the directory. Do not use with excluded
                        extensions flag.
  --excluded_extensions EXC_EXT [EXC_EXT ...], -ee EXC_EXT [EXC_EXT ...]
                        Specifies which extensions should exclusively be not
                        checked in the directory. Do not use with included
                        extensions flag.
  --duration DUR, -d DUR
                        Specifies the time between checks of the files within
                        watched directory in seconds. Defaults to 0.5
  --suppress_change_notification, -supp
                        Suppresses notification of changes to watched
                        directory.
  --sys_argv SYS_ARGV, -sys SYS_ARGV
                        Appends specified system arguments to run_file call.
  --python_prefix PYTHON_PREFIX, -py PYTHON_PREFIX
                        Sets the prefix to use for script invocation. Defaults
                        to "py"
```
**Examples of usage:**
```
py watcher.py --included .py .txt --run path/to/file.py
```
_Where the desired outcome is to run path/to/file.py when a change is observed in any .py or .txt files in the current working directory._
```
py watcher.py --watch_directory path/to/directory --excluded "" .zip --nested_check
```
_Where the desired outcome is to print when changes to path/to/directory or directories within path/to/directory are made, excluding the directories themselves or .zip files._
