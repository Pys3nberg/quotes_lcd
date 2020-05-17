#! /usr/bin/python3

import time
import board
import busio
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import requests

def format_quote(data):

    return data['contents']['quotes'][0]['quote']
    

def split_quote(quote, char_len):
    
    """
    This functions purpose is to split up a sentence into
    segments where to the total characters are less than or
    equal to the amount of columns on the lcd used
    """
    
    segments = []
    words = quote.split(' ')

    # Loop through quote until no words left
    while len(words) > 0:
        s = ""
        i = -1
        
        for j, word in enumerate(words):
            # Keep adding words to current segment untill word doesn't fit
            if(len(s) + len(word) + 1) <= char_len:
                s += " " + word
                s = s.strip()
                continue
            # Else set the index so a subset of remaining words can be used
            else:
                i = j
                break
            
        segments.append(s)
        if i == -1:
            words = []
        words = words[i:]
            
    return segments

def format_crypt_data(data):
    
    output = ""
    output += "BTC:$" + str(cryptoData['BTC']['USD']) + "\n"
    output += "ETH:$" + str(cryptoData['ETH']['USD']) + "\n"

    return output

if __name__ == "__main__":

    # Get inspirational quote of the day
    resp = requests.get("http://quotes.rest/qod/inspire")   
    quoteData = resp.json()
    quote = format_quote(quoteData)

    # Get current prices of BTC and ETH from bitstamp data
    resp = requests.get("https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH&tsyms=USD&e=bitstamp")
    cryptoData = resp.json()
    crypto = format_crypt_data(cryptoData)

    # Modify this if you have a different sized Character LCD
    lcd_columns = 16
    lcd_rows = 2

    # Initialise I2C bus.
    i2c = busio.I2C(board.SCL, board.SDA)

    # Initialise the LCD class
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

    lcd.clear()
    # Set LCD color to purple
    lcd.color = [0, 100, 0]
    time.sleep(2)

    # Display segmented quote
    for seg in split_quote(quote, 16):
        lcd.clear()
        lcd.message=seg
        time.sleep(2)

    time.sleep(5)
    lcd.clear()

    # Display BTC and ETH prices
    lcd.message = crypto
