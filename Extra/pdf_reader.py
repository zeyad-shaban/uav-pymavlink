import camelot
pdf_path = "file:///C:/Users/zeyad/Downloads/Mission%202-3.pdf"

tables = camelot.read_pdf(pdf_path, pages='all')
# # for i, table in enumerate(tables):
# #     table.to_csv(f'table_{i}.csv')
# #
# # # Or get the table data as a pandas dataframe
# # for table in tables:
# #     df = table.df
# #     print(df)

# import ctypes
# from ctypes.util import find_library
# print(find_library("".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll"))))