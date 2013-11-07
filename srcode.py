from optparse import OptionParser
import os, sys, re
import subprocess

def run_command():
    parser = OptionParser()

    (options, args) = parser.parse_args()
    
    known_command = False
    
    if len(args):
        command = args[0]
        dir = os.getcwd()
        
        if command == 'format':
            if len(args) >= 2:
                known_command = True
                print_formatted_file(args[1])

    if not known_command:
        show_help()

def print_formatted_file(file_path):
    f = open(file_path, 'rb')
    indent_string = ' ' * 4
    indent = 0
    modes = ['html']
    li = 0    
    django_block_indents = []
    for line in f.readlines():
        li += 1
        line = re.sub(u'^\s*', '', line)
        line = re.sub(ur'[\n\r]', '', line)
        current_indent = indent
        
        i = -1
        # Don't use 'for i in range()' here because we need to adjust i 
        # within the loop.
        
        # After the while, the indent variable correspond to the indentation
        # of the next line.
        #
        # So the current line will be indented by current_indent
        while i < len(line):
            i += 1
            
            # detect the modes
            if line[i:].startswith('<script'):
                modes.append('script')
                # Since the mode is 'script'
                # we won't go through the regular html case of '<...'
                indent += 1
            if line[i:].startswith('</script'):
                modes.pop()
            if line[i:].startswith('{%') or line[i:].startswith('{{'):
                modes.append('django')
            if line[i:].startswith('%}') or line[i:].startswith('}}'):
                modes.pop()
                # we do this to avoid the second } being processed by the script mode.
                i += 1
                continue
            if len(modes) < 1:
                print 'ERROR line %d: left all modes' % li
                print line
                exit()
            
            # Detect block beginnings and ends
            # this affects the indentation.
            current_mode = modes[-1]
            if current_mode == 'script':
                if line[i:].startswith('{'):
                    indent += 1
                if line[i:].startswith('}'):
                    indent -= 1
            if current_mode == 'django':
                if re.search(ur'^{%\s+?(comment|for|if|block)[^%]*\s+?%}', line[i:]):
                    django_block_indents.append(indent)
                    indent += 1
                if re.search(ur'^{%\s+?(endcomment|endfor|endif|endblock)[^%]*\s+?%}', line[i:]):
                    indent -= 1                        
                    last_block_indent = django_block_indents.pop()
                    if last_block_indent != indent:
                        print '<!-- WARNING: indentation has changed within this block  %s %s -->' % (indent, last_block_indent)
                        indent = last_block_indent
                        current_indent = indent
            if current_mode == 'html':
                if line[i:].startswith('/>'):
                    indent -= 1
                if line[i:].startswith('<'):
                    if line[i:].startswith('</'):
                        indent -= 1
                    else:
                        indent += 1

        # special case, else are not end of block but indented like them
        if re.search(ur'^{%\s+(else|elif)[^%]*\s+%}$', line):
            current_indent -= 1
        
        # end of a block (e.g. </div> or {% endif %}), 
        # we force the current indentation to the same indentation of the next line
        if indent < current_indent: current_indent = indent
        
        # Just make sure that the current ident is at least one above that of the 
        # block we are in.
        # This is necessary when we have {% if %} \n </div> \n </div> \n {% endif %}
#         if django_block_indents:
#             django_block_indent = django_block_indents[-1]
#             current_indent = max(django_block_indent + 1, current_indent)
        
        print '%s%s' % (indent_string * current_indent, line)

    f.close()

def show_help():
    print '''
Usage:
    python srcode.py format FILE.html
        Correct the indentation in a django template file.
'''

run_command()
