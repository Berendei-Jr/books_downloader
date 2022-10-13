import magic
mime = magic.Magic(mime=True)
print(mime.from_file("abc.pdf"))