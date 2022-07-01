from enum import auto
from io import TextIOWrapper
import subprocess
from typing import TypedDict

# Python3 program to convert ASCII
# string to Hexadecimal format string
 
# function to convert ASCII to HEX
def ASCIItoHEX(ascii):
 
    # Initialize final String
    hexa = ""
 
    # Make a loop to iterate through
    # every character of ascii string
    for i in range(len(ascii)):
 
        # take a char from
        # position i of string
        ch = ascii[i]
 
        # cast char to integer and
        # find its ascii value
        in1 = ord(ch)
   
        # change this ascii value
        # integer to hexadecimal value
        part = hex(in1).lstrip("0x").rstrip("L")
 
        # add this hexadecimal value
        # to final string.
        hexa += part
 
    # return the final string hex
    return hexa

def replaceXmlTemplateValue(in_xml_data: str, 
            in_placeholder: str, in_value_to_place: str) -> str :
    return in_xml_data.replace(f">{in_placeholder}<", f">{in_value_to_place}<")

def adaptXmlTemplate(in_xml_data: str, 
                in_values_to_place: TypedDict) -> str:
    for key,val in in_values_to_place.items():
        in_xml_data = replaceXmlTemplateValue(in_xml_data, key, val)
    return in_xml_data

def adaptConfTemplate(in_conf_data: str,
                in_values_to_place: TypedDict) -> str:
    for key,val in in_values_to_place.items():
        in_conf_data = in_conf_data.replace(f"={key}", f"={val}")
    return in_conf_data

def generateWinWifiFile(in_template_file: str, in_values: TypedDict, in_output_file: str):
    f: TextIOWrapper = open(in_template_file, "r")
    data = f.read()
    f.close()

    data = adaptXmlTemplate(data, in_values)

    #open and read the file after the appending:
    f = open(in_output_file, "w")
    f.write(data)
    f.close()

def generateRpiWifiFile(in_template_file: str, in_values: TypedDict, in_output_file: str):
    f: TextIOWrapper = open(in_template_file, "r")
    data = f.read()
    f.close()

    data = adaptConfTemplate(data, in_values)

    #open and read the file after the appending:
    f = open(in_output_file, "w")
    f.write(data)
    f.close()

win_template_file: str = 'template.xml'
conf_template_file: str = 'template.conf'
output_file: str = 'wifi.xml'
conf_output: str = 'wpa_supplicant.conf'

ssid: str = 'MyWifiSSID'
pswd: str = 'MyWifiPass'
autoconn: str = 'auto'

win_values: TypedDict = {"SSID" : ssid, 
                    "SSIDHEX" : ASCIItoHEX(ssid).upper(), 
                    "AUTOCONN" : autoconn,
                    "PASS" : pswd }

conf_values: TypedDict = {"SSID" : f"\"{ssid}\"",
                    "PASS": f"\"{pswd}\"" }

generateWinWifiFile(win_template_file, win_values, output_file)

generateRpiWifiFile(conf_template_file, conf_values, conf_output)
