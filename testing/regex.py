import re
# text = 'Nordfyns‐hanssee1.680'
# text = 'Sdffghfd‐midtfyn1.680'
text = 'Nordfyns-hanssee1.680'

regex = re.compile(r'([a-zA-ZæøåÆØÅ]+\-{0,1}[a-zA-ZæøåÆØÅ]+)\s{0,3}(\d+.+)')

matches = re.search(regex, text)

if matches is not None:
    print(matches.group())
    print(matches.group(1))
    print(matches.group(2))
