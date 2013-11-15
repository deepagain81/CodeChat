#!/usr/bin/python
#
# .. -*- coding: utf-8 -*-
#
#    Copyright (C) 2012-2013 Bryan A. Jones.
#
#    This file is part of CodeChat.
#
#    CodeChat is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#    CodeChat is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along with CodeChat.  If not, see <http://www.gnu.org/licenses/>.
#
# ***************************
# code_chat.py - Run CodeChat
# ***************************
# Author: Bryan A. Jones <bjones AT ece DOT msstate DOT edu>
#
# This script runs the CodeChat application.
#
# This script will be imported by the main entry point, then again by the multiprocessing module. So, only put imports below needed by both.
from CodeChat.MultiprocessingSphinx import MultiprocessingSphinxManager

if __name__ == '__main__':
    # Hide this import, so the MultiprocessingSphinx process doesn't import unnecessary items.
    from CodeChat.CodeChat import main

    msm = MultiprocessingSphinxManager()
    main(msm)
