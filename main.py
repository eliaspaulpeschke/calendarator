import pdfkit

def main():
    options = { 
        'page-width': '1404px'
      , 'page-height': '1872px'
      , 'margin-top': '0'
      , 'margin-left': '0'
      , 'margin-bottom': '0'
      , 'margin-right': '0'
      }
    pdfkit.from_file('test.html', 'test.pdf', options=options)

    

if __name__ == "__main__":
    main()
