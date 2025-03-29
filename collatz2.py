print ('hallo, wat is jouw naam?')
naam=input ()
print ('hallo '+naam)
print ('wat is jouw achternaam?')
naam2=input()
if naam2=='paiva'or 'Paiva':
    print('wow, jij bent familie van dr. Paiva!')
else:
    print('jammer, ik dacht dat ik met een Paiva sprak. Maar goed...')
    print ()
print ('hoe oud ben jij?')
leeftijd=int(input())
if leeftijd>=50:
    print ('met jouw leeftijd krijg je korting als oude persoon')
elif leeftijd<=11:
    print ('Jij bent te jong om zo laat wakker te zijn')
else:
    print ('je ben gelukkig nog jong')
    
