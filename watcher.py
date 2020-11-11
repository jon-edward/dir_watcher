import watcher_tools as w
import time
import os
from typing import List, Tuple
from argparse import ArgumentParser
from datetime import datetime


def _handle_arguments() -> Tuple[str, str, bool, List[str], List[str], float, bool, str, str]:
    a = ArgumentParser(description="Watch a directory for changes and optionally run a specified file " +
                                   "when a change is detected.", allow_abbrev=True)

    a.add_argument("--run_file", "-rf", type=str, dest="run_f",
                   default="",
                   help="Defines a .py file to run when a change is detected in watched directory. Defaults to not " +
                        "running any files upon change detected.")

    a.add_argument("--watch_directory", "-wd", type=str, dest="w_dir",
                   default=os.getcwd(),
                   help="Specifies which directory to watch for changes. Defaults to the current working directory.")

    a.add_argument("--nested_check", "-nc", action="store_true", dest="nest",
                   help="The existence of this flag checks directories within watched directory. Defaults to only " +
                        "checking files at the top level of the watched directory.")

    a.add_argument("--included_extensions", "-ie", nargs="+", action="append", dest="inc_ext", default=[],
                   help="Specifies which extensions should exclusively be checked in the directory. Do not use with " +
                        "excluded extensions flag.")

    a.add_argument("--excluded_extensions", "-ee", nargs="+", action="append", dest="exc_ext", default=[],
                   help="Specifies which extensions should exclusively be not checked in the directory. Do not use " +
                        "with included extensions flag.")

    a.add_argument("--duration", "-d", type=float, dest="dur",
                   default=0.5,
                   help="Specifies the time between checks of the files within watched directory in seconds. " +
                        "Defaults to 0.5")

    a.add_argument("--suppress_change_notification", "-supp", dest="info", action="store_false",
                   help="Suppresses notification of changes to watched directory.")

    a.add_argument("--sys_argv", "-sys", type=str, default="",
                   help="Appends specified system arguments to run_file call.")

    a.add_argument("--python_prefix", "-py", type=str, default="py",
                   help="Sets the prefix to use for script invocation. Defaults to \"py\"")

    args = a.parse_args()

    run_file = args.run_f

    if run_file and not os.path.isabs(run_file):
        run_file = os.path.join(os.getcwd(), run_file)

    directory_to_watch = args.w_dir

    if not os.path.isabs(directory_to_watch):
        directory_to_watch = os.path.join(os.getcwd(), directory_to_watch)

    nested_check = args.nest
    included_extensions = []
    [included_extensions.extend(a) for a in args.inc_ext]
    excluded_extensions = []
    [excluded_extensions.extend(a) for a in args.exc_ext]
    duration = args.dur
    print_info = args.info
    sys_args_to_append = args.sys_argv
    prefix = args.python_prefix

    return (directory_to_watch,
            run_file,
            nested_check,
            included_extensions,
            excluded_extensions,
            duration,
            print_info,
            sys_args_to_append,
            prefix)


def _get_current_state(d, i, e, n):
    if n:
        return w.list_nested_directories(path_to_directory=d, accepted_extensions=i, excluded_extensions=e)
    else:
        return w.list_top_level_of_directory(path_to_directory=d, accepted_extensions=i, excluded_extensions=e)


def watch(dir_to_watch: str,
          run_file: str = "",
          nested: bool = False,
          inc_ext: List[str] = None,
          exc_ext: List[str] = None,
          dur: float = 0.5,
          print_info: bool = True,
          sys_argv: List[str] = None,
          pref: str = "py") -> None:
    """
    :param dir_to_watch: Specifies the directory to watch.
    :param run_file: Specifies the file to run when a change is encountered. Optional.
    :param nested: Specifies whether or not to check directories within directories for changes. Defaults to False.
    :param inc_ext: Filters checked items by whitelisting extensions. Optional. Directories are denoted by "".
    :param exc_ext: Filters checked items by blacklisting extensions. Optional. Directories are denoted by "".
    :param dur: Specifies how long to wait before checking directory again. Defaults to 0.5
    :param print_info: Specifies whether or not to output directory change information. Defaults to True.
    :param sys_argv: Specifies system arguments to append to run_file call. Optional.
    :param pref: Specifies prefix to use for python script invocation. Defaults to "py".
    :return: None
    """
    last_state = _get_current_state(dir_to_watch, inc_ext, exc_ext, nested)
    last_times = [(f, os.stat(f).st_mtime) for f in last_state]
    last_state.sort()
    print("-" * 60 + str(datetime.now()))
    while True:
        time.sleep(dur)
        curr_state = _get_current_state(dir_to_watch, inc_ext, exc_ext, nested)
        curr_times = [(f, os.stat(f).st_mtime) for f in curr_state]
        comp_last = set(last_state)
        comp_curr = set(curr_state)
        deleted_items = comp_last - comp_curr
        created_items = comp_curr - comp_last

        modified_items = []
        for state in curr_times:
            past_counterpart = next((i for i in last_times if state[0] == i[0]), None)
            if past_counterpart and past_counterpart[1] != state[1]:
                modified_items.append(state)

        change_encountered = deleted_items or created_items or modified_items

        if print_info:
            if deleted_items:
                print(f"Lost file{'' if len(deleted_items) < 2 else 's'}: ")
                for i in deleted_items:
                    print(f" - {os.path.join(dir_to_watch, i)}")
            if created_items:
                print(f"New file{'' if len(created_items) < 2 else 's'}: ")
                for i in created_items:
                    print(f" - {os.path.join(dir_to_watch, i)}")
            if modified_items:
                print(f"Modified file{'' if len(modified_items) < 2 else 's'}: ")
                for i in modified_items:
                    print(f" - {os.path.join(dir_to_watch, i[0])}")

        if change_encountered:
            print("-" * 60 + str(datetime.now()))
            if run_file:
                run_statement = f"{pref} {run_file} {sys_argv}"
                print(f" * {run_statement}")
                os.system(run_statement)
                print("-" * 60 + str(datetime.now()))

        last_state = _get_current_state(dir_to_watch, inc_ext, exc_ext, nested)
        last_times = [(f, os.stat(f).st_mtime) for f in last_state]


if __name__ == '__main__':
    watch(*_handle_arguments())
