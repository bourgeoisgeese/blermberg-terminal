import button as button
import yfinance as yf
import tkinter as tk
from tkinter import messagebox
import Quartz as CG
import Quartz.CoreGraphics as CGC

# Define the GUI window
window = tk.Tk()
window.title('blermberg turminel')
window.geometry('500x600')

# Change background color
window.configure(bg='#000000')

# Add a border
window.tk_setPalette(background='#000000', foreground='white', activeBackground='#000000', activeForeground='white',
                     highlightBackground='#2a2a2a', highlightColor='white', highlightThickness=1)

# Add a label with an old school font
label = tk.Label(window, text='blermberg terminal', font=('Courier', 30), bg='#000000', fg='white')
label.pack(pady=20)


# Define the function that will analyse the stock data and display the results
def analyze_data():
    # Retrieve the threshold values from the user input
    short_interest_ratio_threshold = float(short_interest_ratio_entry.get())
    short_interest_volume_threshold = int(short_interest_volume_entry.get())
    days_to_cover_threshold = float(days_to_cover_entry.get())
    put_call_ratio_threshold = float(put_call_ratio_entry.get())

    # Retrieve a dictionary of all available stock data using yfinance
    stock_data = yf.download(tickers='msft aapl', period='1y', interval='1d', group_by='ticker', as_dict=True)

    # Create a PDF document
    pdf_file = CGC.PDFDocumentCreateWithURL(
        CGC.CFURLCreateWithFileSystemPath(None, 'short_selling_behaviour_report.pdf', CG.kCFURLPOSIXPathStyle, False))
    pdf_context = CGC.CGPDFContextCreateWithURL(pdf_file, ((0, 0), (612, 792)), None)

    # Set the watermark on the PDF document
    watermark_path = 'not_for_distribution.png'
    watermark_image = CGC.CGImageCreateWithPNGDataProvider(CGC.CGDataProviderCreateWithFilename(watermark_path), None,
                                                           False, CG.kCGRenderingIntentDefault)
    pdf_context.saveGState()
    pdf_context.translateCTM(0, 792)
    pdf_context.scaleCTM(1, -1)
    pdf_context.drawPDFDocument(((0, 0), (612, 792)), pdf_file)
    pdf_context.setAlpha(0.5)
    pdf_context.drawImage(watermark_image, ((612 - watermark_image.width) / 2, (792 - watermark_image.height) / 2))
    pdf_context.restoreGState()

    # Loop through each exchange and ticker symbol and analyze their stock data
    for exchange in stock_data:
        for ticker_symbol in stock_data[exchange].keys():
            try:
                # Retrieve stock data using yfinance
                stock = stock_data[exchange][ticker_symbol]

                # Calculate the short interest ratio, short interest volume, days to cover, and put/call ratio
                short_interest_ratio = stock.info['shortInterestRatio']
                short_interest_volume = stock.info['sharesShort']
                days_to_cover = stock.info['daysToCover']
                put_call_ratio = stock.option_chain().put_call_ratio.mean()

                # Print the metrics
                print(f'Metrics for {ticker_symbol}:')
                print(f'Short interest ratio: {short_interest_ratio:.2f}')
                print(f'Short interest volume: {short_interest_volume:,}')
                print(f'Days to cover: {days_to_cover:.2f}')
                print(f'Put/call ratio: {put_call_ratio:.2f}')

            except Exception as e:

                # Write the metrics to the PDF document
                pdf_context.beginPage(None)
                pdf_context.setFont('Helvetica', 12)
                pdf_context.drawText(72, 720, f'Metrics for {ticker_symbol}:')
                pdf_context.drawText(72, 700, f'Short interest ratio: {short_interest_ratio:.2f}')
                pdf_context.drawText(72, 680, f'Short interest volume: {short_interest_volume:,}')
                pdf_context.drawText(72, 660, f'Days to cover: {days_to_cover:.2f}')
                pdf_context.drawText(72, 640, f'Put/call ratio: {put_call_ratio:.2f}\n')
                pdf_context.endPage()

                # Display a pop-up message box with the results
                messagebox.showinfo(title='blermberg terminal short seller analysis tool',
                                    message=f'{ticker_symbol} analysis complete!\n\nShort interest ratio: {short_interest_ratio:.2f}\nShort interest volume: {short_interest_volume:,}\nDays to cover: {days_to_cover:.2f}\nPut/call ratio: {put_call_ratio:.2f}')

            except Exception as e:
                print(f'Error analyzing {ticker_symbol}: {e}')

                # Save and close the PDF document
            pdf_context.close()
            pdf_file_path = CGC.CGPDFDocumentCreateWithURL(
                CGC.CFURLCreateWithFileSystemPath(None, 'short_selling_behavior_report.pdf', CG.kCFURLPOSIXPathStyle,
                                                  False))
            pdf_file_data = pdf_file_path.dataRepresentation()
            with open('short_selling_behavior_report.pdf', 'wb') as f:
                f.write(pdf_file_data)
                f.close()

            # Create labels and entry boxes for the threshold values
        short_interest_ratio_label = tk.Label(window, text='Short Interest Ratio Threshold:', font=('Courier', 14),
                                              bg='#000000', fg='white')
        short_interest_ratio_label.pack(pady=5)
        short_interest_ratio_entry = tk.Entry(window, font=('Courier', 14), bg='white', fg='black', justify='center')
        short_interest_ratio_entry.pack(pady=5)

        short_interest_volume_label = tk.Label(window, text='Short Interest Volume Threshold:', font=('Courier', 14),
                                               bg='#000000', fg='white')
        short_interest_volume_label.pack(pady=5)
        short_interest_volume_entry = tk.Entry(window, font=('Courier', 14), bg='white', fg='black', justify='center')
        short_interest_volume_entry.pack(pady=5)

        days_to_cover_label = tk.Label(window, text='Days to Cover Threshold:', font=('Courier', 14), bg='#000000',
                                       fg='white')
        days_to_cover_label.pack(pady=5)
        days_to_cover_entry = tk.Entry(window, font=('Courier', 14), bg='white', fg='black', justify='center')
        days_to_cover_entry.pack(pady=5)

        put_call_ratio_label = tk.Label(window, text='Put/Call Ratio Threshold:', font=('Courier', 14), bg='#000000',
                                        fg='white')
        put_call_ratio_label.pack(pady=5)
        put_call_ratio_entry = tk.Entry(window, font=('Courier', 14), bg='white', fg='black', justify='center')
        put_call_ratio_entry.pack(pady=5)

        # Create a button to start the analysis
        analyze_button = tk.Button(window, text='Analyze Data',

# Create a button to start the analysis
button = tk.Button(window, text='Analyze Data', font=('Courier', 20), command=analyze_data, bg='#2a2a2a', fg='white', activebackground='#ff6600', activeforeground='white')


# Run the GUI
window.mainloop()

# Save the output to a text file
with open('short_selling_behavior_report.txt', 'w') as f:
    f.write(output)

# Display a pop-up message with the results
messagebox.showinfo('Blermberg Terminal', 'blermberg has finished. Results saved to short_selling_behavior_report.txt.')

# Save the PDF document
pdf_context.finish()