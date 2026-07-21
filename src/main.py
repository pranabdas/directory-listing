#!/usr/local/bin/python3
"""
use os package to iterate through files in a directory
"""
import os
import sys
import json
import base64
import datetime as dt
import subprocess
from settings import SITE_URL, IGNORE_GIT, BASE_URL, SITE_NAME, FOOTER_TEXT

# Get the absolute path of the directory containing this script (the 'src' folder)
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(SCRIPT_DIR, "icons.json"), encoding="utf-8") as json_file:
    data = json.load(json_file)


def main():
    """
    main function
    """
    if len(sys.argv) > 1:
        print("changing directory to " + sys.argv[1])
        # add error handling to chdir
        try:
            os.chdir(sys.argv[1])
        except OSError:
            print("Cannot change the current working Directory")
            sys.exit()
    else:
        print("no directory specified")
        sys.exit()

    for dirname, dirnames, filenames in os.walk("."):
        if IGNORE_GIT:
            if ".git" in dirnames:
                dirnames.remove(".git")

        if "index.html" in filenames:
            print("Skipping  : " + dirname + "/index.html already exists")
        else:
            print("Generating: " + dirname + "/index.html")
            with open(os.path.join(dirname, "index.html"), "w", encoding="utf-8") as f:
                f.write(
                    "\n".join(
                        [
                            get_template_head(dirname, SITE_URL, BASE_URL),
                            (
                                '<tr class="w-2/4 bg-white border-b border-gray-200 hover:bg-gray-50"><th scope="row" class=" py-2 px-2 lg:px-6 font-medium text-gray-900 whitespace-nowrap flex align-middle"><img style="max-width:23px; margin-right:5px" src="'
                                + get_icon_base64("o.folder-home")
                                + '"/>'
                                + '<a class="my-auto text-blue-700 hover:text-pink-500" href="../">••&ensp;<span class="text-gray-400">(&uarr;&nbsp;parent directory)</span></a></th><td>--</td><td>--</td></tr>'
                                if dirname != "."
                                else ""
                            ),
                        ]
                    )
                )
                # sort dirnames alphabetically
                dirnames.sort()
                for subdirname in dirnames:
                    f.write(
                        '<tr class="w-1/4 bg-white border-b border-gray-200 hover:bg-gray-50"><th scope="row" class=" py-2 px-2 lg:px-6 font-medium text-gray-900 whitespace-nowrap flex align-middle"><img style="max-width:23px; margin-right:5px" src="'
                        + get_icon_base64("o.folder")
                        + '"/>'
                        + '<a class="my-auto text-blue-700 hover:text-pink-500" href="'
                        + subdirname
                        + '/">'
                        + subdirname
                        + "</a></th><td>--</td><td>"
                        + get_file_modified_time(dirname + "/" + subdirname)
                        + "</td></tr>\n"
                    )
                # sort filenames alphabetically
                filenames.sort()
                for filename in filenames:
                    path = dirname == "." and filename or dirname + "/" + filename
                    f.write(
                        '<tr class="w-1/4 bg-white border-b border-gray-200 hover:bg-gray-50"><th scope="row" class=" py-2 px-2 lg:px-6 font-medium text-gray-900 whitespace-nowrap flex align-middle"><img style="max-width:23px; margin-right:5px" src="'
                        + get_icon_base64(filename)
                        + '"/>'
                        + '<a class="my-auto text-blue-700 hover:text-pink-500" href="'
                        + filename
                        + '">'
                        + filename
                        + "</a></th><td>"
                        + get_file_size(path)
                        + "</td><td>"
                        + get_file_modified_time(path)
                        + "</td></tr>\n"
                    )

                f.write("\n".join([get_template_foot()]))


def get_file_size(filepath):
    """
    get file size
    """
    size = os.path.getsize(filepath)
    if size < 1024:
        return str(size) + " B"
    elif size < 1024 * 1024:
        return str(round((size / 1024), 2)) + " KB"
    elif size < 1024 * 1024 * 1024:
        return str(round((size / 1024 / 1024), 2)) + " MB"
    else:
        return str(round((size / 1024 / 1024 / 1024), 2)) + " GB"


def get_file_modified_time(filepath):
    """
    get file modified time
    """
    git_cmd = 'git log -1 --pretty="format:%cd" --date="format:%d-%b-%Y %H:%M"' + " " + filepath
    return subprocess.check_output(git_cmd, shell=True).decode("utf-8") or dt.datetime.fromtimestamp(
        os.path.getmtime(filepath)
    ).strftime("%d-%b-%Y %H:%M") or "??"


def get_template_head(dirname, SITE_URL, BASE_URL):
    """
    get template head
    """
    with open(os.path.join(SCRIPT_DIR, "template", "head.html"), encoding="utf-8") as file:
        head = file.read()

    if BASE_URL == '.':
        ABS_URL = ''
    else:
        ABS_URL = "/" + BASE_URL

    if SITE_NAME != "" and BASE_URL == ".":
        foldername = SITE_NAME + dirname[1:]
    else:
        foldername = BASE_URL + dirname[1:]

    return head.format(
        foldername=foldername,
        breadcrumb=generate_breadcrumb(foldername, SITE_NAME),
        SITE_URL=SITE_URL,
        ABS_URL=ABS_URL
    )


def get_template_foot():
    """
    get template foot
    """
    with open(os.path.join(SCRIPT_DIR, "template", "foot.html"), encoding="utf-8") as file:
        foot = file.read()
    footer_text = FOOTER_TEXT.format(year=str(dt.datetime.now().year))
    return foot.format(footer_text=footer_text)


def get_icon_base64(filename):
    """
    get icon base64
    """
    icon_path = os.path.join(SCRIPT_DIR, "png", get_icon_from_filename(filename))
    with open(icon_path, "rb") as file:
        return "data:image/png;base64, " + base64.b64encode(file.read()).decode("ascii")


def get_icon_from_filename(filename):
    """
    get icon from filename
    """
    extension = "." + filename.split(".")[-1]
    # extension = "." + extension
    # print(extension)
    for i in data:
        if extension in i["extension"]:
            # print(i["icon"])
            return i["icon"] + ".png"
    # print("no icon found")
    return "unknown.png"


def generate_breadcrumb(input_dir, site_name=""):
    dir_items = str(input_dir).split("/")

    # remove empty items
    dir_items_cleaned = list(filter(None, dir_items))

    url = ""
    result = ""
    for index, item in enumerate(dir_items_cleaned):
        if site_name != "" and index == 0:
            url += "/"
        elif site_name != "" and index == 1:
            url += item
        else:
            url += "/" + item

        if index < len(dir_items_cleaned) - 1:
            result += f'<a class="text-sky-500 hover:text-pink-500" href="{url}">{item}</a>' + "/"
        else:
            result += '<span class="text-slate-500">' + item + "</span>"

    return result


if __name__ == "__main__":
    main()
