import sys
import json
import string
import re
import random

from landmark_ml.util import PageManagementUtilities
from learning.PageManager import PageManager
from landmark_ml.learning import TreeListLearner


class SlotComparator(object):

    def __init__(self):
        self.__min_page_occurrences = 7

    def cluster_slots(self, page_directory, write_debug_files=False):
        pages = PageManagementUtilities().load_pages(page_directory, limit=250)

        print "THERE ARE %d PAGES" % len(pages)

        page_mgr = PageManager(write_debug_files=write_debug_files)

        for page in pages:
            page_content = pages[page]
            page_mgr.addPage(page, page_content)

        # first, do some processing to get the visible chunks and the FULL prefix tree
        visible_structure = page_mgr.getVisibleTokenStructure()
        tl = TreeListLearner()
        (ptree, paths_to_vis_text, path_to_invis_toks) = tl.prefix_tree(visible_structure)  # , tag_only=True)

        # make this into a by-page structure, since we will want to use that for counts, etc.
        visible_text_by_page = {}
        for entry in visible_structure:
            page_id = entry['page_id']
            vis_text = entry['visible_token_buffer']
            invis_tokens = entry['invisible_token_buffer_before']
            loc = entry['first_vis_token'].token_location

            if page_id not in visible_text_by_page:
                visible_text_by_page[page_id] = []
            visible_text_by_page[page_id].append((vis_text, loc, invis_tokens))

        # using the by-page structure, get the chunks and its left and right neighbors
        chunk_neighbors = {}
        for page in visible_text_by_page:
            # need to order chunks so for any chunk we can get it's left and right neighbors
            # note that a chunk may occur more than once per page, so we need it to be a list
            by_location = sorted([(a[1], a[0], a[2]) for a in visible_text_by_page[page]])  # now it's (loc, txt), (loc, txt)
            for idx in range(len(by_location)):
                (location, txt, invis_preceding) = by_location[idx]
                txt = txt.strip()
                if txt not in chunk_neighbors:
                    chunk_neighbors[txt] = []
                before_neighbor = '<START>'
                after_neighbor = '<END>'

                invis_after = ''

                if idx > 0:
                    before_neighbor = by_location[idx - 1][1]
                if idx < len(by_location) - 1:
                    after_neighbor = by_location[idx + 1][1]
                    invis_after = by_location[idx + 1][2]
                chunk_neighbors[txt].append((before_neighbor, after_neighbor, invis_preceding, invis_after))

        # now, prune the full prefix tree into the prefixes we care about (those that occur enough)
        tl.set_min_page_occurrences(self.__min_page_occurrences)
        valid_prefixes = tl.prefix_tree_to_paths(ptree)

        # do the structure to get all the visible chunks associated with the prefixes
        prefixes_with_vis = tl.get_visible_text_for_prefix(valid_prefixes, paths_to_vis_text)

        for prefix in prefixes_with_vis:
            print "== %s ==" % prefix
            cluster_for_prefix = prefixes_with_vis[prefix]
            cluster_size = float(len(cluster_for_prefix))

            if cluster_size < self.__min_page_occurrences:
                continue

            cluster_members = {}
            for c in cluster_for_prefix:
                count = cluster_for_prefix.count(c)
                prop = float(count) / cluster_size
                cluster_members[c] = {
                    'raw_count': count,
                    'proportion': prop
                }

            # maybe we want to take the top X by count?? Look at those??
            top_x = 10
            inverted_by_count = {}
            for p in cluster_members:
                cnt = cluster_members[p]['raw_count']
                if cnt not in inverted_by_count:
                    inverted_by_count[cnt] = []
                inverted_by_count[cnt].append(p)

            keepers = []
            for cnt in sorted(inverted_by_count.keys(), reverse=True):
                keepers.extend(inverted_by_count[cnt])
                if len(keepers) > top_x:
                    break
            printers = keepers[:top_x]

            prev_chunk_coverage = {}
            tot_coverage = 0
            for p in printers:

                #if cluster_members[p]['raw_count'] < self.__min_page_occurrences:
                #    continue

                chunk_ngs = chunk_neighbors[p]
                prev_chunks = [a[0] for a in chunk_ngs if a[2].find(prefix) > -1]  # only care about chunks preceding that have prefix between them

                for pc in prev_chunks:
                    if pc not in prev_chunk_coverage:
                        prev_chunk_coverage[pc] = 0
                    prev_chunk_coverage[pc] += 1
                    tot_coverage += 1
                print "\tVALUE: "+p+" -- OCCURS: (%d/%d)" % (cluster_members[p]['raw_count'], int(cluster_size))#, str(prev_chunks))
            if len(cluster_members.keys()) > 10:
                print "\tand (%d) more" % (len(cluster_members.keys()) - 10)

            print "-- prev chunks --"
            for pc in prev_chunk_coverage:
                print "\t\t%s (%d/%d)" % (pc.encode('ascii', 'ignore'), prev_chunk_coverage[pc], tot_coverage)
            print "\n\n"

        #why are we missing viz text?
        # its ok if our clusters are too precise...


    def cluster_slots_old(self, page_directory, write_debug_files=False):
        pages = PageManagementUtilities().load_pages(page_directory, limit=250)

        print "THERE ARE %d PAGES" % len(pages)

        page_mgr = PageManager(write_debug_files=write_debug_files)

        for page in pages:
            page_content = pages[page]
            page_mgr.addPage(page, page_content)

        visible_structure = page_mgr.getVisibleTokenStructure()
        tl = TreeListLearner()
        tl.set_min_page_occurrences(self.__min_page_occurrences)
        (ptree, paths_to_vis_text, path_to_invis_toks) = tl.prefix_tree(visible_structure) #, tag_only=True)

        valid_prefixes = tl.prefix_tree_to_paths(ptree)


        # invert the paths to visible text so it's keyed on chunks...
        prefix_paths_for_chunks = {}
        for path in paths_to_vis_text:
            chnks = paths_to_vis_text[path]
            for chnk in chnks:
                if chnk not in prefix_paths_for_chunks:
                    prefix_paths_for_chunks[chnk] = []
                if path not in prefix_paths_for_chunks[chnk]:
                    prefix_paths_for_chunks[chnk].append(path)

        # make this into a by-page structure, since we will want to use that for counts, etc.
        visible_text_by_page = {}
        for entry in visible_structure:
            page_id = entry['page_id']
            vis_text = entry['visible_token_buffer']
            loc = entry['first_vis_token'].token_location

            if page_id not in visible_text_by_page:
                visible_text_by_page[page_id] = []
            visible_text_by_page[page_id].append((vis_text, loc))

        # ok, for each piece of visible text, let's get some features going
        visible_text_features = {}
        for page in visible_text_by_page:
            visible_text_features[page] = {}

            uniq_chunks = set([tup[0] for tup in visible_text_by_page[page]])

            # need to order chunks so for any chunk we can get it's left and right neighbors
            # note that a chunk may occur more than once per page, so we need it to be a list
            by_location = sorted([(a[1], a[0]) for a in visible_text_by_page[page]]) # now it's (loc, txt), (loc, txt)
            chunk_neighbors = {}
            for idx in range(len(by_location)):
                (location, txt) = by_location[idx]
                if txt not in chunk_neighbors:
                    chunk_neighbors[txt] = []
                before_neighbor = '<START>'
                after_neighbor = '<END>'
                if idx > 0:
                    before_neighbor = by_location[idx-1][-1]
                if idx < len(by_location) - 1:
                    after_neighbor = by_location[idx+1][-1]
                chunk_neighbors[txt].append((before_neighbor, after_neighbor))


            for chunk in uniq_chunks:
                visible_text_features[page][chunk] = {
                    'chunk_length': len(chunk),
                    'num_tokens': len(chunk.strip().split()),
                    'occurences_on_page': self.occurences_on_page(chunk, visible_text_by_page[page]),
                    'pct_pages_appears': self.pct_pages_appears(chunk, visible_text_by_page),
                    'number_periods': self.count_character_occurrence(chunk, "."),
                    'number_dashes': self.count_character_occurrence(chunk, "-"),
                    'number_commas': self.count_character_occurrence(chunk, ","),
                    'number_fwd_slashes': self.count_character_occurrence(chunk, "/"),
                    'number_back_slashes': self.count_character_occurrence(chunk, "\\"),
                    'number_dollar_signs': self.count_character_occurrence(chunk, "$"),
                    'tree_paths': prefix_paths_for_chunks[chunk],
                    'pct_non_letter_chars': self.pct_non_chars(chunk),
                    'chunk_before': [a[0] for a in chunk_neighbors[chunk]],
                    'chunk_after': [a[-1] for a in chunk_neighbors[chunk]],
                    'page': page, # long story, but makes it easier to invert by chunk below...
                }

        # ok, so now let's invert this? Want to look at each chunk...
        chunk_features = {}
        for page in visible_text_features:
            for chunk in visible_text_features[page]:
                if chunk not in chunk_features:
                    chunk_features[chunk] = {}
                for feature in visible_text_features[page][chunk]:
                    if feature not in chunk_features[chunk]:
                        chunk_features[chunk][feature] = []
                    chunk_features[chunk][feature].append(visible_text_features[page][chunk][feature])


        # so, dedupe the values (helps take care of some that will be the same, like length, across all of them
        # really lazy bc I could do something smarter about all of these above
        chunk_features_final = {}
        for chunk in chunk_features:
            chunk_features_final[chunk] = {}
            for feature in chunk_features[chunk]:
                # going to uniqefy each value
                try:
                    # in a try bc list of listst causes problems bc its unhashable
                    chunk_features_final[chunk][feature] = list(set(chunk_features[chunk][feature]))
                except:
                    # so if it's a list of lists, flatten it, and then uniquefy
                    chunk_features_final[chunk][feature] = list(set([item for sublist in chunk_features[chunk][feature] for item in sublist]))

        print json.dumps(chunk_features_final)
        print "-----------------------------"
        print "-----------------------------"
        for chunk in chunk_features_final:
            if chunk_features_final[chunk]['pct_pages_appears'][0] > 0.05: # 0.7: # TODO: Perhaps make this a fixed number, rather than PCT (5, 7)
                do_print = False

                output = chunk+"\n"
                output += '\t'+' -- '.join(chunk_features_final[chunk]['chunk_after'][:5])+" +("+str(len(chunk_features_final[chunk]['chunk_after']) - 5)+") more\n"

                # if the text after has many values, then maybe chunk is some sort of attribute text?
                # or look at how many times each of the after texts appaers across teh site? If low, then it changes
                # a lot... so you could do an average? see if it's low and then that makes current chunk look like
                # an attribute?
                # Otherwise it could be "static page info" or site info? (like categories, such as states, or headers)
                change_estimator =\
                    float(len(chunk_features_final[chunk]['chunk_after'])) / float(len(visible_text_by_page.keys()))

                if change_estimator >= 0.01: #0.1:
                    do_print = True
#                    print "\t -- ATTRIBUTE"

                    #look at the invisible text between this visible token and the ones that follow it
                    #so you need to somehow figure that out, and count thsoe paths

                    path_counts = {}
                    for chnk in chunk_features_final[chunk]['chunk_after']:
                        paths = chunk_features_final[chnk]['tree_paths']
                        for pth in paths:
                            if pth not in path_counts:
                                path_counts[pth] = 0.0
                            path_counts[pth] += 1.0
                    for p in path_counts:
                        path_counts[p] = path_counts[p] / float(len(chunk_features_final[chunk]['chunk_after']))

                    output += "\tPATH COUNTS:\n"
                    for p in path_counts:
                        output += "\t\t"+p+" -- "+str(path_counts[p])+"\n"

                if do_print:
                    print output
                    print '......'

#        so if you are flagged as data, essentially, if the guy preceding you is a data flag, then your value is data...

    def pct_pages_appears(self, chunk, visible_text_by_page):
        seen_pages = 0
        for page in visible_text_by_page:
            cnt = self.occurences_on_page(chunk, visible_text_by_page[page])
            if cnt > 0:
                seen_pages += 1
        return float(seen_pages) / float(len(visible_text_by_page.keys()))

    def occurences_on_page(self, chunk, page_chunks):
        count = 0
        for (p_chunk, location) in page_chunks:
            if p_chunk == chunk:
                count += 1
        return count

    def count_character_occurrence(self, chunk, character):
        return chunk.count(character)

    def strip_punct(self, chunk):
        return str(chunk.encode('ascii', 'ignore')).translate(string.maketrans("", ""), string.punctuation)

    def pct_non_chars(self, chunk):
        return 1.0 - float(len(self.strip_punct(chunk))) / float(len(chunk))


if __name__ == '__main__':
    s = SlotComparator()
    s.cluster_slots(sys.argv[1])
