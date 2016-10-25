'''
Create .rst documentation of scripts from header comments
'''

import os, re, shutil, argparse
import parsers


SourceFileTemplate = '''
{filename}
{line}

Header
~~~~~~

{header}


Raw Code
~~~~~~~~

.. literalinclude:: {filepath}
    :linenos:

'''

DirectoryIndexFileTemplate = '''
{path}
{line}

.. toctree::
'''


class SourceFile(object):

    TEMPLATE = SourceFileTemplate
    
    @classmethod
    def create_doc_rst_from_sourcefile(cls, filepath, target):
        '''
        Fill keyword values in :py:attr:`TEMPLATE`

        Parameters
        ----------

        filepath : str
            Path to the script being documented

        target : str
            Path to the documentation file to be written


        '''

        p = parsers.Parser
        filename = os.path.basename(filepath)

        # Create a .rst-style documentation from cls.TEMPLATE
        doc = cls.TEMPLATE.format(
            filename = filename,
            line = '-'*max(len(filename), 50),
            header = p.extract_comment_header_from_file(filepath),
            filepath = os.path.relpath(filepath, os.path.dirname(target)).replace('\\', '/'))

        # check to see if target's directory exists
        if not os.path.isdir(os.path.dirname(target)):

            # if not, create it
            os.makedirs(os.path.dirname(target))

        # write the documentation for sourcefile to target
        with open(target, 'w+') as fp:
            fp.write(doc)

def _inside_dir(checkdir, target):
    chk = os.path.normpath(os.path.abspath(checkdir))
    if chk == os.path.normpath(os.path.abspath(target))[:len(chk)]:
        return True

    return False

def find_exclude(candidate, excludes):
    for ex in excludes:
        if _inside_dir(ex, candidate):
            return True

    return False


def build_docs(target='..', dest='.', excludes = ['../.git', '../dist', '../build']):
    '''
    Build docs, mirroring target directory strucuture in dest

    Parameters
    ----------
    target : str
        Path to repo root containing source scripts

    dest : str
        Path to documentation root

    excludes : list
        List of subdirectories within target to exclude from docs creation. By 
        default, ``./.git``, ``./dist``, and ``./build`` are excluded. The 
        argument ``dest`` is excluded automatically (regardless of user input).
    '''

    scripts_directory = os.path.normpath(os.path.abspath(os.path.expanduser(target)))
    dest = os.path.normpath(os.path.abspath(os.path.expanduser(dest)))

    # Add dest to excludes
    excludes.append(dest)

    # Make excludes absolute and normalized paths
    excludes = map(os.path.abspath, excludes)
    excludes = map(os.path.normpath, excludes)


    sphinxscript_path = os.path.join(dest, 'sphinxscript')
    if os.path.isdir(sphinxscript_path):
        shutil.rmtree(sphinxscript_path)

    for current_scripts_dir, inner_dirs, inner_files in os.walk(scripts_directory):

        if find_exclude(current_scripts_dir, excludes):
            continue

        current_dirname = os.path.basename(current_scripts_dir)
        current_relpath = os.path.relpath(current_scripts_dir, scripts_directory)

        includes_to_add_to_dir_rst = []

        for f in inner_files:
            
            try:
                # Create documentation for script
                SourceFile.create_doc_rst_from_sourcefile(
                    filepath = os.path.join(current_scripts_dir, f),
                    target = os.path.join(sphinxscript_path, current_relpath, os.path.splitext(f)[0] + '.rst')
                    )

                # Add relpath to file to dir .rst file queue
                includes_to_add_to_dir_rst.append(
                    os.path.join(
                        os.path.basename(os.path.normpath(os.path.join(sphinxscript_path, current_relpath))), 
                        os.path.splitext(os.path.basename(f))[0]
                        ))

            except ValueError:

                # File type not recognized. Skip silently.
                pass

        # Assemble path to dir .rst file

        # dir_rst_dirpath is the path to the folder we are documenting
        current_doc_dirpath = os.path.normpath(os.path.join(sphinxscript_path, current_relpath))

        # dir_rst_filepath is one directory below current_doc_dirpath, but has 
        # the same name as basename(current_doc_dirpath)
        dir_rst_filepath = os.path.join(
            current_doc_dirpath, '..', os.path.basename(current_doc_dirpath) +'.rst')

        # Create file at dir_rst_filepath
        with open(dir_rst_filepath, 'w+') as ds:

            ds.write(DirectoryIndexFileTemplate.format(
                path = current_dirname,
                line = '-'*max(len(current_dirname), 50)
                ))

            for a in includes_to_add_to_dir_rst:
                ds.write('    {}\n'.format(a.replace('\\', '/')))

            for d in inner_dirs:
                if find_exclude(os.path.join(current_scripts_dir, d), excludes):
                    continue


                inner_dir_docpath = os.path.join(
                    os.path.basename(os.path.normpath(os.path.join(sphinxscript_path, current_relpath))), 
                    d)

                ds.write('    {}\n'.format(inner_dir_docpath.replace('\\', '/')))

