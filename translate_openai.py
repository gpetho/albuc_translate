import openai
import os
import tqdm
import logging
import argparse
import yaml
from transformers import AutoTokenizer

MAX_ATTEMPTS = 3  # Maximum number of attempts to retry a failed generation

def print_context(response, logger, tokenizer):
    logger.info(f"Context: {str(len(response['choices'][0]['text']))}")
    logger.info(tokenizer.decode(response['choices'][0]['text'].encode()))

def main():
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='Generate translations for Latin text')
    parser.add_argument('language', type=str, choices=['ara', 'lat', 'occ', 'ofr'],
                        help='Language to translate from: ara, lat, occ, ofr')
    parser.add_argument('model_key', type=str,
                        help='Key to the model in the YAML file, e.g., gpt-3.5-turbo')
    parser.add_argument('count', type=int, default=10,
                        help='How many translations to generate')
    parser.add_argument('-s', '--start-number', type=int, default=0,
                        help='Starting number for output files')
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

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
        tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    else:
        logging.basicConfig(level=logging.ERROR)

    # Load model ID from YAML configuration
    with open("translate_config.yaml") as f:
        config = yaml.safe_load(f)

    if args.model_key not in config['model']:
        raise ValueError(f"Model key '{args.model_key}' not found in the 'model' section of the config file.")

    model_id = config['model'][args.model_key]['model_id']

    # Load prompts if provided
    first_prompt = ''
    if args.prompt:
        with open(args.prompt) as f:
            first_prompt = f.read()

    turn_prefix = ''
    if args.follow_up:
        with open(args.follow_up) as f:
            turn_prefix = f.read()

    # Load input lines if provided
    lines = []
    if args.input:
        with open(args.input) as f:
            lines = f.readlines()
    else:
        with open(f'{args.language}/all_text.txt') as f:
            lines = f.readlines()    
    print(f"Generating {args.count} translations starting at "
          f"{args.start_number} for {args.language} using {model_id}")

    model_fn = model_id.replace(':', '_').replace('/', '_')

    # Set up output directory
    out_dir = args.output if args.output else f"{args.language}_translations/{model_fn}"
    os.makedirs(out_dir, exist_ok=True)

    for fnum in range(args.start_number, args.count):
        with open(f"{out_dir}/{model_fn}_{fnum}.txt", "w") as outfile:
            context = []
            for line in tqdm.tqdm(lines):
                attempt = 0
                while True:
                    try:
                        if context and len(context) < args.max_ctx:
                            response = client.chat.completions.create(
                                messages = [{"role": "user", "content": turn_prefix + line}],
                                model=model_id,
                            )
                        else:
                            response = client.chat.completions.create(
                                messages = [{"role": "user", "content": first_prompt + line}],
                                model=model_id,
                            )
                    except Exception as e:
                        logger.error(f"OpenAI API error: {e}")
                        if attempt < MAX_ATTEMPTS:
                            attempt += 1
                            logger.info(f"Retrying... {attempt}")
                            continue
                        else:
                            break

                    if response and 'choices' in response and response.choices[0].text.strip():
                        break
                    else:
                        if attempt < MAX_ATTEMPTS:
                            attempt += 1
                            logger.info(f"Retrying... {attempt}")
                        else:
                            break

                if args.verbose:
                    print_context(response, logger=logger, tokenizer=tokenizer)

                if response and 'choices' in response and response.choices[0].text.strip():
                    print(line.strip() + '\t' + response.choices[0].text.strip(), file=outfile)
                    context = []

if __name__ == '__main__':
    main()