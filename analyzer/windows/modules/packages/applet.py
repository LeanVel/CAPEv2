# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from __future__ import absolute_import
import tempfile

from lib.common.abstracts import Package


class Applet(Package):
    """Java Applet analysis package."""

    PATHS = [
        ("ProgramFiles", "Mozilla Firefox", "firefox.exe"),
        ("ProgramFiles", "Internet Explorer", "iexplore.exe"),
    ]

    def make_html(self, path, class_name):
        html = f"""
        <html>
            <body>
                <applet archive="{path}" code="{class_name}" width="1" height="1">
                </applet>
            </body>
        </html>
        """

        _, file_path = tempfile.mkstemp(suffix=".html")
        with open(file_path, "w") as file_handle:
            file_handle.write(html)

        return file_path

    def start(self, path):
        browser = self.get_path("browser")
        class_name = self.options.get("class")
        html_path = self.make_html(path, class_name)
        return self.execute(browser, f'"{html_path}"', html_path)
