import math

NAMED_COLORS = [
    {'id': 0, 'name': 'Black', 'rgb': (0, 0, 0)},
    {'id': 1, 'name': 'Maroon', 'rgb': (128, 0, 0)},
    {'id': 2, 'name': 'Green', 'rgb': (0, 128, 128)},
    {'id': 3, 'name': 'Olive', 'rgb': (128, 128, 128)},
    {'id': 4, 'name': 'Navy', 'rgb': (0, 0, 0)},
    {'id': 5, 'name': 'Purple', 'rgb': (128, 0, 0)},
    {'id': 6, 'name': 'Teal', 'rgb': (0, 128, 128)},
    {'id': 7, 'name': 'Silver', 'rgb': (192, 192, 192)},
    {'id': 8, 'name': 'Grey', 'rgb': (128, 128, 128)},
    {'id': 9, 'name': 'Red', 'rgb': (255, 0, 0)},
    {'id': 10, 'name': 'Lime', 'rgb': (0, 255, 255)},
    {'id': 11, 'name': 'Yellow', 'rgb': (255, 255, 255)},
    {'id': 12, 'name': 'Blue', 'rgb': (0, 0, 0)},
    {'id': 13, 'name': 'Fuchsia', 'rgb': (255, 0, 0)},
    {'id': 14, 'name': 'Aqua', 'rgb': (0, 255, 255)},
    {'id': 15, 'name': 'White', 'rgb': (255, 255, 255)},
    {'id': 16, 'name': 'Grey0', 'rgb': (0, 0, 0)},
    {'id': 17, 'name': 'NavyBlue', 'rgb': (0, 0, 0)},
    {'id': 18, 'name': 'DarkBlue', 'rgb': (0, 0, 0)},
    {'id': 19, 'name': 'Blue3', 'rgb': (0, 0, 0)},
    {'id': 20, 'name': 'Blue3', 'rgb': (0, 0, 0)},
    {'id': 21, 'name': 'Blue1', 'rgb': (0, 0, 0)},
    {'id': 22, 'name': 'DarkGreen', 'rgb': (0, 95, 95)},
    {'id': 23, 'name': 'DeepSkyBlue4', 'rgb': (0, 95, 95)},
    {'id': 24, 'name': 'DeepSkyBlue4', 'rgb': (0, 95, 95)},
    {'id': 25, 'name': 'DeepSkyBlue4', 'rgb': (0, 95, 95)},
    {'id': 26, 'name': 'DodgerBlue3', 'rgb': (0, 95, 95)},
    {'id': 27, 'name': 'DodgerBlue2', 'rgb': (0, 95, 95)},
    {'id': 28, 'name': 'Green4', 'rgb': (0, 135, 135)},
    {'id': 29, 'name': 'SpringGreen4', 'rgb': (0, 135, 135)},
    {'id': 30, 'name': 'Turquoise4', 'rgb': (0, 135, 135)},
    {'id': 31, 'name': 'DeepSkyBlue3', 'rgb': (0, 135, 135)},
    {'id': 32, 'name': 'DeepSkyBlue3', 'rgb': (0, 135, 135)},
    {'id': 33, 'name': 'DodgerBlue1', 'rgb': (0, 135, 135)},
    {'id': 34, 'name': 'Green3', 'rgb': (0, 175, 175)},
    {'id': 35, 'name': 'SpringGreen3', 'rgb': (0, 175, 175)},
    {'id': 36, 'name': 'DarkCyan', 'rgb': (0, 175, 175)},
    {'id': 37, 'name': 'LightSeaGreen', 'rgb': (0, 175, 175)},
    {'id': 38, 'name': 'DeepSkyBlue2', 'rgb': (0, 175, 175)},
    {'id': 39, 'name': 'DeepSkyBlue1', 'rgb': (0, 175, 175)},
    {'id': 40, 'name': 'Green3', 'rgb': (0, 215, 215)},
    {'id': 41, 'name': 'SpringGreen3', 'rgb': (0, 215, 215)},
    {'id': 42, 'name': 'SpringGreen2', 'rgb': (0, 215, 215)},
    {'id': 43, 'name': 'Cyan3', 'rgb': (0, 215, 215)},
    {'id': 44, 'name': 'DarkTurquoise', 'rgb': (0, 215, 215)},
    {'id': 45, 'name': 'Turquoise2', 'rgb': (0, 215, 215)},
    {'id': 46, 'name': 'Green1', 'rgb': (0, 255, 255)},
    {'id': 47, 'name': 'SpringGreen2', 'rgb': (0, 255, 255)},
    {'id': 48, 'name': 'SpringGreen1', 'rgb': (0, 255, 255)},
    {'id': 49, 'name': 'MediumSpringGreen', 'rgb': (0, 255, 255)},
    {'id': 50, 'name': 'Cyan2', 'rgb': (0, 255, 255)},
    {'id': 51, 'name': 'Cyan1', 'rgb': (0, 255, 255)},
    {'id': 52, 'name': 'DarkRed', 'rgb': (95, 0, 0)},
    {'id': 53, 'name': 'DeepPink4', 'rgb': (95, 0, 0)},
    {'id': 54, 'name': 'Purple4', 'rgb': (95, 0, 0)},
    {'id': 55, 'name': 'Purple4', 'rgb': (95, 0, 0)},
    {'id': 56, 'name': 'Purple3', 'rgb': (95, 0, 0)},
    {'id': 57, 'name': 'BlueViolet', 'rgb': (95, 0, 0)},
    {'id': 58, 'name': 'Orange4', 'rgb': (95, 95, 95)},
    {'id': 59, 'name': 'Grey37', 'rgb': (95, 95, 95)},
    {'id': 60, 'name': 'MediumPurple4', 'rgb': (95, 95, 95)},
    {'id': 61, 'name': 'SlateBlue3', 'rgb': (95, 95, 95)},
    {'id': 62, 'name': 'SlateBlue3', 'rgb': (95, 95, 95)},
    {'id': 63, 'name': 'RoyalBlue1', 'rgb': (95, 95, 95)},
    {'id': 64, 'name': 'Chartreuse4', 'rgb': (95, 135, 135)},
    {'id': 65, 'name': 'DarkSeaGreen4', 'rgb': (95, 135, 135)},
    {'id': 66, 'name': 'PaleTurquoise4', 'rgb': (95, 135, 135)},
    {'id': 67, 'name': 'SteelBlue', 'rgb': (95, 135, 135)},
    {'id': 68, 'name': 'SteelBlue3', 'rgb': (95, 135, 135)},
    {'id': 69, 'name': 'CornflowerBlue', 'rgb': (95, 135, 135)},
    {'id': 70, 'name': 'Chartreuse3', 'rgb': (95, 175, 175)},
    {'id': 71, 'name': 'DarkSeaGreen4', 'rgb': (95, 175, 175)},
    {'id': 72, 'name': 'CadetBlue', 'rgb': (95, 175, 175)},
    {'id': 73, 'name': 'CadetBlue', 'rgb': (95, 175, 175)},
    {'id': 74, 'name': 'SkyBlue3', 'rgb': (95, 175, 175)},
    {'id': 75, 'name': 'SteelBlue1', 'rgb': (95, 175, 175)},
    {'id': 76, 'name': 'Chartreuse3', 'rgb': (95, 215, 215)},
    {'id': 77, 'name': 'PaleGreen3', 'rgb': (95, 215, 215)},
    {'id': 78, 'name': 'SeaGreen3', 'rgb': (95, 215, 215)},
    {'id': 79, 'name': 'Aquamarine3', 'rgb': (95, 215, 215)},
    {'id': 80, 'name': 'MediumTurquoise', 'rgb': (95, 215, 215)},
    {'id': 81, 'name': 'SteelBlue1', 'rgb': (95, 215, 215)},
    {'id': 82, 'name': 'Chartreuse2', 'rgb': (95, 255, 255)},
    {'id': 83, 'name': 'SeaGreen2', 'rgb': (95, 255, 255)},
    {'id': 84, 'name': 'SeaGreen1', 'rgb': (95, 255, 255)},
    {'id': 85, 'name': 'SeaGreen1', 'rgb': (95, 255, 255)},
    {'id': 86, 'name': 'Aquamarine1', 'rgb': (95, 255, 255)},
    {'id': 87, 'name': 'DarkSlateGray2', 'rgb': (95, 255, 255)},
    {'id': 88, 'name': 'DarkRed', 'rgb': (135, 0, 0)},
    {'id': 89, 'name': 'DeepPink4', 'rgb': (135, 0, 0)},
    {'id': 90, 'name': 'DarkMagenta', 'rgb': (135, 0, 0)},
    {'id': 91, 'name': 'DarkMagenta', 'rgb': (135, 0, 0)},
    {'id': 92, 'name': 'DarkViolet', 'rgb': (135, 0, 0)},
    {'id': 93, 'name': 'Purple', 'rgb': (135, 0, 0)},
    {'id': 94, 'name': 'Orange4', 'rgb': (135, 95, 95)},
    {'id': 95, 'name': 'LightPink4', 'rgb': (135, 95, 95)},
    {'id': 96, 'name': 'Plum4', 'rgb': (135, 95, 95)},
    {'id': 97, 'name': 'MediumPurple3', 'rgb': (135, 95, 95)},
    {'id': 98, 'name': 'MediumPurple3', 'rgb': (135, 95, 95)},
    {'id': 99, 'name': 'SlateBlue1', 'rgb': (135, 95, 95)},
    {'id': 100, 'name': 'Yellow4', 'rgb': (135, 135, 135)},
    {'id': 101, 'name': 'Wheat4', 'rgb': (135, 135, 135)},
    {'id': 102, 'name': 'Grey53', 'rgb': (135, 135, 135)},
    {'id': 103, 'name': 'LightSlateGrey', 'rgb': (135, 135, 135)},
    {'id': 104, 'name': 'MediumPurple', 'rgb': (135, 135, 135)},
    {'id': 105, 'name': 'LightSlateBlue', 'rgb': (135, 135, 135)},
    {'id': 106, 'name': 'Yellow4', 'rgb': (135, 175, 175)},
    {'id': 107, 'name': 'DarkOliveGreen3', 'rgb': (135, 175, 175)},
    {'id': 108, 'name': 'DarkSeaGreen', 'rgb': (135, 175, 175)},
    {'id': 109, 'name': 'LightSkyBlue3', 'rgb': (135, 175, 175)},
    {'id': 110, 'name': 'LightSkyBlue3', 'rgb': (135, 175, 175)},
    {'id': 111, 'name': 'SkyBlue2', 'rgb': (135, 175, 175)},
    {'id': 112, 'name': 'Chartreuse2', 'rgb': (135, 215, 215)},
    {'id': 113, 'name': 'DarkOliveGreen3', 'rgb': (135, 215, 215)},
    {'id': 114, 'name': 'PaleGreen3', 'rgb': (135, 215, 215)},
    {'id': 115, 'name': 'DarkSeaGreen3', 'rgb': (135, 215, 215)},
    {'id': 116, 'name': 'DarkSlateGray3', 'rgb': (135, 215, 215)},
    {'id': 117, 'name': 'SkyBlue1', 'rgb': (135, 215, 215)},
    {'id': 118, 'name': 'Chartreuse1', 'rgb': (135, 255, 255)},
    {'id': 119, 'name': 'LightGreen', 'rgb': (135, 255, 255)},
    {'id': 120, 'name': 'LightGreen', 'rgb': (135, 255, 255)},
    {'id': 121, 'name': 'PaleGreen1', 'rgb': (135, 255, 255)},
    {'id': 122, 'name': 'Aquamarine1', 'rgb': (135, 255, 255)},
    {'id': 123, 'name': 'DarkSlateGray1', 'rgb': (135, 255, 255)},
    {'id': 124, 'name': 'Red3', 'rgb': (175, 0, 0)},
    {'id': 125, 'name': 'DeepPink4', 'rgb': (175, 0, 0)},
    {'id': 126, 'name': 'MediumVioletRed', 'rgb': (175, 0, 0)},
    {'id': 127, 'name': 'Magenta3', 'rgb': (175, 0, 0)},
    {'id': 128, 'name': 'DarkViolet', 'rgb': (175, 0, 0)},
    {'id': 129, 'name': 'Purple', 'rgb': (175, 0, 0)},
    {'id': 130, 'name': 'DarkOrange3', 'rgb': (175, 95, 95)},
    {'id': 131, 'name': 'IndianRed', 'rgb': (175, 95, 95)},
    {'id': 132, 'name': 'HotPink3', 'rgb': (175, 95, 95)},
    {'id': 133, 'name': 'MediumOrchid3', 'rgb': (175, 95, 95)},
    {'id': 134, 'name': 'MediumOrchid', 'rgb': (175, 95, 95)},
    {'id': 135, 'name': 'MediumPurple2', 'rgb': (175, 95, 95)},
    {'id': 136, 'name': 'DarkGoldenrod', 'rgb': (175, 135, 135)},
    {'id': 137, 'name': 'LightSalmon3', 'rgb': (175, 135, 135)},
    {'id': 138, 'name': 'RosyBrown', 'rgb': (175, 135, 135)},
    {'id': 139, 'name': 'Grey63', 'rgb': (175, 135, 135)},
    {'id': 140, 'name': 'MediumPurple2', 'rgb': (175, 135, 135)},
    {'id': 141, 'name': 'MediumPurple1', 'rgb': (175, 135, 135)},
    {'id': 142, 'name': 'Gold3', 'rgb': (175, 175, 175)},
    {'id': 143, 'name': 'DarkKhaki', 'rgb': (175, 175, 175)},
    {'id': 144, 'name': 'NavajoWhite3', 'rgb': (175, 175, 175)},
    {'id': 145, 'name': 'Grey69', 'rgb': (175, 175, 175)},
    {'id': 146, 'name': 'LightSteelBlue3', 'rgb': (175, 175, 175)},
    {'id': 147, 'name': 'LightSteelBlue', 'rgb': (175, 175, 175)},
    {'id': 148, 'name': 'Yellow3', 'rgb': (175, 215, 215)},
    {'id': 149, 'name': 'DarkOliveGreen3', 'rgb': (175, 215, 215)},
    {'id': 150, 'name': 'DarkSeaGreen3', 'rgb': (175, 215, 215)},
    {'id': 151, 'name': 'DarkSeaGreen2', 'rgb': (175, 215, 215)},
    {'id': 152, 'name': 'LightCyan3', 'rgb': (175, 215, 215)},
    {'id': 153, 'name': 'LightSkyBlue1', 'rgb': (175, 215, 215)},
    {'id': 154, 'name': 'GreenYellow', 'rgb': (175, 255, 255)},
    {'id': 155, 'name': 'DarkOliveGreen2', 'rgb': (175, 255, 255)},
    {'id': 156, 'name': 'PaleGreen1', 'rgb': (175, 255, 255)},
    {'id': 157, 'name': 'DarkSeaGreen2', 'rgb': (175, 255, 255)},
    {'id': 158, 'name': 'DarkSeaGreen1', 'rgb': (175, 255, 255)},
    {'id': 159, 'name': 'PaleTurquoise1', 'rgb': (175, 255, 255)},
    {'id': 160, 'name': 'Red3', 'rgb': (215, 0, 0)},
    {'id': 161, 'name': 'DeepPink3', 'rgb': (215, 0, 0)},
    {'id': 162, 'name': 'DeepPink3', 'rgb': (215, 0, 0)},
    {'id': 163, 'name': 'Magenta3', 'rgb': (215, 0, 0)},
    {'id': 164, 'name': 'Magenta3', 'rgb': (215, 0, 0)},
    {'id': 165, 'name': 'Magenta2', 'rgb': (215, 0, 0)},
    {'id': 166, 'name': 'DarkOrange3', 'rgb': (215, 95, 95)},
    {'id': 167, 'name': 'IndianRed', 'rgb': (215, 95, 95)},
    {'id': 168, 'name': 'HotPink3', 'rgb': (215, 95, 95)},
    {'id': 169, 'name': 'HotPink2', 'rgb': (215, 95, 95)},
    {'id': 170, 'name': 'Orchid', 'rgb': (215, 95, 95)},
    {'id': 171, 'name': 'MediumOrchid1', 'rgb': (215, 95, 95)},
    {'id': 172, 'name': 'Orange3', 'rgb': (215, 135, 135)},
    {'id': 173, 'name': 'LightSalmon3', 'rgb': (215, 135, 135)},
    {'id': 174, 'name': 'LightPink3', 'rgb': (215, 135, 135)},
    {'id': 175, 'name': 'Pink3', 'rgb': (215, 135, 135)},
    {'id': 176, 'name': 'Plum3', 'rgb': (215, 135, 135)},
    {'id': 177, 'name': 'Violet', 'rgb': (215, 135, 135)},
    {'id': 178, 'name': 'Gold3', 'rgb': (215, 175, 175)},
    {'id': 179, 'name': 'LightGoldenrod3', 'rgb': (215, 175, 175)},
    {'id': 180, 'name': 'Tan', 'rgb': (215, 175, 175)},
    {'id': 181, 'name': 'MistyRose3', 'rgb': (215, 175, 175)},
    {'id': 182, 'name': 'Thistle3', 'rgb': (215, 175, 175)},
    {'id': 183, 'name': 'Plum2', 'rgb': (215, 175, 175)},
    {'id': 184, 'name': 'Yellow3', 'rgb': (215, 215, 215)},
    {'id': 185, 'name': 'Khaki3', 'rgb': (215, 215, 215)},
    {'id': 186, 'name': 'LightGoldenrod2', 'rgb': (215, 215, 215)},
    {'id': 187, 'name': 'LightYellow3', 'rgb': (215, 215, 215)},
    {'id': 188, 'name': 'Grey84', 'rgb': (215, 215, 215)},
    {'id': 189, 'name': 'LightSteelBlue1', 'rgb': (215, 215, 215)},
    {'id': 190, 'name': 'Yellow2', 'rgb': (215, 255, 255)},
    {'id': 191, 'name': 'DarkOliveGreen1', 'rgb': (215, 255, 255)},
    {'id': 192, 'name': 'DarkOliveGreen1', 'rgb': (215, 255, 255)},
    {'id': 193, 'name': 'DarkSeaGreen1', 'rgb': (215, 255, 255)},
    {'id': 194, 'name': 'Honeydew2', 'rgb': (215, 255, 255)},
    {'id': 195, 'name': 'LightCyan1', 'rgb': (215, 255, 255)},
    {'id': 196, 'name': 'Red1', 'rgb': (255, 0, 0)},
    {'id': 197, 'name': 'DeepPink2', 'rgb': (255, 0, 0)},
    {'id': 198, 'name': 'DeepPink1', 'rgb': (255, 0, 0)},
    {'id': 199, 'name': 'DeepPink1', 'rgb': (255, 0, 0)},
    {'id': 200, 'name': 'Magenta2', 'rgb': (255, 0, 0)},
    {'id': 201, 'name': 'Magenta1', 'rgb': (255, 0, 0)},
    {'id': 202, 'name': 'OrangeRed1', 'rgb': (255, 95, 95)},
    {'id': 203, 'name': 'IndianRed1', 'rgb': (255, 95, 95)},
    {'id': 204, 'name': 'IndianRed1', 'rgb': (255, 95, 95)},
    {'id': 205, 'name': 'HotPink', 'rgb': (255, 95, 95)},
    {'id': 206, 'name': 'HotPink', 'rgb': (255, 95, 95)},
    {'id': 207, 'name': 'MediumOrchid1', 'rgb': (255, 95, 95)},
    {'id': 208, 'name': 'DarkOrange', 'rgb': (255, 135, 135)},
    {'id': 209, 'name': 'Salmon1', 'rgb': (255, 135, 135)},
    {'id': 210, 'name': 'LightCoral', 'rgb': (255, 135, 135)},
    {'id': 211, 'name': 'PaleVioletRed1', 'rgb': (255, 135, 135)},
    {'id': 212, 'name': 'Orchid2', 'rgb': (255, 135, 135)},
    {'id': 213, 'name': 'Orchid1', 'rgb': (255, 135, 135)},
    {'id': 214, 'name': 'Orange1', 'rgb': (255, 175, 175)},
    {'id': 215, 'name': 'SandyBrown', 'rgb': (255, 175, 175)},
    {'id': 216, 'name': 'LightSalmon1', 'rgb': (255, 175, 175)},
    {'id': 217, 'name': 'LightPink1', 'rgb': (255, 175, 175)},
    {'id': 218, 'name': 'Pink1', 'rgb': (255, 175, 175)},
    {'id': 219, 'name': 'Plum1', 'rgb': (255, 175, 175)},
    {'id': 220, 'name': 'Gold1', 'rgb': (255, 215, 215)},
    {'id': 221, 'name': 'LightGoldenrod2', 'rgb': (255, 215, 215)},
    {'id': 222, 'name': 'LightGoldenrod2', 'rgb': (255, 215, 215)},
    {'id': 223, 'name': 'NavajoWhite1', 'rgb': (255, 215, 215)},
    {'id': 224, 'name': 'MistyRose1', 'rgb': (255, 215, 215)},
    {'id': 225, 'name': 'Thistle1', 'rgb': (255, 215, 215)},
    {'id': 226, 'name': 'Yellow1', 'rgb': (255, 255, 255)},
    {'id': 227, 'name': 'LightGoldenrod1', 'rgb': (255, 255, 255)},
    {'id': 228, 'name': 'Khaki1', 'rgb': (255, 255, 255)},
    {'id': 229, 'name': 'Wheat1', 'rgb': (255, 255, 255)},
    {'id': 230, 'name': 'Cornsilk1', 'rgb': (255, 255, 255)},
    {'id': 231, 'name': 'Grey100', 'rgb': (255, 255, 255)},
    {'id': 232, 'name': 'Grey3', 'rgb': (8, 8, 8)},
    {'id': 233, 'name': 'Grey7', 'rgb': (18, 18, 18)},
    {'id': 234, 'name': 'Grey11', 'rgb': (28, 28, 28)},
    {'id': 235, 'name': 'Grey15', 'rgb': (38, 38, 38)},
    {'id': 236, 'name': 'Grey19', 'rgb': (48, 48, 48)},
    {'id': 237, 'name': 'Grey23', 'rgb': (58, 58, 58)},
    {'id': 238, 'name': 'Grey27', 'rgb': (68, 68, 68)},
    {'id': 239, 'name': 'Grey30', 'rgb': (78, 78, 78)},
    {'id': 240, 'name': 'Grey35', 'rgb': (88, 88, 88)},
    {'id': 241, 'name': 'Grey39', 'rgb': (98, 98, 98)},
    {'id': 242, 'name': 'Grey42', 'rgb': (108, 108, 108)},
    {'id': 243, 'name': 'Grey46', 'rgb': (118, 118, 118)},
    {'id': 244, 'name': 'Grey50', 'rgb': (128, 128, 128)},
    {'id': 245, 'name': 'Grey54', 'rgb': (138, 138, 138)},
    {'id': 246, 'name': 'Grey58', 'rgb': (148, 148, 148)},
    {'id': 247, 'name': 'Grey62', 'rgb': (158, 158, 158)},
    {'id': 248, 'name': 'Grey66', 'rgb': (168, 168, 168)},
    {'id': 249, 'name': 'Grey70', 'rgb': (178, 178, 178)},
    {'id': 250, 'name': 'Grey74', 'rgb': (188, 188, 188)},
    {'id': 251, 'name': 'Grey78', 'rgb': (198, 198, 198)},
    {'id': 252, 'name': 'Grey82', 'rgb': (208, 208, 208)},
    {'id': 253, 'name': 'Grey85', 'rgb': (218, 218, 218)},
    {'id': 254, 'name': 'Grey89', 'rgb': (228, 228, 228)},
    {'id': 255, 'name': 'Grey93', 'rgb': (238, 238, 238)},
]


def color_distance(a: 'Tuple[int, int, int]', b: 'Tuple[int, int, int]'):
    rmean = (a[0] + b[0]) // 2
    r = a[0] - b[0]
    g = a[1] - b[1]
    b = a[2] - b[2]

    return math.sqrt((((512 + rmean) * r**2) >> 8)
                     + 4 * g**2
                     + (((767 - rmean) * b**2) >> 8))


def color_name(color):
    distances = [{'id': c['id'],
                  'name': c['name'],
                  'rgb': c['rgb'],
                  'dist': color_distance(color, c['rgb'])}
                 for c in NAMED_COLORS]

    best = sorted(distances, key=lambda c: c['dist'])[0]

    return best['name']


class Color:
    def __init__(self, html=None, r=None, g=None, b=None):
        if html:
            self.value = html

        elif r or g or b:
            self._red = r or 0
            self._green = g or 0
            self._blue = b or 0

        else:
            self.value = 0

    @property
    def value(self):
        return self._red << 16 | self._green << 8 | self.blue

    @value.setter
    def value(self, val):
        self._red = (val >> 16) & 0xff
        self._green = (val >> 8) & 0xff
        self._blue = val & 0xff

    @property
    def rgb(self):
        return (self.red, self.green, self.blue)

    @rgb.setter
    def rgb(self, val):
        self.red, self.green, self.blue = val

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, val):
        self._red = max(0, min(255, val))

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, val):
        self._green = max(0, min(255, val))

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, val):
        self._blue = max(0, min(255, val))
