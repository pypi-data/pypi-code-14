#encoding=utf-8

DisplayStyle ={
    'default': '0',
    'bold': '1',
    'nonbold': '22',
    'underline': '4',
    'nonunderline': '24',
    'blink': '5',
    'nonblink': '25',
    'reverse': '7',
    'nonreverse': '27'}
TextColor = {
    'black': '30',
    'red': '31',
    'green': '32',
    'yellow': '33',
    'blue': '34',
    'magenta': '35',
    'cyan': '36',
    'white': '37'
}
BackgroundColor = {
    'black': '40',
    'red': '41',
    'green': '42',
    'yellow': '43',
    'blue': '44',
    'magenta': '45',
    'cyan': '46',
    'white': '47'
}

class ColorSheet():
    def __init__(self, textColor=None, backgroundColor=None, displayStyle=None):
        '''
        3 args: textColor, backgroundColor, displayStyle
        textColor: 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
        backgroundColor: 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
        displayStyle: 'default', 'bold', 'nonbold', 'underline', 'nonunderline', 'blink', 'nonblink', 'reverse', 'nonreverse'
        '''
        self.setColor(textColor)
        self.setBgColor(backgroundColor)
        self.setStyle(displayStyle)


    def setColor(self, textColor):
        '''
        available value: 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
        '''
        if TextColor.get(textColor) or textColor == None:
            self.tColor = textColor
        else:
            self.tColor = None 
            raise ValueError('invalid color: %s' % textColor)

    def setBgColor(self, backgroundColor):
        '''
        available value: 'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
        '''
        if BackgroundColor.get(backgroundColor) or backgroundColor == None:
            self.bgColor = backgroundColor
        else:
            self.bgColor = None 
            raise ValueError('invalid color: %s' % backgroundColor)

    def setStyle(self, displayStyle):
        '''
        available value: 'default', 'bold', 'nonbold', 'underline', 'nonunderline', 'blink', 'nonblink', 'reverse', 'nonreverse'
        '''
        if DisplayStyle.get(displayStyle) or displayStyle == None:
            self.style = displayStyle
        else:
            self.style = None 
            raise ValueError('invalid color: %s' % displayStyle)

    def dye(self, text):
        color = 'm'
        if self.tColor:
            color = ';' + TextColor[self.tColor] + color
        if self.bgColor:
            color = ';' + BackgroundColor[self.bgColor] + color
        if self.style:
            color = ';' + DisplayStyle[self.style] + color
        return '\033['+color+text+'\033[0m'


def test():
    for s in DisplayStyle:
        print(ColorSheet(None,None,s).dye('%-15s%-11s%-11s%-11s%-11s%-11s%-11s%-11s%-11s') % tuple([s] + [x for x in BackgroundColor]))
        for x in TextColor:
            print('%-13s%s' % (x,''.join([ColorSheet(x,y,s).dye('Hello World') for y in BackgroundColor])) )

if __name__ == '__main__':
    test()
