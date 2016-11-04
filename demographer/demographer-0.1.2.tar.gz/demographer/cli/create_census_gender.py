from demographer.gender import create_census_gender_dict

def main():
    import argparse
    
    import logging
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Create a census gender dictionary.')
    parser.add_argument('--census-data-path', required=True, help='The path to the census data.')
    parser.add_argument('--output', required=True, help='Where to store the created census gender dictionary.')


    args = parser.parse_args()
    
    create_census_gender_dict(args.census_data_path, args.output)
    
    import logging
    logging.info('Done')


if __name__ == '__main__':
    main()