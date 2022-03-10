import ast

from flask import Flask, request, jsonify, app
# import sys
import urllib.parse
import re
from urllib.request import Request, urlopen

# path = '/dictionary_json/oussaElDictionary/Dictionary'
# if path not in sys.path:
#     sys.path.insert(0, path)

app = Flask(__name__)


@app.route("/apiou19990612Translator", methods=['GET'])
def translator_json():
    d = {}

    ta = Translator()
    text = request.args['text']
    lang_text = request.args['langText']
    lang_translation_text = request.args['langTransText']
    data = get_translator_data(text, lang_text, lang_translation_text)
    if ta.get_word_translated(data, text) != ['word not find']:
        d['translation'] = ta.get_word_translated(data, text)
    else:
        data = get_translator_data(text.replace(' ', '-'), lang_text, lang_translation_text)
        d['translation'] = ta.get_word_translated(data, text)
    return jsonify(d)


def get_translator_data(word, lang_word, lang_translation):
    # link = 'https://translate.google.com/?hl=fr&sl='+lang_word+'&tl='+lang_translation+'&text='+word+'&op=translate'
    # link = 'https://translate.yandex.com/?lang='+lang_word+'-'+lang_translation+'&text='+word
    link = f"https://mymemory.translated.net/en/{lang_word}/{lang_translation}/{urllib.parse.quote(word)}"
    headers = {'use-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
               }
    try:
        # print(f"https://mymemory.translated.net/en/{lang_word}/{lang_translation}/{urllib.parse.quote(word)}")
        # print(urllib.parse.unquote(urllib.parse.quote(link+'/', safe='/')))
        # print(link)
        req = Request(link, headers=headers)
        # print(urllib.parse.quote(link), "eeee")
        web_page = urlopen(req)
        data = web_page.read()
    except Exception:
        data = 'word not find'
    return data


class Translator:

    def get_word_translated(self, data, word):
        if data != 'word not find':
            if not re.search('<h1 class="search_title">Results for.*?translation.*?</h1>', str(data)):
                return ["500"]
            aa = re.findall(r'<span class="text">(.*?)</span>', str(data))
            word_translated = []
            if len(aa) == 0:
                word_translated = ['hard to get it']
            if len(str(word).split()) == 1 or len(str(word).split()) == 2:
                for i in range(len(aa)):
                    if '>' not in aa[i] or '<' not in aa[i]:
                        aai = str(ast.literal_eval("b'" + aa[i] + "'").decode('utf-8')).replace('&quot;', '')
                        if '&' not in aa[i]:
                            if str(word).lower() not in aa[i] and str(word).upper() not in aa[i] and str(word)[
                                0].upper() + str(word)[1:].lower() not in aa[i]:
                                if '[' not in aa[i] and ']' not in aa[i] and '(' not in aa[i] and ')' not in aa[
                                    i] and '{' not in aa[i] and '}' not in aa[i]:
                                    if '@' not in aa[i]:
                                        if '*' not in aa[i]:
                                            if len(aai.split()) >= 15:
                                                aair = aai.replace(' ', '')
                                                if ';' not in aair and len(aair.split(';')) == 1:
                                                    continue
                                                if ',' not in aair and len(aair.split(',')) == 1:
                                                    continue
                                                if '-' not in aair and len(aair.split('-')) == 1:
                                                    continue
                                                if ';' in aair and len(aair.split(';')) < 4:
                                                    continue
                                                if ',' in aair and len(aair.split(',')) < 4:
                                                    continue
                                                if '-' in aair and len(aair.split('-')) < 4:
                                                    continue
                                            if aai.replace(' ', '') != "":
                                                if aai.replace(' ', '') != ".":
                                                    word_translated.append(
                                                        aai.replace('!', '').replace('-', '').replace('.', '').replace(
                                                            ':', '').replace('~', '').replace('§', '').replace('£', ''))
            else:
                for i in range(len(aa)):
                    if '>' not in aa[i] or '<' not in aa[i]:
                        if '&' not in aa[i]:
                            if str(word).lower() not in aa[i] and str(word).upper() not in aa[i] and str(word)[
                                0].upper() + str(word)[1:].lower() not in aa[i]:
                                if '[' not in aa[i] and ']' not in aa[i] and '(' not in aa[i] and ')' not in aa[
                                    i] and '{' not in aa[i] and '}' not in aa[i]:
                                    if '@' not in aa[i]:
                                        if '*' not in aa[i]:
                                            if str(ast.literal_eval("b'" + aa[i] + "'").decode('utf-8')).replace(
                                                    '&quot;', '').replace(' ', '') != "":
                                                if str(ast.literal_eval("b'" + aa[i] + "'").decode('utf-8')).replace(
                                                        '&quot;', '').replace(' ', '') != ".":
                                                    word_translated.append(str(ast.literal_eval(
                                                        "b'" + aa[i].replace('!', '').replace('-', '').replace('.',
                                                                                                               '') + "'").decode(
                                                        'utf-8')).replace('&quot;', '').replace(':', ''))
        else:
            word_translated = ['word not find']
        return word_translated


if __name__ == "__main__":
    app.run(debug=True)
