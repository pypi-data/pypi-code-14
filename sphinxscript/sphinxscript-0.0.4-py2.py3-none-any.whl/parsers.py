'''
Tools for parsing filenames and extracting comment headers from files
'''

import os, re, shutil, argparse



class Parser(object):

    PARSERS = {
    
        'r': {

            'regex': [
                # Files can end in .r or .rscript
                '\.(r|rscript)$'
            ],

            # block patterns can be defined with:
            'block_patterns': [
                # a "multiline quoted block"
                r'(\s*\n)*\s*\'(?P<comment>[^\']*)\'', 

                # a 'multiline quoted block'
                r'(\s*\n)*\s*\"(?P<comment>[^\"]*)\"'], 

            # start-of-line patterns can be defined with:
            'start_patterns': [

                # a start-of-line #
                (r'(\s*\n)*(?P<comment>([\ \t]*#[^\n]*(\n|/Z))+)', r'^\s*#+')]
        },

        'matlab': {

            'regex': [
                # Files can end in .m
                r'\.m$'
            ],

            # block patterns can be defined with
            'block_patterns': [
                
                # a "multiline quoted block"
                r'(\s*\n)*\s*\'(?P<comment>[^\']*)\'', 
                
                # a 'multiline quoted block'
                r'(\s*\n)*\s*\"(?P<comment>[^\"]*)\"', 

                # a %{ multiline comment block %}
                r'(\s*\n)*\s*\%\{(?P<comment>[^\']*)\%\}'],

            # start-of-line patterns can be defined with:
            'start_patterns': [

                # a start-of-line %
                (r'(\s*\n)*(?P<comment>([\ \t]*\%+[^\n]*(\n|/Z))+)', r'^\s*\%+')]

        },

        'stata': {

            'regex': [
                # Files can end in .do
                '\.do$'
            ],

            # block patterns can be defined with a /* multiline */
            'block_patterns': [r'(\s*\n)*\s*\/\*(?P<comment>[^\']*)\*\/'],

            # start patterns can be defined with:
            'start_patterns': [

                # a start-of-line *
                (r'(\s*\n)*(?P<comment>([\ \t]*\*[^\n]*(\n|/Z))+)', r'^\s*\*+'),

                # a start-of-line // (don't allow end-of-line comments for header)
                (r'(\s*\n)*(?P<comment>([\ \t]*\/\/[^\n]*(\n|/Z))+)', r'^\s*\/\/')]

            },

        'python': {

            'regex': [
                # Files can end in .py, .pyc, .pyb, etc.
                r'\.py\w*$'
            ],

            # block patterns can be defined with: 
            'block_patterns': [

                # a ''' multiline quoted block '''
                r'(\s*\n)*\s*\'\'\'(?P<comment>([^\'](\'{,2}(?!=\')))*)\'\'\'',

                # a """ multiline quoted block """
                r'(\s*\n)*\s*\"\"\"(?P<comment>([^\"](\"{,2}(?!=\")))*)\"\"\"'],

            # start patterns can be defined with:
            'start_patterns': [
            
                # a start-of-line #
                (r'(\s*\n)*(?P<comment>([\ \t]*#[^\n]*(\n|/Z))+)', r'^\s*#+')]

        },

        'julia': {

            'regex': [
                # Files can end in .jl or .julia
                r'\.(jl|julia)$'
            ],

            # block patterns can be defined with: 
            'block_patterns': [

                # a ''' multiline quoted block '''
                r'(\s*\n)*\s*\#\=(?P<comment>([^\'](\'{,2}(?!=\')))*)\=\#',

                # a """ multiline quoted block """
                r'(\s*\n)*\s*\"\"\"(?P<comment>([^\"](\"{,2}(?!=\")))*)\"\"\"'],

            # start patterns can be defined with:
            'start_patterns': [
            
                # a start-of-line #
                (r'(\s*\n)*(?P<comment>([\ \t]*#[^\n]*(\n|/Z))+)', r'^\s*#+')]
        }
    }
    '''
    PARSERS defines the set of regular expressions for each available syntax

    Each syntax has the following three entries:

    :regex: list of regular expressions which match valid filenames for each 
        syntax
    :block_patterns: list of regular expressions whcih match block comments. 
        These expressions should return a 'comment' group if matched.
    :start_patterns: list of tuples. Each tuple contains a regular expression 
        which matches start-of-line comments and a regular expression which can 
        be used to strip the comment characters.
    '''



    @staticmethod
    def _extract_comment_header(doc, block_patterns, start_patterns):
        '''
        Extract the comment header from a file
    
        Parameters
        ----------
        doc : str
            document from which to extract the header

        block_patterns : list
            list of regular expressions whcih match block comments. These 
            expressions should return a 'comment' group if matched.
        
        start_patterns : list
            list of tuples. Each tuple contains a regular expression which 
            matches start-of-line comments and a regular expression which can be 
            used to strip the comment characters.

        Returns

        header : str
            Comment header

        '''

        # Search for block patterns first
        # If these show up at the top of a file, parse the block pattern 
        # and then return the result
        for pattern in block_patterns:
            search = re.match(pattern, doc)
            if search:
                return search.group('comment')

        # If no block patterns match, search for start of line comments
        # This is to get around julia syntax issue where the block comment 
        # ``#= ... =#`` could be misread as a line comment.
        for pattern, sub_pattern in start_patterns:
            comment_search = re.match(pattern, doc)
            if comment_search:
                comment_lines = map(lambda l: re.sub(sub_pattern, '', l), comment_search.group('comment').split('\n'))

                # Find the minimum number of whitespace characters on the left 
                # of each line
                min_whitespace = min([len(l) - len(l.lstrip()) for l in comment_lines if len(l) > 0])

                # strip min_whitespace whitespace characters from the left side
                comment_lines = map(lambda l: l if len(l) < min_whitespace else l[min_whitespace:], comment_lines)
                
                # join comment lines into a comment block
                return '\n'.join(comment_lines)
            
        return ''

    @classmethod
    def determine_syntax_from_filename(cls, filepath):
        '''
        Determine the programming language from a filename or filepath

        Parameters
        ----------
        filepath : str
            filename or filepath from which to determine syntax

        Returns
        -------
        syntax : str
            name of syntax indicated by filepath

        '''

        for syntax, defn in cls.PARSERS.items():
            for patt in defn['regex']:
                if re.search(patt, filepath, re.I):
                    return syntax
        
        raise ValueError('Cannot determine filetype. Extension unknown.')


    @classmethod
    def extract_comment_header_from_file(cls, filepath):
        '''
        Extract the comment header from a file

        Parameters
        ----------
        filepath : str
            filename or filepath from which to determine syntax

        Returns
        -------
        header : str
            First comment header extracted from filepath
        '''

        syntax = cls.determine_syntax_from_filename(filepath)

        with open(filepath, 'r') as file_obj:

            doc = file_obj.read()

            return cls._extract_comment_header(
                doc, 
                cls.PARSERS[syntax]['block_patterns'],
                cls.PARSERS[syntax]['start_patterns'])
