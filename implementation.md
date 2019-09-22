# Order book implentation

## Followed approach

The required functionality was implemented in python 3 in orderBook.py. The functionality is outlined in
`Order Book Excercise.docx`.

The program takes an XML file containing orders and parses it using the `ElementTree` Libary.

The file name is taken as the first command line argument to the program.

The entire XML file is read into memory at the start of the process. This avoids multiple disk reads.

Each order action in the XML file is checked to determine what order book it belongs to. If no book is found, one is
created; Otherwise an existing book is manipulated, to add and remove orders. Order books are implemented as class
`OrderBook`. Each `OrderBook` implements function for to add orders, delete orders, and print the contents of the
orderbook.

All orders actions are stored separately from the totals for each price to allow deletion of order actions without
losing track of total orders per price.

The list of order actions is parsed in a linear manner.

Orders actions and order totals are stored in dictionaries by `orderId` and `price`.

Runtime is printed out using the datetime library.

## Notes on performance

A large portion of the run time is dedicated to the initial parsing of the XML file. The current implentation also
prints out the parsing time after completion. Performance gains could be had by not using XML, although that would
require transforming the dataset to a flat plaintext or CSV format.

Multithreading could be used as an approach, but caution should be exercised, because order actions in the same order
book influence the same order totals. The safest approach would be to split the processing by order book and to
introduce mutex locks to ensure only one thread is working on a book at a time.

Another approach could be taken if the dataset can be sorted before processing, but sorting large datasets can be very
expensive. A sorted dataset could make splitting the processing work by price easy.

A divide and conquer approach could also be taken, where the dataset is split into blocks. Each block is calculated in
it's own thread. After all the block have been processed, their results are totalled to determine the final result.

The simplest approach would however be to use a faster processor. It might not be ideal but, faster hardware can be much
cheaper that dedicating a large amount of developer time to optimization.
