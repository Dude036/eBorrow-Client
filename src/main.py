import eel
import protocol_builder

eel.init('web')

eel.start('html/login.html', block=False)

while True:
    eel.sleep(10)
