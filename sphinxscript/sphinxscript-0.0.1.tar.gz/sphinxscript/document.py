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


def build_docs(target='..', dest='.'):
    '''
    Build docs, mirroring target directory strucuture in dest

    Parameters
    ----------
    target : str
        Path to repo root containing source scripts

    dest : str
        Path to documentation root
    '''
    target = os.path.abspath(target)
    dest = os.path.abspath(dest)

    sphinxscript_path = os.path.join(dest, os.path.basename(target))
    if os.path.isdir(sphinxscript_path):
        shutil.rmtree(sphinxscript_path)

    for dirpath, dirs, files in os.walk(os.path.abspath(os.path.expanduser(target))):

        # If ``dirpath`` is inside the docs dir ``dest``, skip
        reldoc = os.path.relpath(dest, dirpath)
        if re.search(r'^\.\.([/\\]+\.\.)*$'.format(re.escape(os.sep)), reldoc) or reldoc == os.curdir:
            continue

        dirname = os.path.basename(os.path.abspath(dirpath))
        relpath = os.path.relpath(dirpath, os.path.abspath(os.path.expanduser(target)))

        to_add = []
        for f in files:
            try:
                SourceFile.create_doc_rst_from_sourcefile(
                    filepath = os.path.join(dirpath, f),
                    target = os.path.join(sphinxscript_path, relpath, os.path.splitext(f)[0] + '.rst')
                    )
                to_add.append(
                    os.path.join(
                        os.path.basename(dirpath), 
                        os.path.splitext(os.path.basename(f))[0]
                        ))

            except ValueError:
                pass

        dirspec = os.path.join(sphinxscript_path, relpath, '..', dirname +'.rst')
        with open(dirspec, 'w+') as ds:
            ds.write(DirectoryIndexFileTemplate.format(
                path=dirname,
                line='-'*max(len(dirname), 50)
                ))

            for a in to_add:
                ds.write('    {}\n'.format(a.replace('\\', '/')))

            for d in dirs:
                if os.path.abspath(os.path.join(dirpath, d)) == os.path.abspath(dest):
                    continue
                ds.write('    {}\n'.format(os.path.join(os.path.basename(dirpath), d)).replace('\\', '/'))

