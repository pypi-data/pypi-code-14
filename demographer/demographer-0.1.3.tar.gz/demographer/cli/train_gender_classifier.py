from demographer.gender import train_gender_classifier

def main():
    import argparse

    import logging
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description='Train a gender classifier Requires an existing census gender dictionary.')
    parser.add_argument('--gender-dict', help='The path to the created gender dictionary.')
    parser.add_argument('--output', required=True, help='Where to store the trained census gender classifier.')


    args = parser.parse_args()
    
    train_gender_classifier(args.output, dictionary_filename=args.gender_dict)
    
    import logging
    logging.info('Done')


if __name__ == '__main__':
    main()