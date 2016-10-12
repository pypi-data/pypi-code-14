import re
from landmark_extractor.extraction.Landmark import ItemRule, RuleSet, IterationRule,\
    escape_regex_string
import unicodedata
import PageManager

class Stripes(object):
    '''
    Stripes which are generate from sample pages
    
    TODO look into simple_test boundaries
    '''
    def trim(self, sample_page):
        '''
        This method trims the pages per our alphanumeric "word" boundary
          - It only applies this to ONE page and SHOULD be done to all pages used to
            build the original template.
        '''
        new_stripes = []
        string_index = 0
        for stripe in self._stripes:
            stripe_match = re.search(re.escape(stripe),sample_page[string_index:])
            if stripe_match and stripe[0].isalnum():
                if stripe_match.start() > 0:
                    if sample_page[string_index+stripe_match.start()-1].isalnum():
                        while stripe and stripe[0].isalnum():
                            #now we need to remove the first character of this stripe
                            stripe = stripe[1:]
                            
            if stripe_match and stripe and stripe[-1].isalnum():
                if stripe_match.end() < len(sample_page):
                    if sample_page[string_index+stripe_match.end()].isalnum():
                        while stripe and stripe[-1].isalnum():
                            #now we need to remove the first character of this stripe
                            stripe = stripe[0:-1]
                            
            if stripe_match:
                string_index = string_index + stripe_match.end()
                if stripe:
                    new_stripes.append(stripe)

        self._stripes = new_stripes

    def length(self):
        return len(self._stripes)
    
    def getStripe(self, stripe_id):
        return self._stripes[stripe_id]
    
    def getSlotValues(self, page):
        slotValues = []
        stripe_index = 0
        string_index = 0
        for left_stripe in self._stripes[0:-1]:
            stripe_index = stripe_index + 1
            left_stripe_match = re.search(re.escape(left_stripe),page[string_index:])
            left_stripe_index = left_stripe_match.end()
             
            right_stripe = self._stripes[stripe_index]
            right_stripe_match = re.search(re.escape(right_stripe),page[left_stripe_index+string_index:])
             
            right_stripe_index = right_stripe_match.start() + left_stripe_index
            
            value = page[string_index+left_stripe_index:string_index+right_stripe_index]
            start_index = string_index+left_stripe_index
            stop_index = string_index+right_stripe_index        
            slotValues.append({'extract': value, 'start_index': start_index, 'stop_index': stop_index})
            
            string_index = string_index + right_stripe_index
            
        return slotValues
    
    def getValue(self, page, slot_start, slot_end = -1):
        if slot_end == -1:
            slot_end = slot_start
        
        stripe_index = 0
        string_index = 0
        for left_stripe in self._stripes:
            stripe_index = stripe_index + 1
            left_stripe_match = re.search(re.escape(left_stripe),page[string_index:])
            left_stripe_index = left_stripe_match.end()
            
            if stripe_index < len(self._stripes):
                right_stripe = self._stripes[stripe_index]
                right_stripe_match = re.search(re.escape(right_stripe),page[left_stripe_index+string_index:])
                right_stripe_index = right_stripe_match.start() + left_stripe_index
            else:
                right_stripe_index = len(page)
            
            if stripe_index > slot_start:
                start_index = string_index+left_stripe_index
            if stripe_index > slot_end:
                stop_index = string_index+right_stripe_index
                break;
            string_index = string_index + right_stripe_index
        
        value = page[start_index:stop_index]
        
        return {'extract': value, 'start_index': start_index, 'stop_index': stop_index}

    def whichSlots(self, page, markup_set):
        """
        Returns which slots the markup is part of
        """
        slot_info = {}
        slot_markups = {}
        for markup in markup_set:
            slot_info[markup] = []
            slot_markups[markup] = markup_set[markup]
            
        string_index = 0
        stripe_index = 0
        for left_stripe in self._stripes[0:-1]:
            stripe_index = stripe_index + 1
            left_stripe_match = re.search(re.escape(left_stripe),page[string_index:])
            left_stripe_index = left_stripe_match.end()
             
            right_stripe = self._stripes[stripe_index]
            right_stripe_match = re.search(re.escape(right_stripe),page[left_stripe_index+string_index:])
             
            right_stripe_index = right_stripe_match.start() + left_stripe_index
             
            value = page[string_index+left_stripe_index:string_index+right_stripe_index]
            
            for markup in slot_markups:
                if slot_markups[markup] in value:
                    slot_info[markup].append(stripe_index - 1)
            
            string_index = string_index + right_stripe_index
        
        return slot_info
    
    def cleanStripesWithMarkup(self, page, markups):
        ''' 
        Cleans the stripes based on the markup passed in for this page
         - If markup is across or in any stripe, remove that from the stripe
         - UNLESS the markup can be found in a single stripe elsewhere
        '''
        for markup in markups:
            #FOR NOW WE IGNORE THE indexes... but we should do something with it
            #TODO: Use the indexes 
            indexes = [[m.start(), m.start()+len(markups[markup]['extract'])] for m in re.finditer(re.escape(markups[markup]['extract']), page)]
            if len(indexes) > 0:
                slot_sets = []
                for index_set in indexes:
                    slots = self.__slots_for_markup(page, index_set)
                    if len(slots) == 1:
                        slot_sets = [(slots, index_set)]
                        
                        break;
                    if len(slots) > 0:
                        slot_sets.append( (slots, index_set) )
                
                if len(slot_sets) > 0:
                    #let's find the smallest one
                    size = 0
                    slots = []
                    indexes = []
                    for slot_set, index_set in slot_sets:
                        if len(slot_set) > size:
                            slots = slot_set
                            indexes = index_set
                            size = len(slot_set)
                    
                    #if that is the case, let's remove the stripe(s) in the middle and trim the sides!
                    self.__clean_slots_from_markup(page, indexes, slots)
                    
                else:
                    #this means the markup is in a stripe
                    index_set = indexes[0]
                    string_index = 0
                    stripe_index = 0
                    slots = []
                    for stripe in self._stripes:
                        left_stripe_match = re.search(re.escape(stripe),page[string_index:])
                        stripe_start = string_index+left_stripe_match.start()
                        stripe_end = string_index+left_stripe_match.end()
                        
                        if stripe_start <= index_set[0] and stripe_end >= index_set[1]:
                            #split this stripe
                            new_left_stripe = self._stripes[stripe_index][0:index_set[0]-stripe_start]
                            new_right_stripe = self._stripes[stripe_index][index_set[1]-stripe_start:]
                            self._stripes[stripe_index] = new_left_stripe
                            self._stripes.insert(stripe_index+1, new_right_stripe)
                            break
                        
                        stripe_index = stripe_index + 1
                        string_index = stripe_end
                        
    def learnRulesFromMarkup(self, pages, page_markups):
        #First create a key based markup dictionary instead of page based
        page_ids = list()
        keys = list()
        for page_markup in page_markups:
            page_ids.append(page_markup)
            keys.extend(page_markups[page_markup])
        keys = list(set(keys))
        
        key_based_markup = {}
        for key in keys:
            if key not in key_based_markup:
                key_based_markup[key] = []
            for page_id in page_ids:
                if key in page_markups[page_id]:
                    key_based_markup[key].append({page_id:page_markups[page_id][key]})
        
        rule_set = RuleSet()
        for key in key_based_markup:
            rule = self.__learn_rule_from_markup(pages, key_based_markup[key])
            if rule:
                rule.set_name(key)
                rule_set.add_rule(rule)
            else:
                print 'Unable to learn rule for ' + key
        
#         print '====STRIPES===='
#         for _stripe_ in self._stripes:
#             print '----'
#             print _stripe_
#         
#         print '====PAGES===='
#         for _page_ in pages:
#             print '----'
#             print pages[_page_].getString()
        
        return rule_set
    
    def __test_item_rule(self, begin_regex, end_regex, pages, page_based_markup_list):
        for markup in page_based_markup_list:
            for page in markup:
                page_str = pages[page].getString().replace(PageManager.PAGE_BEGIN, '')
                value = markup[page]['extract']
                if isinstance(value, unicode):
                    value_unicode = value
                else:
                    value_unicode = unicode(value, 'utf-8', 'ignore') 
                value_ascii = unicodedata.normalize('NFKD', value_unicode).encode('ascii', 'ignore')
                
                test_rule = ItemRule('test_rule', begin_regex.replace(PageManager.PAGE_BEGIN, ''), end_regex.replace(PageManager.PAGE_BEGIN, ''))
                
                extract = test_rule.apply(page_str)
                if isinstance(extract['extract'], unicode):
                    extract_unicode = extract['extract']
                    extract_unicode = unicode(str(extract['extract']), 'utf-8', 'ignore')
                else:
                    extract_unicode = unicode(extract['extract'], 'utf-8', 'ignore')
                extract_ascii = unicodedata.normalize('NFKD', extract_unicode).encode('ascii', 'ignore')
                if not extract_ascii.strip().startswith(value_ascii.strip()):
                    print begin_regex.replace(PageManager.PAGE_BEGIN, '')
                    print '-----'
                    print extract_ascii
                    print '-----'
                    print value_ascii
                    print '-----'
#                 if value not in extract_ascii:
                    return None
        return test_rule
    
    def __learn_rule_from_markup(self, pages, page_based_markup_list):
        rule_regex_string = ''
        rule = None
        
        #lets check the first one to build the rule...
        for page in page_based_markup_list[0]:
            page_str = pages[page].getString()
            value = page_based_markup_list[0][page]
            
#             if isinstance(value['extract'], unicode):
#                 value_unicode = value['extract']
#             else:
#                 value_unicode = unicode(value['extract'], 'utf-8', 'ignore')
#             print value_unicode
#             
#             value['extract'] = unicodedata.normalize('NFKD', value_unicode).encode('ascii', 'ignore')
#             print '<BRIAN>'
#             print '<BRIAN>'
#             print value['extract']
            break
        
        indexes = [[m.start(), m.start()+len(value['extract'])] for m in re.finditer(re.escape(value['extract']), page_str)]
        target_slot = -1
        if len(indexes) > 0:
            for index_set in indexes:
                slots = self.__slots_for_markup(page_str, index_set)
                if len(slots) == 1:
                    target_slot = slots[0]
                    break
        
        if target_slot < 0:
            return None
        
        original_slot = target_slot
        #for now make the end regex the next stripe or nothing if it is the last stripe
        end_regex_string = ''
        if original_slot+1 < len(self._stripes):
            end_regex_string = self._stripes[original_slot+1]
        
        while not rule and target_slot >= 0:
            if rule_regex_string:
                rule_regex_string = ".*?" + rule_regex_string
            rule_regex_string = escape_regex_string(self._stripes[target_slot]) + rule_regex_string
            
            rule = self.__test_item_rule(rule_regex_string, escape_regex_string(end_regex_string), pages, page_based_markup_list)
            target_slot = target_slot - 1
        
        #if the rule has a sequence then it is a IterationRule
        from learning.PageManager import PageManager
        if 'sequence' in value:
            sequence_markups = []
            sequence_markups_pages = PageManager()
            sequence_pagemanager = PageManager()
            
            sub_markups = {}
            sub_pagemanager = PageManager()
            
            for index in page_based_markup_list:
                for page_iter in index:
                    page_iter_str = pages[page_iter].getString()
                    sub_page = rule.apply(page_iter_str)
                    value_iter = index[page_iter]
            
                    for item_1 in value_iter['sequence']:
                        sequence_number = item_1['sequence_number']
                        if isinstance(item_1['extract'], unicode):
                            extract_unicode = item_1['extract']
                            extract_unicode = unicode(str(item_1['extract']), 'utf-8', 'ignore')
                        else:
                            extract_unicode = unicode(item_1['extract'], 'utf-8', 'ignore')
                        item_1['extract'] = unicodedata.normalize('NFKD', extract_unicode).encode('ascii', 'ignore')
                        
                        #build the sub_markups and pages as we are looking through the sequence
                        for item in item_1:
                            sub_page_id = page_iter+str(sequence_number)
                            if item not in ['begin_index', 'end_index', 'extract', 'sequence', 'sequence_number']:
                                sub_pagemanager.addPage(sub_page_id, str(item_1['extract']))
                                if sub_page_id not in sub_markups:
                                    sub_markups[sub_page_id] = {}
                                sub_markups[sub_page_id][item] = item_1[item]
                                
                        #find the one after it
                        item_2 = None
                        for item in value_iter['sequence']:
                            if item['sequence_number'] == sequence_number + 1:
                                item_2 = item
                                break;
                        if item_2:
                            item_2['extract'] = unicodedata.normalize('NFKD', item_2['extract']).encode('ascii', 'ignore')
                            
                            text_between = sub_page['extract'][sub_page['extract'].find(item_1['extract'])+len(item_1['extract']):sub_page['extract'].rfind(item_2['extract'])]
#                             text_between = unicodedata.normalize('NFKD', text_between).encode('ascii', 'ignore')
                            sequence_pagemanager.addPage(page_iter+str(sequence_number), text_between)
                            sequence_markups_pages.addPage(page_iter+str(sequence_number), item_1['extract']+text_between+item_2['extract'])
                            sequence_markups.append({page_iter+str(sequence_number): item_1})
            
            sequence_pagemanager.learnStripes()
            iter_rule_regex_string = ''
            iter_rule = None
            target_slot = len(sequence_pagemanager.getSripes())-1
            
            #TODO: I am not creating this rule correctly... for now I am just saying make it
            #all of the stripes together that are between each item and test it.
            for iter_stripe in sequence_pagemanager._stripes._stripes:
                if iter_rule_regex_string:
                    iter_rule_regex_string += ".*?"
                iter_rule_regex_string += escape_regex_string(iter_stripe)
            iter_rule = self.__test_item_rule('', iter_rule_regex_string, sequence_markups_pages._pages, sequence_markups)
#             while not iter_rule:
#                 if iter_rule_regex_string:
#                     iter_rule_regex_string = ".*?" + iter_rule_regex_string
#                 iter_rule_regex_string = Landmark.escape_regex_string(sequence_manager._stripes._stripes[target_slot]) + iter_rule_regex_string
#                 iter_rule = self.__test_item_rule('', iter_rule_regex_string, sequence_markups_pages._pages, sequence_markups)
#                 target_slot = target_slot - 1
            if iter_rule:
                rule = IterationRule('test_rule', rule.begin_regex, rule.end_regex,
                                     iter_rule.end_regex, iter_rule.end_regex, True, True)
                
                if len(sub_pagemanager.getPageIds()) > 1:
                    #only do this if there was an iter_rule
                    sub_pagemanager.learnStripes()
                    sub_rules = sub_pagemanager.learnRulesFromMarkup(sub_markups)
                    rule.set_sub_rules(sub_rules)
        
        #now check if there are any sub_rules to learn
        for item in value:
            if item not in ['begin_index', 'end_index', 'extract', 'sequence', 'sequence_number']:
                #learn the sub_rule then append it to "rule"
                sequence_manager = PageManager()
                sub_page_based_markups_list = []
                for index in page_based_markup_list:
                    for page_id in page_based_markup_list[index]:
                        page_str = pages[page_id].getString()
                        sub_page = rule.apply(page_str)
                        sequence_manager.addPage(sub_page)
                        sub_page_based_markups_list.append({page_str:value[item]})
                sub_rule = self.__learn_rule_from_markup(sequence_manager._pages, sub_page_based_markups_list)
                sub_rule.set_name(item)
                if not rule['sub_rules']:
                    rule['sub_rules'] = []
                rule['sub_rules'].append(sub_rule)
        return rule
        
    def __clean_slots_from_markup(self, page, index_set, slot_set, remove_stripes_inbetween = False):
        if not slot_set:
            return
        
        # Remove all the slots except the first one
        # Essentially merging them
        # BUT only if we were told to do so
        if not remove_stripes_inbetween:
            self._stripes = [i for j, i in enumerate(self._stripes) if j not in slot_set[1:]]
            left_slot = slot_set[0]
            right_slot = left_slot
        else:
            left_slot = slot_set[0]
            right_slot = slot_set[-1]
        
        # Now trim the slot as needed - and also take care of if the slot turns into nothing...
        extract = self.getValue(page, left_slot, right_slot)
        
        if index_set[1] > extract['stop_index']:
            #trim the left side of the right stripe as long as it doesn't remove this stripe
            index_update = index_set[1] - extract['stop_index']
            if index_update < len(self._stripes[right_slot+1]):
                self._stripes[right_slot+1] = self._stripes[right_slot+1][index_update:]
            else:
                #just remove the right stripe == update_slot + 1
                self._stripes = [i for j, i in enumerate(self._stripes) if j != right_slot + 1]
                
        if index_set[0] < extract['start_index']:
            #trim the right side of the left stripe as long as it doesn't remove this stripe
            index_update = extract['start_index'] - index_set[0]
            if index_update < len(self._stripes[left_slot]):
                self._stripes[left_slot] = self._stripes[left_slot][:len(self._stripes[left_slot])-index_update]
            else:
                #just remove the left stripe == update_slot
                self._stripes = [i for j, i in enumerate(self._stripes) if j != left_slot]
    
    def __slots_for_markup(self, page, index_set):
        string_index = 0
        stripe_index = 0
        slots = []
        
        #Find the left slot id
        for left_stripe in self._stripes:
            stripe_index = stripe_index + 1
            left_stripe_match = re.search(re.escape(left_stripe),page[string_index:])
            left_stripe_start = left_stripe_match.start()
            left_stripe_end = left_stripe_match.end()
            
            if stripe_index < len(self._stripes):
                right_stripe = self._stripes[stripe_index]
                right_stripe_match = re.search(re.escape(right_stripe),page[string_index+left_stripe_end:])
                right_stripe_start = left_stripe_end + right_stripe_match.start()
                right_stripe_end = left_stripe_end + right_stripe_match.end()
            else:
                right_stripe_start = right_stripe_end = len(page)
            
            if not slots:
                if string_index+left_stripe_start < index_set[0] and index_set[0] < string_index+right_stripe_end:
                    slots.append(stripe_index - 1)
            else:
                if string_index+right_stripe_end <= index_set[1]+1:
                    slots.append(stripe_index - 1)
                else:
                    return slots
                
            string_index = string_index + right_stripe_start
        return slots

    def __init__(self, stripes):
        self._stripes = stripes

#     def __init__(self, page_template, marker):
#         self._stripes = filter(None, [item.strip() for item in page_template.split(marker)])
        