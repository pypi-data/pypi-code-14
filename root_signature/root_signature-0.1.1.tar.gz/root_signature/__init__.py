class RootFiles:
    def dirFiles(self, directory, n_files = None): 
        ROOT.gSystem.Load(root_lib)
        t = ROOT.TRegexp(".*root")
        l = ROOT.mlTTreeLoop()
        l.disableQiwiAggInterface()
        directory = directory
        l.AddFilesRecursively(directory, t)
        return l
        
    def load(self, dir, feature_list = []):
        l = self.dirFiles(directory = dir)
        if feature_list != []:
            ok = l.UncompressReady((';').join(feature_list))
            if ok == True:
                return l
            else:
                print('Check your root files!')
        else:
            ok = l.UncompressReady()
            if ok == True:
                return l
            else:
                print('Check your root files!')

class Signature:
    #l.LoopStart()
    def get_header(self, l):
        header = l.GetHeader().split(';')
        header.extend(l.GetFixedHeader().split(';')) 
        #header = list(filter(None, header))
        return header
    
    def get_signature(self, l):    
        while l.UncompressNext():
                signature = l.GetAttributes().split(';')
                fixed_attributes = l.GetFixedAttributes().split(';')
                signature.extend(fixed_attributes)
                #signature = list(filter(None, signature))
                yield signature
    
    def write_to_file(self, file_name, l):
        l.LoopStart()
        signature = self.get_signature(l)
        header = self.get_header(l)     
        with open(file_name, "a") as f:
            f.write(','.join([item  for item in header]) + '\n')
            try:
                while True:
                    temp_s = next(signature)
                    f.write(','.join([item  for item in temp_s]) + '\n')
            except StopIteration:
                print('Done!')
    def get_popularity(self, l, n_features = None):
        l.LoopStart()
        temp_p = l.ListAttributesByPopularity()
        popularity = list(filter(lambda x: x not in ['\n', ''], temp_p.split('|')))
        popularity = list(map(lambda x: x.replace(' ', ''), popularity))
        popularity.remove('attribute')
        popularity.remove('popularity')
        return popularity[0:2*n_features:2]
