import hazm
import re
import string

from regexes.currency import CURRENCY_REGEX
from regexes.email import EMAIL_REGEX
from regexes.latin import LATIN_REGEX
from regexes.latin import LATIN_REGEX, LATIN_WITH_SPECIAL_REGEX
from regexes.number import NUMBERS_REGEX
from regexes.phone import PHONE_REGEX
from regexes.quote import DOUBLE_QUOTE_REGEX, SINGLE_QUOTE_REGEX
from regexes.url import URL_REGEX
from regexes.persian import PERSIAN_REGEX
from regexes.punk import PUNK_REGEX
import dictionary

allowed_char = string.ascii_letters + string.digits + ':/@_-. '


def make_trans(list_a, list_b):
    return dict((ord(a), b) for a, b in zip(list_a, list_b))


def multiple_replace(text, chars_to_mapping):
    pattern = "|".join(map(re.escape, chars_to_mapping.keys()))
    return re.sub(pattern, lambda m: chars_to_mapping[m.group()], str(text))



ar2fa_digits = make_trans("٠١٢٣٤٥٦٧٨٩٪", "۰۱۲۳۴۵۶۷۸۹٪")
fa2en_digits = make_trans("۰۱۲۳۴۵۶۷۸۹٪", "0123456789%")
normalizer = hazm.Normalizer(persian_numbers=True, punctuation_spacing=False)


def normalize(text, zwnj="\u200c", tokenized=False):
    text = text.replace("\n", " ").replace("\t", " ")
    text = re.sub(r"\u200c+", "\u200c", text)
    text = text.replace('ـ', '')
    text = normalizer.normalize(text)

    if len(dictionary.characters) > 0:
        text = multiple_replace(text, dictionary.characters)

    if len(dictionary.words_map) > 0:
        text = multiple_replace(text, dictionary.words_map)

    text = text.translate(ar2fa_digits)
    text = text.translate(fa2en_digits)

    text = SINGLE_QUOTE_REGEX.sub("'", text)
    text = DOUBLE_QUOTE_REGEX.sub('"', text)
    text = CURRENCY_REGEX.sub(r" \1 ", text)
    text = URL_REGEX.sub(" ", text)
    text = EMAIL_REGEX.sub(" ", text)
    text = PHONE_REGEX.sub(r" \1 ", text)
    text = NUMBERS_REGEX.sub(r" \1 ", text)
    text = LATIN_REGEX.sub(r" \1 ", text)
    # text = PUNK_REGEX.sub(r" \1 ", text)  # must be remained the same!

    # Allow only english and persian characters
    text = re.sub(PERSIAN_REGEX, " ", text)

    text = text.replace(f" {zwnj} ", f"{zwnj}")
    text = text.replace(f"{zwnj} ", f"{zwnj}")
    text = text.replace(f" {zwnj}", f"{zwnj}")

    if len(dictionary.special_tokens) > 0:
        text = multiple_replace(text, dictionary.special_tokens)

    tokens = []
    for token in text.split():
        token = token.strip()
        if token:
            if token.startswith(zwnj) and token.endswith(zwnj):
                token = token[1:-1]
            if token.startswith(zwnj):
                token = token[1:]
            elif token.endswith(zwnj):
                token = token[:-1]
            else:
                token = token

            tokens.append(token)

    if tokenized:
        return tokens

    return " ".join(tokens)
