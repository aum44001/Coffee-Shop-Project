from library.lib_query_order import getInvoiceforPrint


def renderHeader(invoice_id):
    return """
    <!DOCTYPE html>
    <html>
    <head><title>InvoiceID : {0}</title>
    </head>
    """.format(invoice_id)


def renderBodyTitle(pageTitle, invoiceID,datenow):
    return """<body>
    <hr>
    <div id="printArea">
    <center><h1 style="font-family:Tahoma">""" + pageTitle + """ </h1></center><br>
    <div style=padding-left:10%>
    <p style="font-family:Tahoma"><b>Invoice ID : </b> """ + str(invoiceID) + """<br>
    <b>Order Date: </b> """ + datenow + """<br>
    </div>
    """


def renderBodyTable(items,total):
    table = """<center>
    <table border=1 style="font-family:Tahoma" width="80%">
    <tr>
    <th>Product</th>
    <th>Price</th>
    <th>Amount</th>
    <th>Total</th>
    </tr>
    """
    for i in items:
        table = table + "<tr>"
        table = table + "<td>" + i['product_name'] + " " + i['product_size'] + "</td>"
        table = table + "<td style='text-align:right'>" + str(i['product_price']) + " Baht.</td>"
        table = table + "<td style='text-align:right'>" + str(i['product_qty']) + " Piece.</td>"
        table = table + "<td style='text-align:right'>" + str(i['product_total']) + " Baht.</td>"
        table = table + "</tr>"
    table = table + """<tr>
        <td colspan="3">
        <b><p style="text-align:right;">Total Price</p></b>
        </td>
        <td style='text-align:right'>
        """ + str(total) + """
         Baht.</td>
        </tr>
        </table>
        </center>
        """
    return table


def renderBodyFooter():
    return """
    </div>
    </body>
    </html>
    """


def createhtmlfile():
    pageTitle = "Roast Coffee Shop Invoice"
    invoicedata = getInvoiceforPrint()
    invoice_id = invoicedata[0]
    datenow = str(invoicedata[1])[:19]
    items = invoicedata[2]
    total = invoicedata[3]

    HTML = renderHeader(invoice_id) + \
           renderBodyTitle(pageTitle, invoice_id,datenow) + \
           renderBodyTable(items,total) + renderBodyFooter()

    # print(HTML)
    with open("reports/invoiceID_" + str(invoice_id) + ".html", mode="w", newline="", encoding="utf8") as f:
        f.write(HTML)
