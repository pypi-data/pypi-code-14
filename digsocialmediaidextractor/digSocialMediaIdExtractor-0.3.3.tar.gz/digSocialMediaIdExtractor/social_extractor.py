from digDictionaryExtractor.populate_trie import populate_trie
TWITTER = 'twitter'
INSTAGRAM = 'instagram'
FACEBOOK = 'facebook'
WECHAT = 'wechat'
WHATSAPP = 'whatsapp'
GOOGLE = 'google'
LINKEDIN = 'linkedin'
LINKDIN = 'linkdin'
SOCIAL_MEDIAS = [TWITTER, INSTAGRAM, FACEBOOK, WECHAT, WHATSAPP, GOOGLE, LINKEDIN, LINKDIN]
class SocialExtractor:
    def __init__(self, list_words_en, list_words_fr, high_recall=True, forward_limit=11):
        self.is_high_recall = high_recall
        self.trie_en = populate_trie(list_words_en)
        self.trie_fr = populate_trie(list_words_fr)
        self.forward_limit = forward_limit

    def check_word_en(self, word):
        return self.trie_en.get(word) is not None

    def check_word_fr(self, word):
        return self.trie_fr.get(word) is not None

    def extract(self, tokens):
        tokens = map(lambda x:x.lower(),tokens)
        handles = dict()
        is_extracted = False
        handle = self.get_handle_after_social_media(tokens, TWITTER)
        if(handle is not None):
            handles['twitter'] = handle
            is_extracted = True

        handle = self.get_handle_after_social_media(tokens, INSTAGRAM)
        if(handle is not None):
            handles['instagram'] = handle
            is_extracted = True

        if(is_extracted):
            return handles
        return None

    def get_handle_after_social_media(self, tokens, social_media=TWITTER):
        handle = None
        #print tokens
        if(social_media in tokens):
            social_media_index = tokens.index(social_media)
            handle_index = social_media_index + 1
            limit = min(social_media_index + self.forward_limit, len(tokens))
            check_dictionary = True
            while(handle_index < limit):
                word_at_index = tokens[handle_index]
                #print "Current Word:"+word_at_index
                if(word_at_index == u"@"):
                    if(handle_index + 1 < limit):
                        return tokens[handle_index+1]
                elif(check_dictionary and is_valid_handle(word_at_index, social_media)):
                    #Word is a potential handle
                    if(word_at_index.isalpha()):
                        check_dictionary = False
                        if(not word_at_index in SOCIAL_MEDIAS and not self.check_word_en(word_at_index)
                            and not self.check_word_fr(word_at_index)):
                            return word_at_index
                handle_index += 1
        return handle

def is_valid_handle(handle, social_media):
    if(social_media == INSTAGRAM):
        #Max 30 chars which are letters, numbers, underscores and periods
        if(len(handle) <= 30):
            handle = handle.replace("_","")
            handle = handle.replace(".","")
            if(handle.isalnum()):
                return True
    if(social_media == TWITTER):
        #Max 15 chars which are letter, numbers, underscores
        if(len(handle) <= 15):
            handle = handle.replace("_","")
            if(handle.isalnum()):
                return True
    return False
