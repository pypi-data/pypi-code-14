import os, shutil
from datetime import datetime


def write_rotate(out_path, line):
  with open(out_path, 'a') as f:
   f.write('{} {}\n'.format(datetime.utcnow(), line))

  # limit files to 1 MB
  if os.path.getsize(out_path) > 1024 ** 2:
    shutil.move(out_path, out_path + '.old')

write_rotate('out.txt', '---begin logrot piped output---')
while True:
  try:
    write_rotate('out.txt', raw_input())
  except EOFError:
    break
write_rotate('out.txt', '---end logrot piped output---')
