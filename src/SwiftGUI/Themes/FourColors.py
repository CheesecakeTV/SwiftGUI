from SwiftGUI import GlobalOptions as go
import SwiftGUI as sg
from SwiftGUI.Themes._BaseTheme import BaseTheme

"""
These themes are based on colors of https://colorhunt.co 
Check it out, great website!
"""

class BaseFourColors(BaseTheme):
    suffix = "FourColors"

    col1 = "" # Dark text
    col2 = "" # Background
    col3 = "" # Highlights
    col4 = "" # Light text

    def apply(self) -> None:
        c1 = "#" + self.col1
        c2 = "#" + self.col2
        c3 = "#" + self.col3
        c4 = "#" + self.col4

        temp = go.Common
        temp.highlightcolor = c3
        temp.highlightbackground_color = c2

        #temp = go.Table
        go.Table.background_color = c2
        go.Table.background_color_rows = c2
        go.Table.background_color_active_rows = c3
        go.Table.text_color_active = c1
        go.Table.background_color_headings = c4
        go.Table.background_color_active_headings = c3
        go.Table.text_color_headings = c1
        go.Table.text_color_active_headings = c1

        temp = go.Checkbox
        temp.check_background_color = c1
        temp.background_color_active = c1
        temp.text_color_active = c4

        temp = go.Common_Background
        temp.background_color = c1

        temp = go.Common_Field_Background
        temp.background_color = c2

        temp = go.Common_Textual
        temp.text_color = c4

        temp = go.Notebook
        temp.text_color_tabs = c4
        temp.text_color_tabs_active = c3
        temp.background_color_tabs = c2

        temp = go.Button
        temp.background_color_active = c3
        temp.text_color_active = c1

        temp = go.Input
        temp.selectbackground_color = c3
        temp.select_text_color = c1
        temp.cursor_color = c3
        temp.text_color_disabled = c3
        temp.background_color_readonly = c1

        temp = go.Spinbox
        temp.background_color_button = c2

        temp = go.Separator
        temp.color = c3

        temp = go.LabelFrame
        temp.highlightbackground_color = c4
        temp.relief = "ridge"
        temp.text_color = c3

        temp = go.Listbox
        temp.background_color_selected = c3
        temp.text_color_selected = c1
        temp.text_color = c4
        temp.background_color = c2

        temp = go.Scale
        temp.highlightbackground_color = c1
        temp.troughcolor = c2
        temp.background_color_active = c3

    def get_palette_frame(self, width: int = 50, height: int = 200) -> sg.Frame:
        """
        Returns an sg.Frame that contains the 4 containing colors.
        The size of the frame can be adjusted
        :param width:
        :param height:
        :return:
        """
        height = height // 4
        return sg.Frame([
            [sg.Frame([[sg.Spacer(width=width, height=height)]], background_color= "#" + self.col1)],
            [sg.Frame([[sg.Spacer(width=width, height=height)]], background_color="#" + self.col2)],
            [sg.Frame([[sg.Spacer(width=width, height=height)]], background_color="#" + self.col3)],
            [sg.Frame([[sg.Spacer(width=width, height=height)]], background_color="#" + self.col4)],
        ])

    def preview_palette(self):
        """
        Open the color-palette as a window
        :return:
        """
        layout = [
            [
                self.get_palette_frame()
            ]
        ]
        sg.Window(layout).loop_close()

# class New(BaseFourColors):
#     col1 = ""
#     col2 = ""
#     col3 = ""
#     col4 = ""

class RoyalBlue(BaseFourColors):
    col1 = "21325E"
    col2 = "3E497A"
    col3 = "F1D00A"
    col4 = "F0F0F0"

class RoyalBeige(BaseFourColors):
    col4 = "42032C"
    col3 = "D36B00"
    col2 = "E6D2AA"
    col1 = "F1EFDC"

class LooksGoodSomehow(BaseFourColors):
    col1 = "42032C"
    col2 = "D36B00"
    col3 = "E6D2AA"
    col4 = "F1EFDC"

class NightHorizon(BaseFourColors):
    col1 = "000000"
    col2 = "262A56"
    col3 = "B8621B"
    col4 = "E3CCAE"

class SparkOfMagic(BaseFourColors):
    col1 = "363062"
    col2 = "4D4C7D"
    col3 = "F99417"
    col4 = "F5F5F5"

class GarnetFlair(BaseFourColors):
    col1 = "0F0E0E"
    col2 = "541212"
    col3 = "468A9A"
    col4 = "EEEEEE"

class PastelReef(BaseFourColors):
    col1 = "245953"
    col2 = "408E91"
    col3 = "E49393"
    col4 = "D8D8D8"

class Maritime(BaseFourColors):
    col1 = "071952"
    col2 = "088395"
    col3 = "37B7C3"
    col4 = "EBF4F6"

class HotAsh(BaseFourColors):
    col3 = "ED7D31"
    col2 = "6C5F5B"
    col1 = "4F4A45"
    col4 = "F6F1EE"

class Snake(BaseFourColors):
    col3 = "F3CA52"
    col4 = "F6E9B2"
    col1 = "0A6847"
    col2 = "7ABA78"

class IvoryTerracotta(BaseFourColors):
    col1 = "FAF7F0"
    col2 = "D8D2C2"
    col3 = "B17457"
    col4 = "4A4947"

class OrangeCake(BaseFourColors):
    col4 = "C14600"
    col3 = "FF9D23"
    col2 = "E5D0AC"
    col1 = "FEF9E1"

class CinnamonLatte(BaseFourColors):
    col4 = "F8F4E1"
    col3 = "FEBA17"
    col2 = "74512D"
    col1 = "4E1F00"

class FriedEgg(BaseFourColors):
    col1 = "F8F4E1"
    col2 = "FEBA17"
    col3 = "74512D"
    col4 = "4E1F00"

class Goldenberry(BaseFourColors):
    col1 = "626F47"
    col2 = "A4B465"
    col3 = "FFCF50"
    col4 = "FEFAE0"


# Version 0.5.4
class Goldfish(BaseFourColors):
    col3 = "FF731D"
    col4 = "FFF7E9"
    col2 = "5F9DF7"
    col1 = "1746A2"

class LightCloud(BaseFourColors):
    col1 = "F7F7F7"
    col2 = "EEEEEE"
    col4 = "393E46"
    col3 = "929AAB"

class FrostyBlue(BaseFourColors):
    col1 = "F1F3F8"
    col2 = "D6E0F0"
    col3 = "8D93AB"
    col4 = "393B44"

class Emerald(BaseFourColors):
    col1 = "232931"
    col2 = "393E46"
    col3 = "4ECCA3"
    col4 = "EEEEEE"

class FairyPink(BaseFourColors):
    col4 = "440A67"
    col3 = "93329E"
    col2 = "B4AEE8"
    col1 = "FFE3FE"

class DeepPurple(BaseFourColors):
    col1 = "440A67"
    col2 = "93329E"
    col3 = "B4AEE8"
    col4 = "FFE3FE"

class DarkCoffee(BaseFourColors):
    col4 = "E6E6E6"
    col3 = "C5A880"
    col2 = "532E1C"
    col1 = "0F0F0F"

class MilkTea(BaseFourColors):
    col1 = "E6E6E6"
    col2 = "C5A880"
    col3 = "532E1C"
    col4 = "0F0F0F"

class Maroon(BaseFourColors):
    col4 = "E4C59E"
    col3 = "AF8260"
    col2 = "803D3B"
    col1 = "322C2B"

class _Debug(BaseFourColors):
    col4 = "AA0000"
    col3 = "00AA00"
    col2 = "0000AA"
    col1 = "000000"

class ToffeeBrown(BaseFourColors):
    col1 = "E4C59E"
    col2 = "AF8260"
    col4 = "803D3B"
    col3 = "322C2B"

class Jungle(BaseFourColors):
    col1 = "191A19"
    col2 = "1E5128"
    col3 = "4E9F3D"
    col4 = "D8E9A8"

class Teal(BaseFourColors):
    col4 = "2C3333"
    col3 = "2E4F4F"
    col2 = "0E8388"
    col1 = "CBE4DE"

class SlateBlue(BaseFourColors):
    col1 = "2C3333"
    col2 = "2E4F4F"
    #col3 = "0E8388"
    col3 = "CBE4DE"
    col4 = "CBE4DE"

class ArcticGlow(BaseFourColors):
    col1 = "303841"
    col2 = "00ADB5"
    col4 = "EEEEEE"
    col3 = "FF5722"

class PumpkinSpice(BaseFourColors):
    col4 = "2D2424"
    col3 = "5C3D2E"
    col2 = "B85C38"
    col1 = "E0C097"

class Chocolate(BaseFourColors):
    col1 = "2D2424"
    col2 = "5C3D2E"
    col3 = "B85C38"
    col4 = "E0C097"

class SinCity(BaseFourColors):
    col1 = "171717"
    col2 = "444444"
    col3 = "DA0037"
    col4 = "EDEDED"

class ObsidianRed(BaseFourColors):
    col4 = "DDDDDD"
    col1 = "222831"
    col2 = "30475E"
    col3 = "F05454"

class DarkGold(BaseFourColors):
    col1 = "222831"
    col2 = "393E46"
    col3 = "FFD369"
    col4 = "EEEEEE"

# Can't think of a name
# class Fall(BaseFourColors):
#     col1 = "675D50"
#     col2 = "A9907E"
#     col4 = "F3DEBA"
#     col3 = "ABC4AA"

class NeonRed(BaseFourColors):
    col1 = "000000"
    col2 = "3D0000"
    #col3 = "950101"
    col3 = "FF0000"
    col4 = "FF0000"

class NeonDiamond(BaseFourColors):
    col1 = "212121"
    col2 = "323232"
    #col3 = "0D7377"
    col3 = "14FFEC"
    col4 = "14FFEC"

# class NeonRose(BaseFourColors):
#     col1 = "355C7D"
#     col2 = "6C5B7B"
#     col3 = "C06C84"
#     col4 = "F67280"

class Froggy(BaseFourColors):
    col1 = "EDF1D6"
    col2 = "9DC08B"
    col3 = "609966"
    col4 = "40513B"

class Forest(BaseFourColors):
    col4 = "EDF1D6"
    col3 = "9DC08B"
    col2 = "609966"
    col1 = "40513B"

class MatchaMilk(BaseFourColors):
    col1 = "F8EDE3"
    col2 = "BDD2B6"
    col3 = "A2B29F"
    col4 = "798777"

class CocoaMilk(BaseFourColors):
    col1 = "8D7B68"
    col2 = "A4907C"
    col3 = "C8B6A6"
    col4 = "F1DEC9"

class DeepSea(BaseFourColors):
    col1 = "1B262C"
    col2 = "0F4C75"
    col3 = "3282B8"
    col4 = "BBE1FA"

class BlueWhale(BaseFourColors):
    col1 = "27374D"
    col2 = "526D82"
    col3 = "9DB2BF"
    col4 = "DDE6ED"

class Ducky(BaseFourColors):
    col1 = "F9ED69"
    col2 = "F08A5D"
    col4 = "B83B5E"
    col3 = "6A2C70"

class DarkTeal(BaseFourColors):
    col1 = "222831"
    col2 = "393E46"
    col3 = "00ADB5"
    col4 = "EEEEEE"


