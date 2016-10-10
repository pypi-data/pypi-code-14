from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import a4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def giro(request, queryset):
    doc = SimpleDocTemplate("form_letter.pdf",pagesize=a4,
                                 rightMargin=72,leftMargin=72,
                                 topMargin=72,bottomMargin=18)
    Story=[]
    #im = Image(logo, 2*inch, 2*inch)
    #Story.append(im)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    ptext = '<font size=16>%s</font>' % request.POST.get('title').strip()
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    for medlem in queryset:
        LocalStory = Story
        ptext = '<font size=12>Dear %s:</font>' % medlem
        LocalStory.append(Paragraph(ptext, styles["Normal"]))
        LocalStory.append(Spacer(1, 12))

        ptext = '<font size=12>%s</font>' % request.POST.get('text')
        LocalStory.append(Paragraph(ptext, styles["Justify"]))
        LocalStory.append(Spacer(1, 12))

        # lag side


def ringjelister_pdf(request):
    from cStringIO import StringIO
    #from reportlab.pdfgen import canvas
    #from reportlab.lib.units import cm #, mm
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import *
    from reportlab.lib import colors

    response = HttpResponse(mimetype="application/pdf")
    response['Content-Disposition'] = 'filename=noko.pdf'
    # Our container for 'Flowable' objects
    elements = []

    # A large collection of style sheets pre-made for us
    styles = getSampleStyleSheet()

    # A basic document for us to write to 'rl_hello_table.pdf'
    buf = StringIO()
    doc = SimpleDocTemplate(buf)

    elements.append(Paragraph("Wumpus vs Cave Population Report",
     styles['Title']))

    data2 = Medlem.objects.all()[100]
    data = [['Caves',         'Wumpus Population'],
            ['Deep Ditch',    50],
            ['Death Gully',   5000],
            ['Dire Straits',  600],
            ['Deadly Pit',    5],
            ['Conclusion',    'Run!']]

    # First the top row, with all the text centered and in Times-Bold,
    # and one line above, one line below.
    ts = [('ALIGN', (1,1), (-1,-1), 'CENTER'),
         ('LINEABOVE', (0,0), (-1,0), 1, colors.purple),
         ('LINEBELOW', (0,0), (-1,0), 1, colors.purple),
         ('FONT', (0,0), (-1,0), 'Times-Bold'),

    # The bottom row has one line above, and three lines below of
    # various colors and spacing.
         ('LINEABOVE', (0,-1), (-1,-1), 1, colors.purple),
         ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.purple,
          1, None, None, 4,1),
         ('LINEBELOW', (0,-1), (-1,-1), 1, colors.red),
         ('FONT', (0,-1), (-1,-1), 'Times-Bold')]

    # Create the table with the necessary style, and add it to the
    # elements list.
    table = Table(data2, style=ts)
    elements.append(table)

    # Write the document to disk
    doc.build(elements)
    pdf = buf.getvalue()
    response.write(pdf)
    return response
