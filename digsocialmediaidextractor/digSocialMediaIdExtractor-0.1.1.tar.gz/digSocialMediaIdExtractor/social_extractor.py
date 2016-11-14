from nltk.tokenize import sent_tokenize, word_tokenize
import enchant

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
    def __init__(self, high_recall = True, forward_limit=11):
        self.is_high_recall = high_recall
        self.dictionary_en = enchant.Dict("en_US")
        self.dictionary_fr = enchant.Dict("fr_FR")
        self.forward_limit = forward_limit

    def extract(self, tokens):
        tokens = map(lambda x:x.lower(),tokens)
        #print tokens
        handles = dict()

        handle = self.get_handle_after_social_media(tokens, TWITTER)
        handles['twitter'] = handle
        handle = self.get_handle_after_social_media(tokens, INSTAGRAM)
        handles['instagram'] = handle
        return handles

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
                        if(not word_at_index in SOCIAL_MEDIAS and not self.dictionary_en.check(word_at_index) 
                            and not self.dictionary_fr.check(word_at_index)):
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

def get_word_tokens(text):
    word_tokens = list()
    for s in sent_tokenize(text):
        word_tokens += word_tokenize(s)
    return word_tokens
