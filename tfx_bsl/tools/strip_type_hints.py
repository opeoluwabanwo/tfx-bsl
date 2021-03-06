# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Helper script to strip python hint annotations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import strip_hints


def strip_all_type_hints(root_dir):
  """Strip all type hints in place from the directory rooted from root_dir."""
  for root, _, files in os.walk(root_dir):
    for filename in files:
      if not filename.endswith('.py'):
        continue
      filepath = os.path.join(root, filename)
      print('Processing python file %s' % filepath)
      code_string = strip_hints.strip_file_to_string(
          filepath,
          to_empty=False,
          no_ast=False,
          no_colon_move=False,
          only_assigns_and_defs=False,
          only_test_for_changes=False)
      code_string = code_string.replace(
          'from typing import',
          'from tfx_bsl.types_compat import')
      with open(filepath, 'w') as f:
        f.write(code_string)


def main():
  if len(sys.argv) != 2:
    print('Expects only one argument.')
    sys.exit(1)

  repo_base = sys.argv[1]
  print('Stripping python 3 type hints under {}'.format(repo_base))
  strip_all_type_hints(repo_base)


if __name__ == '__main__':
  main()
