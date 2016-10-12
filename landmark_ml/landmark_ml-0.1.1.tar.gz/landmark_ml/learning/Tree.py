from landmark_ml.learning.TreeNode import TreeNode
import re

class Tree:

    def __init__(self):
        self.__nodes = {}
        self.__min_occurrences = 5.0
        self.__tree = []
        self.__path_delimeter = "<BRK>"

    def getPathDelimeter(self):
        return self.__path_delimeter

    def getMinOccurrences(self):
        return self.__min_occurrences

    def setMinOccurrences(self, min_occurences):
        self.__min_occurrences = min_occurences

    def add_node_set(self, nodes, meta_data):
        for i in range(len(nodes)):
            depth = i
            parent = None
            if i > 0:
                parent = nodes[i-1]
            path_nodes = nodes[:i]
            path_nodes.reverse()
            path_to_node = self.__path_delimeter.join(path_nodes)
            self.add_node(nodes[i], depth, meta_data, path_to_node=path_to_node, parent=parent)

    def add_node(self, identifier, depth, meta_data, path_to_node=None, parent=None):
        if depth not in self.__nodes:
            self.__nodes[depth] = {}

        if identifier not in self.__nodes[depth]:
            nd = TreeNode(identifier, parent, path_to_node)
            nd.updateMetaData(meta_data)
            self.__nodes[depth][identifier] = [nd]
        else:
            # make sure we have the right one!
            found = None
            for nd_add in self.__nodes[depth][identifier]:
                if nd_add.getPath() == path_to_node:
                    found = nd_add
                    break
            if found is not None:
                found.updateMetaData(meta_data)
            else:
                nd = TreeNode(identifier, parent, path_to_node)
                nd.updateMetaData(meta_data)
                self.__nodes[depth][identifier].append(nd)

        for n in self.__nodes[depth][identifier]:
            if identifier.find("rb_loopadlisting_data") > -1:
                print "== %d %s ==" % (depth, identifier)
                print n.getPath()
                print str(n)

        if parent is not None:
            parent_path = self.__path_delimeter.join(path_to_node.split(self.__path_delimeter)[:-1])
            for parent_node in self.__nodes[depth-1][parent]:
                if parent_node.getPath() == parent_path:
                    parent_node.addChild(identifier)

    def valid_paths(self):  # get the valid paths, along with their visible texts...
        # first, get rid of the nodes that account for very little...
        self.prune()

        # now, find all the leaves. Since each node contains it's own paths, we are fine.
        valid = {}
        for depth in self.__nodes:
            for identifier in self.__nodes[depth]:
                for node in self.__nodes[depth][identifier]:
                    if identifier.find("rb_loopadlisting_data") > -1:
                        print "%d %s" % (depth, identifier)
                        md = node.getMetaData()
                        for n in md:
                            if n['page_id'] == 'tmp1.html':
                                print '>>>> %d %s' % (n['first_vis_token_loc'], n['visible_text'])
                        #print str(node.getMetaData())

                    if len(node.getChildren()) == 0:
                        if len(node.getMetaData()) >= self.__min_occurrences:
                            valid[node.getPath()+self.__path_delimeter+identifier] = node.getMetaData()
        return valid

    def prune(self):
        pruners = []
        # find the possible nodes to prune: those that don't occur enough
        for depth in self.__nodes:
            for identifier in self.__nodes[depth]:
                for node in self.__nodes[depth][identifier]:
                    children = node.getChildren()
                    remove_child = []
                    for child in children:
                        if children[child] < self.__min_occurrences:
                            #print "PRUNING: %s (%d)" % ( node.getPath()+self.__path_delimeter+child, children[child])
                            #print str(node)
                            pruners.append((depth+1, child, node.getPath()+self.__path_delimeter+child))
                            remove_child.append(child)
                    for child in remove_child:
                        del children[child]

        # now we do the pruning (since we can't remove as we iterate above)
        for (depth, id, path) in pruners:
            pot_nodes = self.__nodes[depth][id]
            del_idx = 0
            for i in range(len(pot_nodes)):
                nd = pot_nodes[i]
                if nd.getPath() == path:
                    del_idx = i
                    break
            #print "REMOVE: %d %s %s : %d" % (depth, id, path, del_idx)
            del self.__nodes[depth][id][del_idx]

    def display(self, identifier, depth=0):
        for depth in self.__nodes:
            for identifier in self.__nodes[depth]:
                for nd in self.__nodes[depth][identifier]:
                    print depth*"\t"+str(nd)



    def learn_list_rules(self, markup_by_page, page_mgr):
        from landmark_ml.learning import PageManager

        page_mgr.learnStripes(markups=markup_by_page)
        rules = page_mgr.learnRulesFromMarkup(markup_by_page)

        # now, for each markup rule, learn a little page manager
        sublist_page_managers = {}
        for page in markup_by_page:
            for rule_name in markup_by_page[page]:
                if rule_name not in sublist_page_managers:
                    sublist_page_managers[rule_name] = PageManager()
                for rid in range(len(markup_by_page[page][rule_name]['sequence'])):
                    row = markup_by_page[page][rule_name]['sequence'][rid]
                    sublist_page_managers[rule_name].addPage(page + "html%d" % rid, row['extract'])

        sublist_sub_rules = {}
        for sublist in sublist_page_managers:
            sublist_page_managers[sublist].learnStripes()
            sub_rules = sublist_page_managers[sublist].learnAllRules()
            print '====== SUB RULES ====='
            print sub_rules.toJson()
            for sub_rule in sub_rules.rules:
                sub_rule.removehtml = True
            sublist_sub_rules[sublist] = sub_rules  # This should match a rule name in the rules...

        count = 1
        for rule in rules.rules:
            print "== RULE INFO =="
            print str(rule.name)
            rule.set_sub_rules(sublist_sub_rules[rule.name])
            list_name = '_div_list' + format(count, '04')
            for page_id in markup_by_page:
                if rule.name in markup_by_page[page_id]:
                    markup_by_page[page_id][list_name] = markup_by_page[page_id].pop(rule.name)
            rule.name = list_name
            count += 1
            print rule.toJson()
            print "==============="

        print rules.toJson()
        return rules

if __name__ == '__main__':

    tree = Tree()

    import codecs
    with codecs.open('tmp.html', "r", "utf-8") as myfile:
        page_str = myfile.read().encode('utf-8')

    with codecs.open('tmp2.html', "r", "utf-8") as myfile:
        page_str2 = myfile.read().encode('utf-8')

    from landmark_ml.learning.TreeListLearner import TreeListLearner
    (paths, pg_mgr) = TreeListLearner.learn_lists({'tmp1.html': page_str, 'tmp2.html': page_str2}, filter_tags_by='div')

    markup_by_page = TreeListLearner.create_row_markups(paths, pg_mgr)

    import json
    print "=== MARKUP ==="
    print json.dumps(markup_by_page, sort_keys=True, indent=2, separators=(',', ': '))

    print "== learn sub rules =="
    rules = tree.learn_list_rules(markup_by_page, pg_mgr)

    print "== testing rules page 1 =="
    extraction_list = rules.extract(page_str)

    # from extraction.Landmark import flattenResult
    print json.dumps(extraction_list, sort_keys=True, indent=2, separators=(',', ': '))

    print "== testing rules page 2 =="
    extraction_list = rules.extract(page_str2)

    # from extraction.Landmark import flattenResult
    print json.dumps(extraction_list, sort_keys=True, indent=2, separators=(',', ': '))
