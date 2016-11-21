import sys
import numpy as np
import qlda.per_vb as per_vb
import csv
"""
    Read all documents in the file and stores terms and counts in lists.
"""


def read_data(filename):
    wordids = list()
    wordcts = list()
    fp = open(filename, 'r')
    while True:
        line = fp.readline()
        # check end of file
        if len(line) < 1:
            break
        terms = line.split()
        doc_length = int(terms[0])
        ids = np.zeros(doc_length, dtype=np.int32)
        cts = np.zeros(doc_length, dtype=np.int32)
        for j in range(1, doc_length + 1):
            term_count = terms[j].split(':')
            ids[j - 1] = int(term_count[0])
            cts[j - 1] = int(term_count[1])
        wordids.append(ids)
        wordcts.append(cts)
    fp.close()
    return wordids, wordcts


# read mini batch
def read_minibatch_list_frequencies(fp, batch_size):
    wordids = list()
    wordcts = list()
    for i in range(batch_size):
        line = fp.readline()
        # check end of file
        if len(line) < 5:
            break
        terms = line.split()
        doc_length = int(terms[0])
        ids = np.zeros(doc_length, dtype=np.int32)
        cts = np.zeros(doc_length, dtype=np.int32)
        for j in range(1, doc_length + 1):
            term_count = terms[j].split(':')
            ids[j - 1] = int(term_count[0])
            cts[j - 1] = int(term_count[1])
        wordids.append(ids)
        wordcts.append(cts)
    return wordids, wordcts


"""
    Read data for computing perplexities.
"""


def read_data_for_perpl(test_data_folder):
    filename_part1 = '%s/data_test_part_1.txt' % (test_data_folder)
    filename_part2 = '%s/data_test_part_2.txt' % (test_data_folder)
    (wordids_1, wordcts_1) = read_data(filename_part1)
    (wordids_2, wordcts_2) = read_data(filename_part2)
    data_test = list()
    data_test.append(wordids_1)
    data_test.append(wordcts_1)
    data_test.append(wordids_2)
    data_test.append(wordcts_2)
    return data_test


def read_train_data_for_perpl(train_data_folder):
    filename_part1 = '%s/data_train_part_1.txt' % (train_data_folder)
    filename_part2 = '%s/data_train_part_2.txt' % (train_data_folder)
    (wordids_1, wordcts_1) = read_data(filename_part1)
    (wordids_2, wordcts_2) = read_data(filename_part2)
    data_test = list()
    data_test.append(wordids_1)
    data_test.append(wordcts_1)
    data_test.append(wordids_2)
    data_test.append(wordcts_2)
    return data_test


def read_setting(file_name):
    f = open(file_name, 'r')
    settings = f.readlines()
    f.close()
    sets = list()
    vals = list()
    for i in range(len(settings)):
        # print'%s\n'%(settings[i])
        if settings[i][0] == '#':
            continue
        set_val = settings[i].split(':')
        sets.append(set_val[0])
        vals.append(float(set_val[1]))
    ddict = dict(zip(sets, vals))
    ddict['num_terms'] = int(ddict['num_terms'])
    ddict['num_topics'] = int(ddict['num_topics'])
    ddict['iter_train'] = int(ddict['iter_train'])
    ddict['iter_infer'] = int(ddict['iter_infer'])
    ddict['batch_size'] = int(ddict['batch_size'])
    return ddict


# --------------------------------------------------------------------------------
"""
    Compute document sparsity.
"""


def compute_sparsity(doc_tp, batch_size, num_topics, _type):
    sparsity = np.zeros(batch_size, dtype=np.float)
    if _type == 'z':
        for d in range(batch_size):
            N_z = np.zeros(num_topics, dtype=np.int)
            N = len(doc_tp[d])
            for i in range(N):
                N_z[doc_tp[d][i]] += 1
            sparsity[d] = len(np.where(N_z != 0)[0])

    else:
        for d in range(batch_size):
            sparsity[d] = len(np.where(doc_tp[d] > 1e-10)[0])
        sparsity /= num_topics

    return np.mean(sparsity)


"""
    Compute perplexities, employing Variational Bayes.
"""


def compute_perplexities_vb(beta, alpha, eta, max_iter, data_test):
    vb = per_vb.VB(beta, alpha, eta, max_iter)
    LD2 = vb.compute_perplexity(data_test)
    return LD2


"""
    Create list of top words of topics.
"""


def list_top(beta, tops):
    min_float = -sys.float_info.max
    num_tops = beta.shape[0]
    list_tops = list()
    for k in range(num_tops):
        top = list()
        arr = np.array(beta[k, :], copy=True)
        for t in range(tops):
            index = arr.argmax()
            top.append(index)
            arr[index] = min_float
        list_tops.append(top)
    return list_tops


# --------------------------------------------------------------------------------
def write_topics(beta, file_name):
    num_terms = beta.shape[1]
    num_topics = beta.shape[0]
    f = open(file_name, 'w')
    for k in range(num_topics):
        # f.write('topic ' + str(k) + ': ')
        for i in range(num_terms - 1):
            f.write('%.10f ' % (beta[k][i]))
        f.write('%.10f\n' % (beta[k][num_terms - 1]))
    f.close()


def write_perplexities(test_LD2, file_name, i):
    with open(file_name, 'a') as csvfile:
        writer = csv.writer(csvfile, quotechar='\t', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([i, test_LD2])


def write_time(i, j, time_e, time_m, file_name):
    f = open(file_name, 'a')
    f.write('tloop_%d_iloop_%d, %f, %f, %f,\n' % (i, j, time_e, time_m, time_e + time_m))
    f.close()


def write_loop(i, j, file_name):
    f = open(file_name, 'w')
    f.write('%d, %d' % (i, j))
    f.close()


def write_file(i, j, beta, time_e, time_m, theta, sparsity, test_LD2, train_LDA2, list_tops, tops, model_folder):
    # per_file_name = '%s/perplexities_%d.csv' % (model_folder, i)
    per_file_name = '%s/perplexities.csv' % model_folder
    time_file_name = '%s/time_%d.csv' % (model_folder, i)
    loop_file_name = '%s/loops.csv' % model_folder
    # write perplexities
    write_perplexities(test_LD2, train_LDA2, per_file_name, i)
    # write time
    write_time(i, j, time_e, time_m, time_file_name)
    # write loop
    write_loop(i, j, loop_file_name)


def write_setting(ddict, file_name):
    keys = list(ddict.keys())
    vals = list(ddict.values())
    f = open(file_name, 'w')
    for i in range(len(keys)):
        f.write('%s: %f\n' % (keys[i], vals[i]))
    f.close()


# --------------------------------------------------------------------------------
# my: read dictionary
def read_dictionary(file_name):
    dict = {}
    with open(file_name, encoding='utf8') as file:
        for line in file:
            item = line.split(':')
            dict[item[0]] = item[1].replace('\n', '')
    return dict


def read_dictionary2(file_name):
    dictionary = {}
    i = 0
    with open(file_name, encoding='utf8') as f:
        for line in f:
            dictionary[i] = line.replace('\n', '')
            i += 1
    return dictionary


# my: show topic
def show_topics(path_file_beta, dictionary, num_topic=10):
    # print(dictionary)
    num_term = len(dictionary)
    with open(path_file_beta, 'r') as f:
        for i in range(num_topic):
            line = f.readline().split()
            item = {}
            for j in range(len(line)):
                if j >= num_term:
                    break
                item[line[j]] = dictionary[str(j)]
                # item[line[j]] = dictionary[j]
            a = sorted(zip(item.keys(), item.values()), reverse=True)[:100]
            print('topic ', i)
            for w, t in a:
                print(w, ': ', t)


def write_topics2(path_file_beta, path_out, dictionary, num_topic=10):
    # print(dictionary)
    num_term = len(dictionary)
    file_topic_out = open(path_out, 'w', encoding='utf8')
    with open(path_file_beta, 'r') as f:
        for i in range(num_topic):
            line = f.readline().split()
            # print(len(line))
            item = {}
            for j in range(len(line)):
                if j >= num_term:
                    break
                item[line[j]] = dictionary[str(j)]
                # item[line[j]] = dictionary[j]
            a = sorted(zip(item.keys(), item.values()), reverse=True)[:100]
            file_topic_out.write('topic ' + str(i) + '\n: ')
            for w, t in a:
                file_topic_out.write('\t' + str(w) + ': ' + str(t) + '\n ')


def read_file_beta(file_keyword):
    # print('a' in dict1)
    out = open('abc.txt', 'w', encoding='utf8')
    with open(file_keyword, encoding='utf8') as file:
        for topic in file:
            topic = topic.replace('\n', '')
            if topic.find('#') != 0:
                for kw in topic.split(':')[2:]:
                    if kw != '':
                        out.write(kw + ',')
                out.write('\n')
    out.close()


def init_beta(file_name, file_dict, num_topics, num_terms, eta):
    # dict1 = read_dictionary2(file_dict)
    dict1 = read_dictionary(file_dict)
    dict1 = dict(zip(dict1.values(), dict1.keys()))
    topics = {}

    i = 0
    with open(file_name, encoding='utf8') as file:
        for topic in file:
            kws = topic.split(',')
            kws_id = list()
            for kw in kws:
                if kw in dict1:
                    kws_id.append(int(dict1[kw]))
            topics[i] = kws_id
            i += 1
    # print(topics)
    define_kws = {}
    for i in topics:
        for kw in topics[i]:
            if define_kws.get(kw) is None:
                list_topics = list()
            else:
                list_topics = define_kws.get(kw)
            if i not in list_topics:
                list_topics.append(i)
            define_kws[kw] = list_topics

    # print(define_kws)
    sstats = np.random.gamma(100., 1. / 100., (num_topics, num_terms))
    for wid, t in define_kws.items():
        sstats[:, wid] = np.random.gamma(0.1, 0.05, num_topics)

    for wid, topics in define_kws.items():
        score = 10 * num_topics
        if len(topics) > 1:
            score = 4 * num_topics
        sstats[topics, wid] = score

    m_lambda = eta + sstats
    beta_sum = m_lambda.sum(axis=1)
    beta = m_lambda / beta_sum[:, np.newaxis]
    # print(beta)

    for i in beta:
        print(i.max())

    return beta


def create_define_topic(file_name):
    define_kws = {}
    i = 0
    with open(file_name, encoding='utf8') as file:
        for topic in file:
            kws = topic.split(',')
            for kw in kws:
                if define_kws.get(kw) is None:
                    list_topics = list()
                else:
                    list_topics = define_kws.get(kw)
                if i not in list_topics:
                    list_topics.append(i)
                define_kws[kw] = list_topics
            i += 1
    return define_kws


# read memory usage
# def memory_usage_ps():
#     out = subprocess.Popen(['ps', 'v', '-p', str(os.getpid())],
#     stdout=subprocess.PIPE).communicate()[0].split(b'\n')
#     vsz_index = out[0].split().index(b'RSS')
#     mem = float(out[1].split()[vsz_index])
#     return mem