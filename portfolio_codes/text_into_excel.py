import xlsxwriter

workbook = xlsxwriter.Workbook('excel_genere.xlsx')
worksheet = workbook.add_worksheet()


with open("text_files/factures_auto_ecole.txt", "r", encoding="utf-8") as file:

    txt = file.read()

    lines = txt.split("\n")

    for line_nb in range(len(lines)):

        line = lines[line_nb]

        words = line.split()

        for wo_nb in range(len(words)):

            word = words[wo_nb]

            worksheet.write(line_nb, wo_nb, word)


        
workbook.close()
