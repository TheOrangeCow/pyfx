from pyfx import Canvas

canvas = Canvas(50, 15)
canvas.rectangle(1, 1, 48, 13)
canvas.rectangle(5, 4, 10, 5, filled=True, char=".")
canvas.line(20, 12, 30, 3, "/")
canvas.text(22, 1, "PYFX")
canvas.show()
