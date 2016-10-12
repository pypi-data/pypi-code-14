from random import shuffle

class TruffleShuffle(object):

    def __init__(self, page_manager):
        self.__chunkBreakSeparator = '<BRK>'
        self.__page_manager = page_manager

    def get_chunk_separator(self):
        return self.__chunkBreakSeparator

    def get_page_manager(self):
        return self.__page_manager

    # so maybe you table randome samples of 3 pages, and induce a template
    # if you find a template that is similar (or matches) most, then that is the template for this cluster?
    # or you could do a greedy build or something (e.g., add another page and if it doesn't change, you are good)
    def sample_and_learn_template(self, cluster_members, sub_sample_size=5, iterations=10):
        stripes = []
        for itr in range(iterations):
            shuffle(cluster_members) # randomly orders them
            random_members = cluster_members[0:sub_sample_size] # get the sub-sample
            template = self.induce_template(random_members).getStripes()

            stripe_texts = []
            for stripe in template:
                stripe_text = stripe['stripe']
                stripe_texts.append(stripe_text)

            # now, only keep the top X longest stripes and see what it does...
            top_x = 10  # for now...
            stripes_by_size = {}
            for stpe in stripe_texts:
                stsz = len(stpe)
                if stsz not in stripes_by_size:
                    stripes_by_size[stsz] = []
                stripes_by_size[stsz].append(stpe)

            top_sizes = sorted(stripes_by_size.keys(), reverse=True)
            kept_big_stripes = []
            for tsz in top_sizes:
                kept_big_stripes.extend(stripes_by_size[tsz])
                if len(kept_big_stripes) > top_x:
                    break
            # stripes_string = self.__chunkBreakSeparator.join(stripe_texts)
            stripes_string = self.__chunkBreakSeparator.join(kept_big_stripes[:top_x])
            stripes.append(stripes_string)

        template_occurrences = {}
        for tstr in stripes:
            template_occurrences[tstr] = stripes.count(tstr)

        for sstring in template_occurrences:
            if template_occurrences[sstring] > 1:
                print "Template: %s" % sstring[:250]  # just a little bit
                print "Induced template occurs %d out of %d" % (template_occurrences[sstring], iterations)

    def induce_template(self, cluster_members):
        return self.__page_manager.getSubPageManager(cluster_members)

    def prep_truffles_to_shuffle(self, tokens_only = False):
        all_chunks = set()
        page_chunks_map = {}
        for page_id in self.__page_manager.getPageIds():
            if tokens_only:
                page_chunks = set()
                for token in self.__page_manager.getPage(page_id).tokens:
                    page_chunks.add(token.token)
            else:
                page_chunks = self.__page_manager.getPageChunks(page_id)
            all_chunks.update(page_chunks)
            page_chunks_map[page_id] = page_chunks

        chunks_to_remove = set()
        all_pages_sz = len(self.__page_manager.getPageIds())
        for chunk in all_chunks:
            num_pages_with_chunk = 0
            for page_id in self.__page_manager.getPageIds():
                if chunk in page_chunks_map[page_id]:
                    num_pages_with_chunk += 1
            if tokens_only:
                if num_pages_with_chunk < 2 or num_pages_with_chunk == all_pages_sz:
                    chunks_to_remove.add(chunk)
            else:
                if num_pages_with_chunk < 10 or num_pages_with_chunk == all_pages_sz:
                    chunks_to_remove.add(chunk)

#         print str(len(all_chunks)) + " chunks before filtering"
        all_chunks.difference_update(chunks_to_remove)
        for page_id in self.__page_manager.getPageIds():
            page_chunks_map[page_id].difference_update(chunks_to_remove)

#         print str(len(all_chunks)) + " chunks left after filtering"
#         print str(all_pages_sz) + " pages total"
        return all_chunks, page_chunks_map

    def __test_good_merge(self, potential_cluster_template, test_cluster_template):
        good_merge = False
        (old_visible_count, old_invisible_count) = potential_cluster_template.countTokenInfoInStripes()
        old_clean_slot_count = potential_cluster_template.countCleanSlots()
        print '\t\told_visible = ' + str(old_visible_count)
        print '\t\told_invisible = ' + str(old_invisible_count)
        print '\t\told_clean_slot_count = ' + str(old_clean_slot_count)
        
        (new_visible_count, new_invisible_count) = test_cluster_template.countTokenInfoInStripes()
        new_clean_slot_count = test_cluster_template.countCleanSlots()
        print '\t\tnew_visible = ' + str(new_visible_count)
        print '\t\tnew_invisible = ' + str(new_invisible_count)
        print '\t\tnew_clean_slot_count = ' + str(new_clean_slot_count)
        
        if old_invisible_count == new_invisible_count and new_visible_count <= old_visible_count:
            good_merge = True
        if new_clean_slot_count >= old_clean_slot_count:
            good_merge = True
        
        return good_merge
    
#     def __test_good_merge_template_string(self, potential_cluster_template_string, test_cluster_template_string):
#         good_merge = False
#         test_template = PageManager()
#         test_template.addPage('potential', potential_cluster_template_string, add_special_tokens=False)
#         test_template.addPage('test', test_cluster_template_string, add_special_tokens=False)
#         test_template.learnStripes()
#         print len(test_template._stripes)
#         if len(test_template._stripes) < 2:
#             good_merge = True
#         
#         return good_merge, ' '.join(value['stripe'] for value in test_template._stripes)
# 
#     def __merge_clusters_template_string(self, final_clusters):
#         merged_clusters = {}
#         for final_cluster_rule in sorted(final_clusters, key=lambda x: final_clusters[x]['NAME']):
#             final_cluster_name = final_clusters[final_cluster_rule]['NAME']
#             print 'testing ' + final_cluster_name + " ..."
#             c_i = final_clusters[final_cluster_rule]
#             did_merge = False
#             for rule in merged_clusters:
#                 cluster_name = merged_clusters[rule]['NAME']
#                 print '\tgenerating merged template with ' + cluster_name + " ..."
#                 merged = merged_clusters[rule]
#                 good_merge, merged_template_string = self.__test_good_merge_template_string(c_i['TEMPLATE_STRING'], merged['TEMPLATE_STRING'])
#                 if good_merge:
#                     merged_clusters[rule]['MEMBERS'].extend(c_i['MEMBERS'])
#                     merged_clusters[rule]['TEMPLATE_STRING'] = merged_template_string
#                     did_merge = True
#                     print 'merging ' + final_cluster_name
#                     print '\tinto ' + cluster_name
#                     print '\tnew_template = ' + merged_template_string
#                     break
#                 
#             if not did_merge:
#                 merged_clusters[final_cluster_rule] = c_i
#             
#         return merged_clusters
                
    def __merge_clusters(self, final_clusters):
        merged_clusters = {}
        merged_clusters_pms = {}
        for final_cluster_rule in sorted(final_clusters, key=lambda x: final_clusters[x]['NAME']):
            final_cluster_name = final_clusters[final_cluster_rule]['NAME']
            print 'testing ' + final_cluster_name + " ..."
            c_i = final_clusters[final_cluster_rule]
            if final_cluster_rule in merged_clusters_pms:
                c_i_template = merged_clusters_pms[final_cluster_rule]
            else:
                c_i_template = self.induce_template(c_i['MEMBERS'][:5])
            
            did_merge = False
            for rule in merged_clusters:
                cluster_name = merged_clusters[rule]['NAME']
                print '\tgenerating merged template with ' + cluster_name + " ..."
                merged = merged_clusters[rule]
                
                new_members = c_i['MEMBERS'][:5]
                new_members.extend(merged['MEMBERS'][:5])
                merged_cluster_template = self.induce_template(new_members)
                
                if self.__test_good_merge(c_i_template, merged_cluster_template):
                    ###add c_i to merged - really just adding the pages to it for now
                    merged_clusters[rule]['MEMBERS'].extend(c_i['MEMBERS'])
                    merged_clusters_pms[rule] = merged_cluster_template
                    
                    did_merge = True
                    print 'merging ' + final_cluster_name
                    print '\tinto ' + cluster_name
                    break
                    
            if not did_merge:
                merged_clusters[final_cluster_rule] = c_i
                merged_clusters_pms[final_cluster_rule] = c_i_template
            
        return merged_clusters

    ##############################
    #
    # Clusters pages according to "rules". A "rule" is a list of chunks, and a "chunk" is a section of a Web page
    # that is visible to a user.
    #
    # Inputs:
    #   algorithm: 'rule_size': cluster by the size of rule from long rules to short rules
    #               'coverage' : cluster by the number of pages covered by a rule, small to big (more specific to less)
    #
    # Outputs:
    #   dict[rule] = {
    #       'MEMBERS': list of page ids (Pids from the PageManager),
    #       'ANCHOR': the anchoring chunk for this cluster
    #    }
    #   That is, each entry is a rule and its value is a dict. Note that an anchor is unique
    #   Each rule is a string of chunk_1<BRK>chunk_2<BRK>...<BRK>chunk_N
    #   it's a string to make it an index, but to use it you could break on <BRK>
    #  which you can get from the method get_chunk_separator()
    #
    ##############################
    def do_truffle_shuffle(self, algorithm='coverage', tokens_only=False):
        all_chunks, page_chunks_map = self.prep_truffles_to_shuffle(tokens_only)
        chunk_counts = {}
        seen_rules = []
        rule_anchors = {}
        for chunk in all_chunks:
            pages_with_chunk = []
            for page_id in self.__page_manager.getPageIds():
                if chunk in page_chunks_map[page_id]:
                    pages_with_chunk.append(page_id)
            other_chunks = set()
            other_chunks.update(page_chunks_map[pages_with_chunk[0]])
            for page_id in pages_with_chunk:
                other_chunks.intersection_update(page_chunks_map[page_id])

            # now, find all the guys that have all of those chunks...
            if len(other_chunks) > 1: # one token is not enough, enforce that there are at least 2...
                rule = self.__chunkBreakSeparator.join(other_chunks)
                if rule not in seen_rules:
                    chunk_counts[rule] = pages_with_chunk
                    rule_anchors[rule] = chunk
                    
        if algorithm == 'coverage':
            counts = dict([(rule, len(chunk_counts[rule])) for rule in chunk_counts])
        else:
            # count by the size of the rule, but prefer longer,
            # so make it negative so we don't need to change sorted() call below (e.g., make rules negative
            # so that sorted small to large actually gives us longer rules (more negative) to shorter (less neg)
            counts = dict([(rule, -len(rule.split(self.__chunkBreakSeparator))) for rule in chunk_counts])

        inverted = {}
        for rl in counts:
            sz = counts[rl]
            if sz not in inverted:
                inverted[sz] = []
            inverted[sz].append(rl)
        final_clusters = {}
        already_clustered = []
        for size in sorted(inverted.keys()):
            rules = inverted[size]
            for rule in rules:
                pids = [p for p in chunk_counts[rule] if p not in already_clustered]
                if len(pids) > 1:
                    already_clustered.extend(pids)
                    final_clusters[rule] = {
                        'MEMBERS': pids,
                        'ANCHOR': rule_anchors[rule]
                    }
        
#         clusterCount = 1
#         for rule in sorted(final_clusters, key=lambda x: len(final_clusters[x]['MEMBERS']), reverse=True):
#             
#             final_clusters[rule]['NAME'] = 'cluster' + format(clusterCount, '03')
#             template = self.induce_template(final_clusters[rule]['MEMBERS'])
#             template.learnStripes()
#             final_clusters[rule]['TEMPLATE_STRING'] = ' '.join(value['stripe'] for value in template._stripes)
#             clusterCount += 1
# 
#         return self.__merge_clusters(final_clusters)
        return final_clusters

# look at the coverage of the strips (# of chars that show up in all slots vs all stripes). The stripes should cover a lot of the page
# huge slots = bad sign
# invisible stuff should be mostly in the stripes. Other than visible stuff in page, how much of rest is covered in a stripe?

# how can we predict if a cluster is homogenous?