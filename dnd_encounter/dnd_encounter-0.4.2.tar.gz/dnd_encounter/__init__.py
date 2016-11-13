import encounter as encounter

def main():

    args = encounter.getArgs()

    if args.name != None:
        encounter_name = args.name
    else:
        encounter_name = ' '.join(args.monsters)

    fields = [('Encounter Name', encounter_name),
              ('Difficulty', args.difficulty),
              ('XP Value', args.xp),
              ('Location', args.location)]

    for idx,m in enumerate(args.monsters):
        monster = encounter.Monster(args.xml.name, m, idx)
        fields.extend(monster.fields)


    form_data_obj = encounter.EncounterData(fields)
    form_data = form_data_obj.getData()

    encounter.fillOutPdf(form_data, args)

    form_data_obj.close()

if __name__ == '__main__':
    main()
