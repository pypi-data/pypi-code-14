def process(input_file, output_file, demographers=None):
    import logging, json
    from demographer import process_tweet
    
    logging.info('Reading from %s' % input_file)
    logging.info('Writing to %s' % output_file)
    with open(input_file) as input, open(output_file, 'w') as writer:
        for line in input:
            if len(line.strip()) == 0:
                writer.write(line)
                continue
            
            tweet = json.loads(line)
            result = process_tweet(tweet, demographers)
            tweet['demographics'] = result
            
            writer.write(json.dumps(tweet))
            writer.write('\n')
    
    

def main():
    import argparse
    
    import logging
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='Process a tweets file to add demographic information.')
    parser.add_argument('--input', required=True, help='The path to the tweets file to process.')
    parser.add_argument('--output', required=True, help='The tweets file with added demographic information.')


    args = parser.parse_args()
    
    #from demographer.gender_c import GenderCDemographer
    
    #demographers = [GenderCDemographer()]
    demographers = None
    process(args.input, args.output, demographers)
    
    logging.info('Done')


if __name__ == '__main__':
    main()