import eel

eel.init('web')

eel.start('html/hello.html', block=False)

while True:
    eel.sleep(10)
