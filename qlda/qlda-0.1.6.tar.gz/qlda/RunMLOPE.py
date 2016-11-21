import qlda.utilities as utilities
import qlda.MLOPE as MLOPE
import time


class RunMLOPE:
    def __init__(self, train_file, settings, model_folder, test_data, path_dictionary):
        self.train_file = train_file
        self.settings = settings
        self.model_folder = model_folder
        self.test_data = test_data
        self.path_dictionary = path_dictionary

    def run(self):
        # Initialize the algorithm
        print('initialize the algorithm ...')
        ml_ope = MLOPE(self.settings['num_terms'], self.settings['num_topics'], self.settings['alpha'],
                       self.settings['tau0'], self.settings['kappa'], self.settings['iter_infer'])

        # Start
        print('-->START<--')
        i = 0
        time_start = time.time()
        while i < self.settings['iter_train']:
            i += 1
            print('\n***iter_train:%d***\n' % (i))
            datafp = open(self.train_file, 'r')
            j = 0
            while True:
                j += 1
                (wordids, wordcts) = utilities.read_minibatch_list_frequencies(datafp, self.settings['batch_size'])
                # Stop condition
                if len(wordids) == 0:
                    break

                print('---num_minibatch:%d---' % (j))
                ml_ope.static_online(wordids, wordcts)

            datafp.close()

            # write perplexity
            print('compute perplexity')
            test_LD2 = utilities.compute_perplexities_vb(ml_ope.beta, self.settings['alpha'], self.settings['eta'],
                                                    self.settings['iter_infer'], self.test_data)
            file_name_per = '%s/perplexities.csv' % self.model_folder
            utilities.write_perplexities(test_LD2, file_name_per, i)

        # write settings
        print('write setting ...')
        file_name_setting = '%s/setting.txt' % self.model_folder
        utilities.write_setting(self.settings, file_name_setting)

        # write final model to file
        print('write model ...')
        file_name_beta = '%s/beta_final.dat' % self.model_folder
        utilities.write_topics(ml_ope.beta, file_name_beta)
        time_end = time.time()

        # write topic
        file_name_topic = '%s/topic.txt' % self.model_folder
        dictionary = utilities.read_dictionary(self.path_dictionary)
        utilities.write_topics2(file_name_beta, file_name_topic, dictionary, num_topic=self.settings['num_topics'])
        # Finish
        print('-------------------------DONE-------------------------', (time_end - time_start))
