import re
test = '67Mote:'
sidste = '66Note:639COVID19testedeharikkefolkeregisteradresseiDanmark.Note:47COVID19tilfældeharikkefolkeregisteradresseiDanmark.Bemærk:AntalCOVID19tilfældeerikkevistforkommunermedfærreend10COVID19tilfældeafdiskretionshensyniforholdtilpatienterne.'

regex_sidste_linie_med_text = re.compile('^(\d+)Note.+$')

matches_test = re.search(
    regex_sidste_linie_med_text, test)
matches_sidste_linie_med_text = re.search(
    regex_sidste_linie_med_text, sidste)

if matches_test is not None:
    print(matches_test.group(1))
if matches_sidste_linie_med_text is not None:
    print(matches_sidste_linie_med_text.group(1))
