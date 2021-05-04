def shout(string):
    return string.upper() + "!!!!"

if __name__ == '__main__':
    tutors = ['Simon', 'Teresa', 'Kaiqi', 'Michelle']
    angry_tutors = list(map(lambda t: t.upper() + "!!!!", tutors))
    print(angry_tutors)