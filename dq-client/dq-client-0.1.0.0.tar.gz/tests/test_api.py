from time import sleep

from dq import DQClient, JobConfig

JOB_TEMPLATE = {
    "job_name": "marcin 123",
    "input_format": {
        "field_separator": ",",
        "text_delimiter": "",
        "header": 1
    },
    "input_columns": [{
        "no": 0,
        "name": "Name",
        "function": "KOD_POCZTOWY"
    }, {
        "no": 1,
        "name": "Code",
        "function": "MIEJSCOWOSC"
    }, {
        "no": 2,
        "name": "Default City",
        "function": "ULICA_NUMER_DOMU_I_MIESZKANIA"
    }, {
        "no": 3,
        "name": "Default postcode",
        "function": "PRZEPISZ"
    }, {
        "no": 4,
        "name": "Country zone",
        "function": "PRZEPISZ"
    }],
    "extend": {
        "teryt": 0,
        "gus": 0,
        "geocode": 0,
        "building_info": 0,
        "diagnostic": 1,
        "area_characteristic": 0
    }
}

PLAY_JOB_TEMPLATE = {
    "job_name": "marcin 123",
    "input_format": {
        "format": "csv",
        "field_separator": ";",
        "text_delimiter": "\"",
        "code_page": "utf-8",
        "header": 1
    },
    "input_columns": [
        {"no": 0, "name": "id", "function": "PRZEPISZ"},
        {"no": 1, "name": "request", "function": "CALY_ADRES"}
    ],
    "extend": {
        "teryt": 0,
        "gus": 1,
        "geocode": 1,
        "building_info": 0,
        "diagnostic": 1,
        "area_characteristic": 0
    }
}

PLAY_INPUT_DATA = """"ID";"REQUEST"
6876;"34-404, PYZÓWKA, PODHALAŃSKA 100"
"""

INPUT_FILE = """
id, adres,test1,test2,test3,test4,test5,test6
1, 222 bbb,aaaa,bbbb,cccc,dddd,eeeee,ffffff
2, 222 bbb,aaaa,bbbb,cccc,dddd,eeeee,ffffff
3, 222 bbb,aaaa,bbbb,cccc,dddd,eeeee,ffffff
4, 222 bbb,aaaa,bbbb,cccc,dddd,eeeee,ffffff
5, 222 bbb,aaaa,bbbb,cccc,dddd,eeeee,ffffff
6, 222 bbb,aaaa,bbbb,cccc,dddd,eeeee,ffffff
"""


def main():
    dq = DQClient('https://app.dataquality.pl', user='test2@3e.pl', token='imjn8faed2g8bg1xy0sc06wbc7qhewqvevf16z01')

    # dq.list_jobs()
    # print(dq.job_status('408b7a3b-302e-4ecd-9363-11a4c36db7ff'))
    # print(dq.job_result('408b7a3b-302e-4ecd-9363-11a4c36db7ff'))
    # dq.job_result_data('7750b6fc-74bb-4072-892c-81afda79e330')
    print(dq.account_status())
    print(dq.list_jobs())
    print(dq.job_report('2dfafd80-7986-42d1-96be-06260aa32b6f'))
    print(dq.job_state('3f14e25e-9f6d-41ff-a4cb-942743a37b73'))
    print(dq.job_report('3f14e25e-9f6d-41ff-a4cb-942743a37b73'))

    #

    # usuwanie, stopowanie i pobieranie wyników nieistniejącego joba
    # print dq.delete_job('7750b6fc-74bb-4072-892c-81afda79e331')
    # print dq.stop_job('7750b6fc-74bb-4072-892c-81afda79e331')
    # print dq.job_result('7750b6fc-74bb-4072-892c-81afda79e331')


    # tworzenie joba


    # res_method, res_code, res_content = dq.submit_job(JOB_TEMPLATE, input_data=INPUT_FILE)
    # res_method, res_code, res_content = dq.submit_job(JOB_TEMPLATE, input_data=INPUT_FILE)
    # res_method, res_code, res_content = dq.submit_job(JOB_TEMPLATE, input_file='samples/other_data0.csv')


    # resp = dq.submit_job(PLAY_JOB_TEMPLATE, input_data=PLAY_INPUT_DATA)
    # dq.submit_job(JOB_TEMPLATE, input_file='samples/telco_data2.csv')
    # print(resp)

    jobs = []

    for i in range(5):
        job_config = JobConfig('job {}'.format(i))
        job_config.input_format(field_separator=";", text_delimiter="\"", has_header=True)
        job_config.input_column(0, name='id', function='PRZEPISZ')
        job_config.input_column(1, name='request', function='CALY_ADRES')
        job_config.extend(gus=True, geocode=True, diagnostic=True)
        job = dq.submit_job(job_config, input_file='samples/telco_data2.csv',
                            input_file_encoding='windows-1250')
        print(job)

        print(dq.job_state(job.id))
        print(dq.job_report(job.id))

        jobs.append(job)

        if job is None:
            print('something went wrong')
            return
        else:
            print('Job created with id: %s' % job.id)
            # sleep(0.01)

            # zwiększyć czas

    for job in jobs:
        print('checking job {}'.format(job.id))
        for x in range(0, 100):
            state = dq.job_state(job.id)
            if state == 'FINISHED':
                print('finished jobid: {}'.format(job.id))
                break
            print('state %s: %s' % (x, state))
            sleep(5.0)

        print('Getting job results ...')
        print(dq.job_report(job.id))
        dq.job_results(job.id, 'ouput.csv')


if __name__ == '__main__':
    main()
