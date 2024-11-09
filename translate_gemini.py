from collections import deque
import os
import time
import logging
import argparse
import yaml
import tqdm
import more_itertools
import google.generativeai as genai

MAX_ATTEMPTS = 3  # Maximum number of attempts to retry a failed generation

GEMINI_MODELS = {
    'gemini-1.5-flash-002',
    'gemini-1.5-flash-8b',
    'gemini-1.5-pro-002'
}


class Turn:
    def __init__(self, message):
        self.user = {"role": "user", "parts": message}
        self.reply = None

    def add_reply(self, message):
        self.reply = {"role": "model", "parts": message}

    def to_list(self):
        if self.reply is None:
            return [self.user]
        else:
            return [self.user, self.reply]


class MessageDeque:
    def __init__(self, max_length=5):
        self.message_deque = deque([], max_length)

    def add_turn(self, message):
        self.message_deque.append(Turn(message))

    def add_response(self, response):
        self.message_deque[-1].add_reply(response.text)

    def to_list(self):
        return list(more_itertools.flatten([turn.to_list() for turn in self.message_deque]))


def main():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='Generate English translations for text')
    parser.add_argument('language', type=str, choices=['ara', 'lat', 'occ', 'ofr'],
                        help='Language to translate from: ara, lat, occ, ofr')
    parser.add_argument('model_key', type=str,
                        help='Key to the model in the YAML file, e.g., gemini')
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
    parser.add_argument('-r', '--restrict-length', type=float, default=0,
                        help='Restrict output to a multiple of input tokens')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Print contexts in terminal while translating')
    parser.add_argument('--max_ctx', type=int, default=1000,
                        help='Maximum context length clearing chat history')
    args = parser.parse_args()

    if args.start_number >= args.count:
        raise ValueError('Start number must be less than count')

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    # Load model ID from YAML configuration
    with open("translate_config.yaml") as f:
        config = yaml.safe_load(f)

    if args.model_key not in GEMINI_MODELS:
        raise ValueError(f"'{args.model_key}' is not a Google Gemini model.")

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

    # Load input lines if provided
    lines = []
    if args.input:
        with open(args.input) as f:
            lines = f.readlines()
    else:
        with open(f'{args.language}/all_text.txt') as f:
            lines = f.readlines()    
    print(f"Generating {args.count} translations starting at "
          f"{args.start_number} for {args.language} using {args.model_key}")

    gemini = genai.GenerativeModel(args.model_key)

    # Set up output directory
    out_dir = args.output if args.output else f"{args.language}_translations/{args.model_key}"
    os.makedirs(out_dir, exist_ok=True)

    for fnum in range(args.start_number, args.count):
        if fnum == args.start_number and args.start_line:
            open_mode = "a"
        else:
            open_mode = "w"

        with open(f"{out_dir}/gemini_{fnum}.txt", open_mode) as outfile:
            turns = MessageDeque(max_length=5)

            for i, line in tqdm.tqdm(enumerate(lines), total=len(lines)):
                if fnum == args.start_number and args.start_line and i < args.start_line:
                    continue
                attempt = 0

                token_count = gemini.count_tokens(line.strip())
                if args.restrict_length:
                    generation_config = {
                        "max_output_tokens": int(token_count
                                                 * args.restrict_length)
                    }
                else:
                    generation_config = None

                turns.add_turn(turn_prefix + line.strip())
                gemini = genai.GenerativeModel(
                    args.model_key,
                    generation_config=generation_config,
                    system_instruction=first_prompt,
                )

                while True:
                    try:
                        response = gemini.generate_content(turns.to_list())
                    except Exception as e:
                        logger.error(f"Gemini API error: {e}")
                        if attempt < MAX_ATTEMPTS:
                            attempt += 1
                            logger.info(f"Retrying... {attempt}")
                            continue
                        else:
                            break

                    try:
                        response.text
                    except ValueError:
                        logger.error(f"Response error: {response}")
                        if attempt < MAX_ATTEMPTS:
                            attempt += 1
                            logger.info(f"Retrying... {attempt}")
                            continue
                        else:
                            response.text = '.'
                            turns = MessageDeque()
                            break

                    if hasattr(response, 'text') and '\n' in response.text.rstrip("\n"):
                        if attempt < MAX_ATTEMPTS:
                            attempt += 1
                            logger.info(f"Retrying... {attempt}")
                            logger.info(f"'{response.text=}'")
                        else:
                            break
                    else:
                        break

                if args.verbose:
                    logger.info(turns.to_list())
                    logger.info(response)

                if '\n' in response.text.rstrip("\n"):
                    print(line.strip() + '\t' + response.text.split('\n')[0].strip('"'),
                          file=outfile)
                    turns = MessageDeque()

                else:
                    print(line.strip() + '\t' + response.text.rstrip("\n").strip('"'),
                          file=outfile)
                    turns.add_response(response)


if __name__ == '__main__':
    main()
