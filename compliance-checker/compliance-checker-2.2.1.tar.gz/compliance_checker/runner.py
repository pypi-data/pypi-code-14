from __future__ import print_function

import traceback
import sys
import io
from io import StringIO

from compliance_checker.suite import CheckSuite


class ComplianceChecker(object):
    """
    Compliance Checker runner class.

    Ties together the entire compliance checker framework, is used from
    the command line or can be used via import.
    """
    @classmethod
    def run_checker(cls, ds_loc, checker_names, verbose, criteria, output_filename='stdout', output_format='stdout'):
        """
        Static check runner.

        @param  ds_loc          Dataset location (url or file)
        @param  checker_names    List of string names to run, should match keys of checkers dict (empty list means run all)
        @param  verbose         Verbosity of the output (0, 1, 2)
        @param  criteria        Determines failure (lenient, normal, strict)
        @param  output_filename Path to the file for output
        @param  output_format   Format of the output

        @returns                If the tests failed (based on the criteria)
        """
        cs = CheckSuite()
        ds = cs.load_dataset(ds_loc)
        score_groups = cs.run(ds, *checker_names)

        if criteria == 'normal':
            limit = 2
        elif criteria == 'strict':
            limit = 1
        elif criteria == 'lenient':
            limit = 3

        if output_filename == '-' and output_format == 'text':
            groups = cls.stdout_output(cs, score_groups, verbose, limit)

        elif output_format == 'html':
            groups = cls.html_output(cs, score_groups, output_filename, ds_loc, limit)

        elif output_format == 'json':
            groups = cls.json_output(cs, score_groups, output_filename, ds_loc, limit)

        else:
            raise TypeError('Invalid format %s' % output_format)

        errors_occurred = cls.check_errors(score_groups, verbose)

        return cs.passtree(groups, limit), errors_occurred

    @classmethod
    def stdout_output(cls, cs, score_groups, verbose, limit):
        '''
        Calls output routine to display results in terminal, including scoring.
        Goes to verbose function if called by user.

        @param cs           Compliance Checker Suite
        @param score_groups List of results
        @param verbose      Integer value for verbosity level
        @param limit        The degree of strictness, 1 being the strictest, and going up from there.
        '''
        for checker, rpair in score_groups.items():
            groups, errors = rpair
            score_list, points, out_of = cs.standard_output(limit, checker, groups)
            if not verbose:
                cs.non_verbose_output_generation(score_list, groups, limit, points, out_of)
            else:
                cs.verbose_output_generation(groups, limit, points, out_of)
        return groups

    @classmethod
    def html_output(cls, cs, score_groups, output_filename, ds_loc, limit):
        '''
        Generates rendered HTML output for the compliance score(s)
        @param cs              Compliance Checker Suite
        @param score_groups    List of results
        @param output_filename The file path to output to
        @param ds_loc          Location of the source dataset
        @param limit           The degree of strictness, 1 being the strictest, and going up from there.
        '''
        for checker, rpair in score_groups.items():
            groups, errors = rpair
            if output_filename == '-':
                f = StringIO()
                cs.html_output(checker, groups, f, ds_loc, limit)
                f.seek(0)
                print(f.read())
            else:
                with io.open(output_filename, 'w', encoding='utf8') as f:
                    cs.html_output(checker, groups, f, ds_loc, limit)

        return groups

    @classmethod
    def json_output(cls, cs, score_groups, output_filename, ds_loc, limit):
        '''
        Generates JSON output for the ocmpliance score(s)
        @param cs              Compliance Checker Suite
        @param score_groups    List of results
        @param output_filename The file path to output to
        @param ds_loc          Location of the source dataset
        @param limit           The degree of strictness, 1 being the strictest, and going up from there.
        '''
        for checker, rpair in score_groups.items():
            groups, errors = rpair
            if output_filename == '-':
                f = StringIO()
                cs.json_output(checker, groups, f, ds_loc, limit)
                f.seek(0)
                print(f.read())
            else:
                with io.open(output_filename, 'w', encoding='utf8') as f:
                    cs.json_output(checker, groups, f, ds_loc, limit)

        return groups

    @classmethod
    def check_errors(cls, score_groups, verbose):
        '''
        Reports any errors (exceptions) that occurred during checking to stderr.
        Goes to verbose function if called by user.

        @param score_groups List of results
        @param verbose      Integer value for verbosity level
        '''
        errors_occurred = False
        for checker, rpair in score_groups.items():
            groups, errors = rpair
            if len(errors):
                errors_occurred = True
                print("WARNING: The following exceptions occured during the %s checker (possibly indicate compliance checker issues):" % checker, file=sys.stderr)
                for check_name, epair in errors.items():
                    print("%s.%s: %s" % (checker, check_name, epair[0]), file=sys.stderr)

                    if verbose > 0:
                        traceback.print_tb(epair[1].tb_next.tb_next)    # skip first two as they are noise from the running itself @TODO search for check_name
                        print(file=sys.stderr)

        return errors_occurred
