from filesystem_crawler import MatchRule
import re


def parse_match_rules(basedir, rawRules):
    basedir = re.escape(basedir)
    rules = []
    errors = []

    rawLines = None
    rawLines = rawRules.splitlines()

    for lineCount, rawLine in enumerate(rawLines):
        rawLine = rawLine.strip()

        # continue uppon comments or empty lines?
        if not rawLine or rawLine[0] == '#':
            continue

        patternsLine, (isRegex, isNegated, filesOnly, dirsOnly) = (
            _extract_flags_from_rawline(rawLine, 'r', '!i', 'f', 'd'))

        pathPattern, contentPattern = (
            _extract_patterns_form_patters_line(patternsLine))

        pathPattern = _path_pattern_to_regex(pathPattern, isRegex)

        try:
            rules.append(MatchRule(
                basedir + pathPattern + '$',
                not isNegated, dirsOnly,
                filesOnly, contentPattern))
        except Exception as e:
            errors.append((lineCount + 1, e))
    return rules, errors


def parse_match_rules_from_file(basedir, rulesFilename):
    with open(rulesFilename) as f:
        rawRules = f.read()
    return parse_match_rules(basedir, rawRules)


def _path_pattern_to_regex(pathPattern, isRegex):
    # is regex
    if isRegex:
        pathPattern = pathPattern.replace('/', r'\\')
    # is gitignore sintax
    else:
        pathPattern = _gitignorepattern_to_regex(pathPattern)
    return pathPattern


def _gitignorepattern_to_regex(pattern):
    pattern = pattern.replace('.', r'\.')
    pattern = pattern.replace('/', r'\\')
    pattern = pattern.replace('**', r'f7b75160-5e4d-49ec-bf3a-949238767509')
    pattern = pattern.replace('*', r'[^\\]*')
    pattern = pattern.replace('f7b75160-5e4d-49ec-bf3a-949238767509', r'.*')
    return pattern


def _extract_flags_from_rawline(line, *flags):
    '''
    Returns a boolean indicating if each of the provided flags exist
    '''
    flagged = [x for x in flags]
    for ch in line:
        for flag in flags:
            if ch in flag:
                flagged = [True if x == flag else x for x in flagged]
                line = line[1:]
                break
        else:
            break
    return line, [True if x is True else False for x in flagged]


def _extract_patterns_form_patters_line(line):
    '''
    Splits path and content pattherns
    '''
    patterns = line.strip().replace('    ', '\t').split('\t')
    return patterns[0], patterns[1] if len(patterns) > 1 else None
