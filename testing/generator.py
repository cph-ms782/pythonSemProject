def verbose_generator(verbose):
    """returns a generator to loop through the filenames"""
    while True:
        yield verbose

index=0
gen = iter(verbose_generator(True))
while index<10:
    print("index: ", index)
    print(next(gen))
    index += 1