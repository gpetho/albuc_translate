import ollama
import tqdm
import os
import logging
import yaml
import argparse
from transformers import AutoTokenizer

MAX_ATTEMPTS = 3  # Maximum number of attempts to retry a failed generation


def print_context(response, logger, tokenizer):
    logger.info(f"Context: {str(len(response['context']))}")
    logger.info(tokenizer.decode(response['context']))


def main():
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='Generate translations for Latin text')
    parser.add_argument('language', type=str,
                        help='Language to translate from: ara, lat, occ, ofr')
    parser.add_argument('model', type=str,
                        help='Model to use for translation')
    parser.add_argument('count', type=int, default=10,
                        help='How many translations to generate')
    parser.add_argument('-s', '--start-number', type=int, default=0,
                        help='Starting number for output files')
    parser.add_argument('-l', '--start-line', type=int, default=0,
                        help='Starting line of first output file')
    parser.add_argument('-i', '--input', type=str,
                        help='File containing source text to translate')
    parser.add_argument('-o', '--output', type=str,
                        help='Output directory for translations')
    parser.add_argument('-f', '--follow-up', type=str,
                        help='File containing follow-up prompt')
    parser.add_argument('-p', '--prompt', type=str,
                        help='File containing initial prompt')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Print contexts in terminal while translating')
    parser.add_argument('--max_ctx', type=int, default=1000,
                        help='Maximum context length clearing chat history')
    args = parser.parse_args()

    if args.start_number >= args.count:
        raise ValueError('Start number must be less than count')

    if args.language not in ['ara', 'lat', 'occ', 'ofr']:
        raise ValueError('Language must be one of ara, lat, occ, ofr')

    with open("translate_config.yaml") as f:
        config = yaml.safe_load(f)

    if args.model not in config['model']:
        raise ValueError(f"Model {args.model} not in config file")

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
        tokenizer = AutoTokenizer.from_pretrained(config['model'][args.model]['hf'])
    else:
        logging.basicConfig(level=logging.ERROR)

    if args.prompt:
        prompt_file = args.prompt
    else:
        prompt_file = config['prompt'][args.language]
    with open(prompt_file) as f:
        first_prompt = f.read()

    if args.follow_up:
        with open(args.follow_up) as f:
            turn_prefix = f.read()
    else:
        turn_prefix = ''

    if args.input:
        with open(args.input) as f:
            lines = f.readlines()
    else:
        with open(f'{args.language}/all_text.txt') as f:
            lines = f.readlines()

    print(f"Generating {args.count} translations starting at "
          f"{args.start_number} for {args.language} using {args.model}")

    model_fn = args.model.replace(':', '_')

    if args.output:
        out_dir = args.output        
    else:
        out_dir = f"{args.language}_translations/{model_fn}"

    os.makedirs(out_dir, exist_ok=True)

    for fnum in range(args.start_number, args.count):
        if fnum == args.start_number and args.start_line:
            outfile = open(f"{out_dir}/{model_fn}_{fnum}.txt", "a")
        else:
            outfile = open(f"{out_dir}/{model_fn}_{fnum}.txt", "w")
        context = []
        for line in tqdm.tqdm(lines):
            if fnum == args.start_number and args.start_line and lines.index(line) < args.start_line:
                continue
            attempt = 0
            while True:
                if context and len(context) < args.max_ctx:
                    response = ollama.generate(model=args.model,
                                                prompt=turn_prefix + line,
                                                context=context)
                else:
                    response = ollama.generate(model=args.model,
                                                prompt=first_prompt + line)
                if '\n' in response['response']:
                    if attempt < MAX_ATTEMPTS:
                        attempt += 1
                        logger.info(f"Retrying... {attempt}")
                    else:
                        break
                else:
                    break

            if args.verbose:
                print_context(response, logger=logger, tokenizer=tokenizer)

            if '\n' in response['response']:
                print(line.strip() + '\t' + response['response'].split('\n')[0].strip('"'),
                        file=outfile)
                context = []
            else:
                print(line.strip() + '\t' + response['response'].strip('"'),
                        file=outfile)
                context = response.get('context', [])
        outfile.close()


if __name__ == '__main__':
    main()
