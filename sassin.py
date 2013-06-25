# forked from rapydcss https://bitbucket.org/pyjeon/rapydcss
# Portion (C) 2012  Alexander Tsepkov

import os
import StringIO

# attempt to load PySCSS module
try:
  import scss
  if 'Scss' in dir(scss):
    compile_scss = scss.Scss(scss_opts={'compress':False}).compile
except:
  compile_scss = None


def compile(sass, source_fname=''):
  output_buffer = StringIO.StringIO()

  state = {
    'indent_mark': 0,
    'prev_indent': 0,
    'prev_line': '',
    'nested_blocks': 0,
    'line_buffer': '',
  }
  
  # create a separate funtion for parsing the line so that we can call it again after the loop terminates
  def parse_line(line, i_line, state):
    line = state['line_buffer'] + line.rstrip() # remove EOL character
    if line and line[-1] == ',':
      state['line_buffer'] = line[:-1] + ' '
      return
    else:
      state['line_buffer'] = ''

    is_comment = state['prev_line'].strip().startswith('/*')
    if is_comment:
      text = state['prev_line'].rstrip()
      if not text.endswith('*/'):
        state['prev_line'] = text + ' */'

    indent = len(line) - len(line.lstrip())
   
    # make sure we support multi-space indent as long as indent is consistent
    if indent and not state['indent_mark']:
      state['indent_mark'] = indent
  
    if state['indent_mark']:
      check = indent % state['indent_mark']
      if 0 < check < state['indent_mark']:
        raise ValueError('Error: indentation not multiple of first indent, at {0}:{1}'.format(i_line, source_fname))
      indent /= state['indent_mark']
  
    if indent == state['prev_indent']:
      if '@import' in state['prev_line']:
        import_fname = state['prev_line'].split()[1]
        if import_fname.startswith('"'):
          import_fname = import_fname[1:-1]
        if not os.path.isfile(import_fname):
          raise IOError('Error: @import {0} not found at {1}:{2}'.format(import_fname, source_fname, i_line))
        state['prev_line'] = compile_from_file(import_fname)
      elif not is_comment and state['prev_line']:
        state['prev_line'] += ';'
    elif indent > state['prev_indent']:
      # new indentation is greater than previous, we just entered a new block
      state['prev_line'] +=  ' {'
      state['nested_blocks'] += 1
    else:
      # indentation is reset, we exited a block
      block_diff = state['prev_indent'] - indent
      if not is_comment and state['prev_line']:
        state['prev_line'] += ';'
      state['prev_line'] += ' }' * block_diff
      state['nested_blocks'] -= block_diff

    if state['prev_line']:
      output_buffer.write(state['prev_line'] + '\n')

    state['prev_indent'] = indent
    state['prev_line'] = line
  
  for i_line, input_line in enumerate(sass.splitlines()):
    if input_line.strip():
      parse_line(input_line, i_line, state)
  parse_line('\n', i_line+1, state) # parse the last line stored in prev_line buffer

  return output_buffer.getvalue()


def compile_from_file(sass_fname):
  with open(sass_fname) as f:
    sass_text = f.read()
  return compile(sass_text, source_fname=sass_fname)


def compile_with_scss(sass):
  if compile_scss is None:
    raise "Error: couldn't load a SCSS compiler"
  scss_text = compile(sass)
  return compile_scss(scss_text)

