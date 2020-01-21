import os
import re
import fileinput

from django_sonic_screwdriver.utils import shell
from django_sonic_screwdriver.settings import APISettings


RELEASE_TAGS = {
    # pre-release
    "ALPHA": "a",
    "BETA": "b",
    "RC": "rc",
    # dev-release
    "DEV": "dev",
    # post-release
}

RELEASE_SEPARATORS = {"DOT": ".", "MINUS": "-", "UNDERSCORE": "_"}


class Version:
    @staticmethod
    def get_version():
        """
        Return version from setup.py
        """
        with open(os.path.join(os.path.abspath(APISettings.VERSION_FILE))) as version_desc:
            version_file = version_desc.read()

            try:
                return re.search(r"version=['\"]([^'\"]+)['\"]", version_file).group(1)
            except FileNotFoundError:  # pragma: no cover
                shell.fail("File not found!")
                raise FileNotFoundError
            except ValueError:  # pragma: no cover
                shell.fail("Version not found in file " + version_file + "!")
                raise ValueError

    @staticmethod
    def set_version(old_version, new_version):
        """
        Write new version into VERSION_FILE
        """
        try:
            if APISettings.DEBUG:
                shell.debug("* " + old_version + " --> " + new_version)
                return True

            for line in fileinput.input(
                os.path.abspath(APISettings.VERSION_FILE), inplace=True
            ):
                print(line.replace(old_version, new_version), end="")
            shell.success("* " + old_version + " --> " + new_version)
        except FileNotFoundError:
            shell.warn("File not found!")

    @staticmethod
    def get_patch_version(version):
        try:
            patch = version.split(".", 2)[2]
        except IndexError:
            shell.fail("Take note your version looks like this: 0.1.2!")
            raise IndexError
        return patch

    @staticmethod
    def get_current_RELEASE_SEPARATOR(patch):
        for key in RELEASE_SEPARATORS:
            if RELEASE_SEPARATORS[key] in patch:
                return RELEASE_SEPARATORS[key]
        return False

    @staticmethod
    def get_current_pre_release_tag(patch):
        for key in RELEASE_TAGS:
            if RELEASE_TAGS[key] in patch:
                return RELEASE_TAGS[key]
        return False

    def set_major(self):
        """
        Increment the major number of project
        """
        old_version = self.get_version()
        new_version = str(int(old_version.split(".", 5)[0]) + 1) + ".0.0"
        self.set_version(old_version, new_version)

    def set_minor(self):
        """
        Increment the minor number of project
        """
        old_version = self.get_version()
        new_version = (
            str(int(old_version.split(".", 5)[0]))
            + "."
            + str(int(old_version.split(".", 5)[1]) + 1)
            + ".0"
        )
        self.set_version(old_version, new_version)

    def set_patch(self, pre_release_tag=""):
        """
        Increment the patch number of project

        :var release_tag describes the tag ('a', 'b', 'rc', ...)
        :var release_tag_version describes the number behind the 'a', 'b' or 'rc'
        For e.g.:
        """

        current_version = self.get_version()
        current_patch = self.get_patch_version(current_version)
        current_pre_release_tag = self.get_current_pre_release_tag(current_patch)
        current_RELEASE_SEPARATOR = self.get_current_RELEASE_SEPARATOR(current_patch)
        new_patch = ""

        # The new patch should get a release tag
        if pre_release_tag:

            # Check, if the current patch already contains a pre_release_tag.
            if current_pre_release_tag:
                new_patch = (
                    str(current_patch.split(current_pre_release_tag, 2)[0])
                    + pre_release_tag
                )

                if pre_release_tag == current_pre_release_tag:
                    new_patch += str(
                        int(current_patch.split(current_pre_release_tag, 2)[1]) + 1
                    )
                else:
                    new_patch += "0"

            # The current patch does not contains a pre_release_tag.
            else:
                new_patch = (
                    str(int(current_patch) + 1)
                    + APISettings.RELEASE_SEPARATOR
                    + pre_release_tag
                    + "0"
                )

        # The new patch should not contain any tag. So just increase it.
        else:
            if current_RELEASE_SEPARATOR:
                new_patch = str(
                    int(current_patch.split(current_RELEASE_SEPARATOR, 2)[0]) + 1
                )
            elif current_pre_release_tag:
                new_patch = str(
                    int(current_patch.split(current_pre_release_tag, 2)[0]) + 1
                )
            else:
                new_patch = str(int(current_patch) + 1)

        new_version = (
            str(int(current_version.split(".", 5)[0]))
            + "."
            + str(int(current_version.split(".", 5)[1]))
            + "."
            + str(new_patch)
        )
        self.set_version(current_version, new_version)

    def __init__(self, release_tags=None):
        self.release_tags = release_tags or RELEASE_TAGS

    def __getattr__(self, attr):
        if attr not in self.release_tags.keys():
            raise AttributeError("Invalid VersionHandler Key: '%s'" % attr)

        val = self.release_tags[attr]
        return val


version = Version(RELEASE_TAGS)
