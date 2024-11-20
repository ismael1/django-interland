# from config.wsgi import *
from django.template.loader import get_template
from weasyprint import HTML


def printTicket():
    template = get_template('pdf/ticket.html')
    # template = get_template("pdf/ticket.html")
    context = {"name": "Interland MCL"}
    html_template = template.render(context)
    HTML(string=html_template).write_pdf(target="ticket.pdf")

printTicket()

# template = render_to_string('pdf/cotizacionPDF.html', {'ServicioCotizacion': serializer.data})