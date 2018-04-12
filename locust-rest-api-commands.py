#!/usr/local/bin/python
import requests
import argparse
import os
import time
import datetime

MAIN_RESULTS_FOLDER = './results'


def make_dir(path):
    try: 
        os.mkdir(path)
    except OSError:
        # directory already exists
        pass

def get_and_save_result(base_url, path, folder_path, file_prefix):
    response = requests.get(url=base_url + path)

    if response.status_code == 200:
        with open(folder_path + '/%s.csv' % file_prefix, 'w') as results:
            results.write(response.content)


def get_results(base_url):
    folder_name = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
    results_folder = MAIN_RESULTS_FOLDER + '/%s' % folder_name

    make_dir(MAIN_RESULTS_FOLDER)
    make_dir(results_folder)

    # requests
    get_and_save_result(
        base_url=base_url, 
        path='/stats/requests/csv', 
        folder_path=results_folder, 
        file_prefix='requests_csv')

    # distribution
    get_and_save_result(
        base_url=base_url, 
        path='/stats/distribution/csv', 
        folder_path=results_folder, 
        file_prefix='distribution')


    # requests
    get_and_save_result(
        base_url=base_url, 
        path='/stats/requests', 
        folder_path=results_folder, 
        file_prefix='requests')

    # exceptions
    get_and_save_result(
        base_url=base_url, 
        path='/exceptions/csv', 
        folder_path=results_folder, 
        file_prefix='exceptions')

    # resetting stats
    print (requests.get(url=base_url + '/stats/reset'))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Would you like to run locust tests?')
    parser.add_argument('--action', metavar='N', type=str, nargs='+', help='start/stop/results locust', default='none')
    parser.add_argument('--locust_count', metavar='N', type=int, nargs='+', help='an integer for the locust count', default=[1])
    parser.add_argument('--hatch_rate', metavar='N', type=float, nargs='+', help='an integer for the hatch rate', default=[1])
    parser.add_argument('--locust_url', 
        metavar='N', type=str, nargs='+', help='url point to locust web server', default=['http://localhost:8089'])

    args = parser.parse_args()
    print (args)

    if 'start' in args.action:
        print ('starting locust')
        data = {
            'locust_count': args.locust_count[0],
            'hatch_rate': args.hatch_rate[0]
        }
        print (requests.post(url=args.locust_url + '/swarm', data=data))

    elif 'stop' in args.action:
        print ('stopping locust')
        print (requests.get(url=args.locust_url + '/stop'))
    elif 'results' in args.action:
        print ('attempting to retrive results from locust')
        get_results(args.locust_url[0])
    else:
        parser.print_help() 
